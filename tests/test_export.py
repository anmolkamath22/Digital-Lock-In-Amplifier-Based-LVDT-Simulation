import re
import numpy as np
import pytest
from lvdt_sim.export import write_hex, read_hex


def test_independent_hex_round_trip(tmp_path):
    a = np.array([0, 1, -1, -2048, 2047, -32768, 32767], dtype=np.int16)
    path = tmp_path / "samples.hex"
    write_hex(path, a)
    lines = path.read_text().splitlines()
    assert all(re.fullmatch("[0-9A-F]{4}", s) for s in lines)
    decoded = []
    for line in lines:
        word = int(line, 16)
        decoded.append(word if word < 2**15 else word - 2**16)
    np.testing.assert_array_equal(a, decoded)
    np.testing.assert_array_equal(a, read_hex(path))
    assert "0800" not in lines
    assert lines[3] == "F800"


@pytest.mark.parametrize("value", [32768, -32769, 1.5])
def test_bad_hex_input(tmp_path, value):
    with pytest.raises(ValueError):
        write_hex(tmp_path / "bad.hex", np.array([value]))
