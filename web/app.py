"""Demo web app: tune Python signal generation -> export vectors -> run Verilog lock-in -> compare.

Run from the repository root:
    python -m pip install -e . --no-build-isolation --no-deps
    python web/app.py         # then open http://127.0.0.1:5000
"""

from __future__ import annotations

import csv
import io
import json
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request, send_file, send_from_directory

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hdl_runner import ROOT, available_engine, run_hdl  # noqa: E402

from lvdt_sim.config import Config  # noqa: E402
from lvdt_sim.pipeline import export_simulation, run  # noqa: E402
from lvdt_sim import export  # noqa: E402

RUNS = ROOT / "output" / "web_runs"
app = Flask(__name__, static_folder="static")

# Parameters exposed in the UI. fs/fc/LUT/window are fixed because lockin_top.v hard-codes them.
FLOAT_KEYS = ["duration_s", "sensitivity_v_per_mm", "secondary_null_v", "phase_deg", "cubic_v_per_mm3",
              "noise_std_v", "hum_peak_v", "hum_hz", "dc_offset_v", "interference_peak_v",
              "interference_hz", "interference_phase_deg", "drift_peak_v", "drift_hz"]
TRAJ_KEYS = {
    "static": ["value_mm"],
    "step": ["before_mm", "after_mm", "step_s"],
    "sine": ["center_mm", "amplitude_mm", "frequency_hz", "phase_deg"],
    "ramp": ["start_mm", "end_mm"],
    "calibration": ["hold_windows"],
}


