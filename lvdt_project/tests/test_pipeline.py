import csv
import json
import numpy as np
from lvdt_sim.config import Config
from lvdt_sim.pipeline import run, export_simulation, standard_scenarios
from lvdt_sim.export import read_hex, GROUND_TRUTH_COLUMNS, EXPECTED_COLUMNS
from lvdt_sim.metrics import calibration


def test_exports_and_independent_streams(tmp_path):
    c = Config(duration_s=.01995, noise_std_v=.1)
    a = run(c, 7)
    run(c, 8)
    b = run(c, 7)
    np.testing.assert_array_equal(a.adc.codes, b.adc.codes)
    paths = export_simulation(a, tmp_path, "test")
    from pathlib import Path
    v, g = Path(paths["vectors"]), Path(paths["ground_truth"])
    np.testing.assert_array_equal(read_hex(v / "adc_samples.hex"), a.adc.codes)
    meta = json.loads((v / "metadata.json").read_text())
    assert meta["number_of_samples"] == 399 and meta["number_of_windows"] == 1
    assert meta["discarded_trailing_samples"] == 199
    with (g / "ground_truth.csv").open() as handle:
        rows = list(csv.reader(handle))
    assert rows[0] == GROUND_TRUTH_COLUMNS and len(rows) == 400
    with (v / "expected_results.csv").open() as handle:
        expected = list(csv.DictReader(handle))
    assert list(expected[0]) == EXPECTED_COLUMNS
    assert int(expected[0]["end_sample"]) == 199
    assert int(expected[0]["expected_accumulator"]) == a.fixed.accumulator[0]


def test_all_standard_scenarios_and_calibration():
    configs = standard_scenarios()
    assert len(configs) == 10
    sims = {name: run(c, i) for i, (name, c) in enumerate(configs.items())}
    s = sims["calibration"]
    metrics = calibration(s.true_window_mean_mm, s.fixed.displacement_mm, .24)
    assert metrics["r_squared"] > .999999
    assert metrics["max_absolute_error_mm"] < .003
    assert abs(metrics["estimated_sensitivity_v_per_mm"] - .24) < .0001
    assert sims["adc_overrange"].adc.clipped_count > 0
    assert sims["step"].fixed.displacement_mm[49] < 0
    assert sims["step"].fixed.displacement_mm[50] > 0


def test_byte_reproducibility(tmp_path):
    c = Config(duration_s=.02, noise_std_v=.4)
    export_simulation(run(c, 4), tmp_path / "first", "seeded")
    export_simulation(run(c, 4), tmp_path / "second", "seeded")
    for path in (tmp_path / "first").rglob("*"):
        if path.is_file():
            assert path.read_bytes() == (tmp_path / "second" / path.relative_to(tmp_path / "first")).read_bytes()
