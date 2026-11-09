"""Independently decode every generated vector and verify its exact integer sums."""

import argparse
import csv
import hashlib
import json
import logging
from pathlib import Path


def decode(path: Path) -> list[int]:
    lines = path.read_text(encoding="ascii").splitlines()
    if any(len(s) != 4 or any(c not in "0123456789ABCDEF" for c in s) for s in lines):
        raise ValueError(f"Invalid HEX format: {path}")
    return [int(s, 16) - (65536 if int(s, 16) >= 32768 else 0) for s in lines]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    audits = []
    try:
        for directory in sorted((args.output_dir / "vectors").iterdir()):
            if not directory.is_dir():
                continue
            meta = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
            q = decode(directory / "adc_samples.hex")
            r = decode(directory / "reference_lut.hex")
            n, period = meta["window_samples"], meta["reference"]["length"]
            def require(condition: bool, detail: str) -> None:
                if not condition:
                    raise ValueError(f"{directory.name}: {detail}")
            require(len(q) == meta["number_of_samples"], "sample count mismatch")
            require(len(r) == period and r[0] == 0, "reference count or phase mismatch")
            require(all(meta["adc"]["code_min"] <= code <= meta["adc"]["code_max"] for code in q), "invalid ADC range/sign extension")
            with (directory / "expected_results.csv").open(newline="", encoding="utf-8") as handle:
                expected = list(csv.DictReader(handle))
            require(len(expected) == len(q)//n == meta["number_of_windows"], "window count mismatch")
            for i, row in enumerate(expected):
                start, end = i*n, (i+1)*n-1
                require(int(row["window_index"]) == i and int(row["start_sample"]) == start
                        and int(row["end_sample"]) == end, "window alignment mismatch")
                actual = sum(q[j]*r[j % period] for j in range(start, end+1))
                require(actual == int(row["expected_accumulator"]), f"integer accumulator mismatch in window {i}")
            truth = args.output_dir / "ground_truth" / directory.name / "ground_truth.csv"
            with truth.open(newline="", encoding="utf-8") as handle:
                rows = csv.DictReader(handle)
                count = 0
                for index, row in enumerate(rows):
                    require(index < len(q), "extra ground truth row")
                    require(int(row["sample_index"]) == index and int(row["adc_code"]) == q[index], "ground truth ordering/code mismatch")
                    count += 1
            require(count == len(q), "ground truth row count mismatch")
            files = list(directory.iterdir()) + [truth]
            hashes = {str(path.relative_to(args.output_dir)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}
            audits.append({"scenario": directory.name, "samples": len(q), "windows": len(expected), "sha256": hashes})
            logging.info("%s: %d samples and %d exact accumulators verified", directory.name, len(q), len(expected))
        if not audits:
            raise ValueError("No scenario exports found")
        report = {"status": "passed", "scenario_count": len(audits), "sample_count": sum(a["samples"] for a in audits),
                  "window_count": sum(a["windows"] for a in audits), "scenarios": audits}
        reports = args.output_dir / "reports"
        reports.mkdir(parents=True, exist_ok=True)
        (reports / "export_audit.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    except (OSError, ValueError, KeyError) as error:
        parser.exit(1, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
