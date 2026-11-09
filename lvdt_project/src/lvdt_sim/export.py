"""Strict signed-16 HEX and explicit ordered CSV/JSON data contracts."""

import csv
import json
from pathlib import Path
import re
from collections.abc import Mapping, Sequence
import numpy as np
from numpy.typing import NDArray

GROUND_TRUTH_COLUMNS = ["sample_index", "time_s", "displacement_mm", "primary_voltage_v",
                        "secondary_1_v", "secondary_2_v", "differential_voltage_v",
                        "measured_analog_voltage_v", "adc_code"]
EXPECTED_COLUMNS = ["window_index", "start_sample", "end_sample", "center_time_s",
                    "expected_accumulator", "estimated_displacement_mm", "true_window_mean_mm", "absolute_error_mm"]


def write_hex(path: str | Path, values: NDArray) -> None:
    a = np.asarray(values)
    if a.ndim != 1 or a.dtype.kind not in "iu" or np.any(a < -32768) or np.any(a > 32767):
        raise ValueError("HEX values must be a signed-16-range integer vector")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(f"{int(v) & 0xffff:04X}\n" for v in a), encoding="ascii")


def read_hex(path: str | Path) -> NDArray[np.int16]:
    lines = Path(path).read_text(encoding="ascii").splitlines()
    if any(not re.fullmatch(r"[0-9a-fA-F]{4}", line) for line in lines):
        raise ValueError("Each HEX line must contain exactly four hexadecimal characters")
    words = [int(line, 16) for line in lines]
    return np.array([w - 65536 if w >= 32768 else w for w in words], dtype=np.int16)


def write_csv(path: str | Path, columns: Mapping[str, Sequence]) -> None:
    if not columns or len({len(v) for v in columns.values()}) != 1:
        raise ValueError("CSV columns must be nonempty and have matching lengths")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(zip(*columns.values()))


def write_json(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
