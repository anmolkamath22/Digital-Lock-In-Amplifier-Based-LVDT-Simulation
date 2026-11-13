"""Run the Verilog lock-in (hdl/rtl/lockin_top.v + hdl/sim/tb_lockin.v) on exported vectors.

Engine priority:
  1. Icarus Verilog (iverilog + vvp) if on PATH
  2. Vivado xsim (xvlog + xelab + xsim) if on PATH
  3. Cycle-accurate Python model of lockin_top (fallback, clearly labelled)

All engines produce the same CSV contract as the testbench: window_index,accumulator
(window_index is 1-based, as written by tb_lockin.v).
"""

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RTL = ROOT / "hdl" / "rtl" / "lockin_top.v"
TB = ROOT / "hdl" / "sim" / "tb_lockin.v"
WINDOW = 200  # hard-coded in lockin_top.v (sample_count == 199)
LUT_LEN = 20  # hard-coded in lockin_top.v (lut_index == 19)


def _hex_words(path: Path) -> list[int]:
    out = []
    for line in path.read_text().split():
        v = int(line, 16)
        out.append(v - 0x10000 if v & 0x8000 else v)
    return out


def _wrap40(v: int) -> int:
    v &= (1 << 40) - 1
    return v - (1 << 40) if v & (1 << 39) else v


def python_model(adc_hex: Path, lut_hex: Path) -> list[int]:
    """Bit-exact behavioural mirror of lockin_top.v, one accepted sample per clock."""
    samples, lut = _hex_words(adc_hex), _hex_words(lut_hex)
    idx = count = acc = 0
    results = []
    for s in samples:
        product = s * lut[idx]  # signed 16x16 -> 32
        idx = 0 if idx == LUT_LEN - 1 else idx + 1
        if count == WINDOW - 1:
            results.append(_wrap40(acc + product))
            acc, count = 0, 0
        else:
            acc, count = _wrap40(acc + product), count + 1
    return results


def _read_results(csv_path: Path) -> list[int]:
    with csv_path.open() as f:
        return [int(r["accumulator"]) for r in csv.DictReader(f)]


def _run(cmd: list[str], cwd: Path) -> str:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=300)
    log = f"$ {' '.join(cmd)}\n{p.stdout}{p.stderr}"
    if p.returncode != 0:
        raise RuntimeError(log)
    return log


def _add_iverilog_to_path() -> None:
    """Pick up Icarus from IVERILOG_BIN or common install dirs even if PATH is stale."""
    import os
    if shutil.which("iverilog"):
        return
    candidates = [os.environ.get("IVERILOG_BIN", ""),
                  str(Path.home() / "iverilog" / "ucrt64" / "bin"),
                  str(Path.home() / "iverilog" / "bin"), r"C:\iverilog\bin"]
    for c in candidates:
        if c and (Path(c) / "iverilog.exe").exists():
            os.environ["PATH"] = c + os.pathsep + os.environ.get("PATH", "")
            return


_add_iverilog_to_path()


def available_engine() -> str:
    if shutil.which("iverilog") and shutil.which("vvp"):
        return "iverilog"
    if shutil.which("xvlog") and shutil.which("xelab") and shutil.which("xsim"):
        return "xsim"
    return "python-model"


def run_hdl(vector_dir: Path, work: Path, lut_override: Path | None = None) -> dict:
    """Stage vectors as work/data/*.hex (paths the RTL/TB expect) and simulate.

    lut_override lets the same unmodified RTL run with a different reference
    (e.g. a cosine LUT to obtain the quadrature channel)."""
    data = work / "data"
    data.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(vector_dir / "adc_samples.hex", data / "adc_samples.hex")
    shutil.copyfile(lut_override or vector_dir / "reference_lut.hex", data / "reference_lut.hex")
    n = len((data / "adc_samples.hex").read_text().split())
    defines = {"ADC_HEX": '"data/adc_samples.hex"', "NUM_SAMPLES": str(n)}
    engine = available_engine()
    log = ""
    if engine == "iverilog":
        d = [f"-D{k}={v}" for k, v in defines.items()]
        log += _run(["iverilog", "-g2005", *d, "-o", "tb.vvp", str(TB), str(RTL)], work)
        log += _run(["vvp", "-n", "tb.vvp"], work)
        results = _read_results(work / "rtl_results.csv")
    elif engine == "xsim":
        d = [x for k, v in defines.items() for x in ("-d", f"{k}={v}")]
        log += _run(["xvlog", *d, str(RTL), str(TB)], work)
        log += _run(["xelab", "tb_lockin", "-s", "tb_snap"], work)
        log += _run(["xsim", "tb_snap", "-R"], work)
        results = _read_results(work / "rtl_results.csv")
    else:
        results = python_model(data / "adc_samples.hex", data / "reference_lut.hex")
        with (work / "rtl_results.csv").open("w", newline="") as f:
            f.write("window_index,accumulator\n")
            for i, r in enumerate(results, 1):
                f.write(f"{i},{r}\n")
        log = ("No Verilog simulator found on PATH (iverilog / Vivado xsim).\n"
               "Used cycle-accurate Python model of lockin_top.v. Install Icarus Verilog\n"
               "to run the real RTL: https://bleyer.org/icarus/\n"
               f"Total windows processed = {len(results)}\n")
    return {"engine": engine, "results": results, "log": log}