def _decimate(a, n=2000):
    a = np.asarray(a)
    step = max(1, len(a) // n)
    return a[::step].tolist(), step


def build_config(p: dict) -> Config:
    kw = {k: float(p[k]) for k in FLOAT_KEYS if k in p}
    kw["seed"] = int(p.get("seed", 42))
    mode = p.get("mode", "static")
    if mode not in TRAJ_KEYS:
        raise ValueError(f"unknown trajectory mode {mode!r}")
    traj = {"mode": mode}
    for k in TRAJ_KEYS[mode]:
        if mode == "sine" and k == "phase_deg":  # sensor phase_deg shares the name
            if "traj_phase" in p:
                traj[k] = float(p["traj_phase"])
            continue
        if k in p:
            traj[k] = int(p[k]) if k == "hold_windows" else float(p[k])
    if mode == "calibration":
        hold = traj.get("hold_windows", 5)
        kw["duration_s"] = 7 * hold * 200 / 20000.0  # 7 default levels
    if kw.get("duration_s", 1.0) > 5:
        raise ValueError("duration_s limited to 5 s in the demo")
    kw["trajectory"] = traj
    return Config(**kw)


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/info")
def info():
    return jsonify({"engine": available_engine()})


@app.post("/api/generate")
def generate():
    p = request.get_json(force=True)
    try:
        cfg = build_config(p)
        t0 = time.perf_counter()
        sim = run(cfg, int(p.get("stream_id", 0)))
        name = f"run_{int(time.time()*1000)}"
        paths = export_simulation(sim, RUNS, name)
        py_ms = (time.perf_counter() - t0) * 1000
    except (ValueError, TypeError, KeyError) as e:
        return jsonify({"error": str(e)}), 400

    n_show = min(len(sim.time_s), 400)  # first 20 carrier cycles, full resolution
    x_dec, step = _decimate(sim.displacement_mm)
    fx = sim.fixed
    fft = np.abs(np.fft.rfft(sim.measured_v * np.hanning(len(sim.measured_v))))
    freqs = np.fft.rfftfreq(len(sim.measured_v), 1 / cfg.fs_hz)
    fft_db = 20 * np.log10(fft / fft.max() + 1e-12)
    f_dec, fstep = _decimate(fft_db, 1500)
    return jsonify({
        "run": name,
        "python_ms": round(py_ms, 1),
        "samples": cfg.sample_count,
        "windows": int(len(fx.accumulator)),
        "clipped": int(sim.adc.clipped_count),
        "clipped_percent": float(sim.adc.clipped_percent),
        "zoom": {
            "t": sim.time_s[:n_show].tolist(),
            "s1": sim.sensor.secondary_1_v[:n_show].tolist(),
            "s2": sim.sensor.secondary_2_v[:n_show].tolist(),
            "diff": sim.sensor.differential_v[:n_show].tolist(),
            "measured": sim.measured_v[:n_show].tolist(),
            "adc": sim.adc.codes[:n_show].astype(int).tolist(),
        },
        "traj": {"t": sim.time_s[::step].tolist(), "x": x_dec},
        "spectrum": {"f": freqs[::fstep].tolist(), "db": f_dec},
        "expected": {
            "center_t": fx.center_time_s.tolist(),
            "acc": [int(a) for a in fx.accumulator],
            "x_fixed": fx.displacement_mm.tolist(),
            "x_float": sim.floating.displacement_mm.tolist(),
            "truth": sim.true_window_mean_mm.tolist(),
        },
        "paths": paths,
    })


@app.post("/api/simulate/<name>")
def simulate(name: str):
    if not name.startswith("run_") or not name[4:].isdigit():
        return jsonify({"error": "bad run name"}), 400
    vec = RUNS / "vectors" / name
    if not vec.exists():
        return jsonify({"error": "run not found; generate first"}), 404
    t0 = time.perf_counter()
    work = RUNS / "hdl" / name
    # Quadrature reference: same Q1.14 format as the sine LUT, cos instead of sin.
    cos_lut = np.rint(16384 * np.cos(2 * np.pi * np.arange(20) / 20)).astype(np.int16)
    cos_path = RUNS / "vectors" / name / "reference_lut_cos.hex"
    export.write_hex(cos_path, cos_lut)
    try:
        out = run_hdl(vec, work / "I")                    # in-phase: original sine LUT
        out_q = run_hdl(vec, work / "Q", cos_path)        # quadrature: same RTL, cosine LUT
    except Exception as e:  # simulator failure -> show its log
        return jsonify({"error": str(e)}), 500
    ms = (time.perf_counter() - t0) * 1000
    with (vec / "expected_results.csv").open() as f:
        exp = [int(r["expected_accumulator"]) for r in csv.DictReader(f)]
    # Exact Python golden Q sums (int64) from the exported ADC codes.
    codes = export.read_hex(vec / "adc_samples.hex").astype(np.int64)
    nwin = len(codes) // 200
    exp_q = (codes[:nwin * 200] * np.tile(cos_lut.astype(np.int64), nwin * 10)).reshape(nwin, 200).sum(1)
    exp_q = [int(v) for v in exp_q]
    rtl, rtl_q = out["results"], out_q["results"]
    K = json.loads((vec / "metadata.json").read_text())["configuration"]["sensitivity_v_per_mm"]
    to_v = 2 / (200 * 16384) * (2.5 / 2048)           # accumulator -> volts peak
    i_v = np.array(rtl, dtype=float) * to_v
    q_v = np.array(rtl_q, dtype=float) * to_v
    mag_v = np.hypot(i_v, q_v)
    phase = np.degrees(np.arctan2(q_v, i_v))
    mism = [i for i in range(min(len(exp), len(rtl))) if exp[i] != rtl[i]]
    mism_q = [i for i in range(min(len(exp_q), len(rtl_q))) if exp_q[i] != rtl_q[i]]
    passed = not mism and len(exp) == len(rtl)
    passed_q = not mism_q and len(exp_q) == len(rtl_q)
    return jsonify({
        "engine": out["engine"], "log": out["log"] + "\n--- Quadrature run (cosine LUT) ---\n" + out_q["log"],
        "hdl_ms": round(ms, 1),
        "rtl_acc": rtl, "rtl_q_acc": rtl_q, "expected_q": exp_q,
        "rtl_mm": (i_v / K).tolist(),
        "i_v": i_v.tolist(), "q_v": q_v.tolist(), "mag_v": mag_v.tolist(), "mag_mm": (mag_v / K).tolist(),
        "phase_deg": phase.tolist(), "K": K,
        "expected_count": len(exp), "rtl_count": len(rtl),
        "mismatches": len(mism) + abs(len(exp) - len(rtl)), "first_mismatch": mism[0] if mism else None,
        "mismatches_q": len(mism_q) + abs(len(exp_q) - len(rtl_q)),
        "passed": passed, "passed_q": passed_q,
    })


@app.get("/api/download/<name>")
def download(name: str):
    if not name.startswith("run_") or not name[4:].isdigit():
        return "bad name", 400
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for sub in ("vectors", "ground_truth", "hdl"):
            d = RUNS / sub / name
            if d.exists():
                for f in d.rglob("*"):
                    if f.is_file() and f.suffix in {".hex", ".csv", ".json"}:
                        z.write(f, f"{sub}/{f.relative_to(d).as_posix()}")
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"{name}.zip", mimetype="application/zip")


if __name__ == "__main__":
    import os
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    if os.environ.get("FLASK_DEV") == "1":
        app.run(host=host, port=port, debug=True)
    else:
        try:
            from waitress import serve
            print(f"Serving on http://{host}:{port} (waitress)")
            serve(app, host=host, port=port, threads=4)
        except ImportError:
            app.run(host=host, port=port)
