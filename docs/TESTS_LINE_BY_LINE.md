# Tests: every source line explained

These are verification examples, not the signal generation entry point. Pytest discovers functions beginning test_. tmp_path is a pytest-provided temporary folder. Parametrization runs the same test with multiple inputs. Assertions raise a failure when an expected property is false.

## tests/test_trajectories.py

Checks sampling, every trajectory mode, calibration holds, custom CSV interpolation, and rejection of invalid physical/configuration input.

Source snapshot SHA-256: `b1df2e3dd41c326c9f64fb9d9dea5d5d8ff06850ca8eb7d510b1332ea9bbda8f`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>from dataclasses import replace</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 2 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>import pytest</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>from lvdt_sim.trajectories import generate, time_vector</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code>@pytest.mark.parametrize(&quot;mode&quot;, [&quot;static&quot;, &quot;step&quot;, &quot;sine&quot;, &quot;ramp&quot;])</code> | Runs the next test once for each of four built-in motion modes. |
| 9 | <code>def test_modes(mode):</code> | Defines the generic trajectory test with the selected mode. |
| 10 | <code>    c = Config(trajectory={&quot;mode&quot;: mode})</code> | Creates a default one-second instrument using that mode. |
| 11 | <code>    x = generate(c)</code> | Generates displacement samples. |
| 12 | <code>    assert len(x) == 20000</code> | Requires 20,000 samples. |
| 13 | <code>    np.testing.assert_array_equal(time_vector(c), np.arange(20000) / 20000)</code> | Checks every timestamp exactly equals integer sample index divided by 20,000. |
| 14 | <code>    assert np.min(x) &gt;= -5 and np.max(x) &lt;= 5</code> | Checks generated positions stay inside +/-5 mm. |
| 15 | <code></code> | Blank separator for readability; no operation. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code>def test_calibration_and_step():</code> | Defines calibration and exact step-boundary checks. |
| 18 | <code>    c = Config(duration_s=.06, trajectory={&quot;mode&quot;: &quot;calibration&quot;, &quot;values_mm&quot;: [-2, 0, 2], &quot;hold_windows&quot;: 2})</code> | Builds three positions held two windows each: 1200 samples, or 0.06 seconds. |
| 19 | <code>    np.testing.assert_array_equal(generate(c), np.repeat([-2, 0, 2], 400))</code> | Requires exactly 400 consecutive samples at each position. |
| 20 | <code>    s = generate(Config(trajectory={&quot;mode&quot;: &quot;step&quot;, &quot;step_s&quot;: .5}))</code> | Generates the default -3 to +3 step at 0.5 seconds. |
| 21 | <code>    assert s[9999] == -3 and s[10000] == 3</code> | Checks the sample just before transition is -3 and the transition sample is +3. |
| 22 | <code>    with pytest.raises(ValueError):</code> | Declares the following operation must raise ValueError. |
| 23 | <code>        generate(replace(c, duration_s=.1))</code> | Changes duration to an incompatible length and checks calibration rejects it. |
| 24 | <code></code> | Blank separator for readability; no operation. |
| 25 | <code></code> | Blank separator for readability; no operation. |
| 26 | <code>def test_custom(tmp_path):</code> | Defines a custom-CSV test using pytest's temporary directory. |
| 27 | <code>    path = tmp_path / &quot;motion.csv&quot;</code> | Chooses a CSV path inside that directory. |
| 28 | <code>    path.write_text(&quot;time_s,displacement_mm\n0,-1\n1,1\n&quot;)</code> | Writes two motion endpoints: -1 mm at 0 s, +1 mm at 1 s. |
| 29 | <code>    c = Config(trajectory={&quot;mode&quot;: &quot;custom&quot;, &quot;csv_path&quot;: str(path)})</code> | Configures the custom trajectory with that CSV. |
| 30 | <code>    np.testing.assert_allclose(generate(c), -1 + 2 * time_vector(c))</code> | Checks linear interpolation yields -1+2*t at every sample time. |
| 31 | <code>    path.write_text(&quot;time_s,displacement_mm\n0,0\n0,1\n&quot;)</code> | Replaces the CSV with duplicate timestamps. |
| 32 | <code>    with pytest.raises(ValueError):</code> | Requires the invalid input to raise ValueError. |
| 33 | <code>        generate(c)</code> | Calls the generator to trigger timestamp validation. |
| 34 | <code></code> | Blank separator for readability; no operation. |
| 35 | <code></code> | Blank separator for readability; no operation. |
| 36 | <code>@pytest.mark.parametrize(&quot;trajectory&quot;, [{&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: 6}, {&quot;mode&quot;: &quot;sine&quot;, &quot;amplitude_mm&quot;: 6}, {&quot;mode&quot;: &quot;bogus&quot;}])</code> | Repeats invalid-motion testing for out-of-range constant, out-of-range sine, and unknown mode. |
| 37 | <code>def test_invalid_motion(trajectory):</code> | Defines the invalid-motion test. |
| 38 | <code>    with pytest.raises(ValueError):</code> | Requires a ValueError. |
| 39 | <code>        generate(Config(trajectory=trajectory))</code> | Constructs/runs the specified invalid trajectory. |
| 40 | <code></code> | Blank separator for readability; no operation. |
| 41 | <code></code> | Blank separator for readability; no operation. |
| 42 | <code>@pytest.mark.parametrize(&quot;kwargs&quot;, [{&quot;fs_hz&quot;: 19000}, {&quot;duration_s&quot;: .00001}, {&quot;seed&quot;: -1}, {&quot;noise_std_v&quot;: -1}, {&quot;secondary_null_v&quot;: .1}, {&quot;phase_deg&quot;: float(&quot;nan&quot;)}])</code> | Repeats configuration validation for incoherence, fractional duration, negative seed/noise, invalid winding amplitude, and NaN phase. |
| 43 | <code>def test_invalid_config(kwargs):</code> | Defines the invalid-configuration test. |
| 44 | <code>    with pytest.raises(ValueError):</code> | Requires rejection with ValueError. |
| 45 | <code>        Config(**kwargs)</code> | Unpacks each invalid settings dictionary into the Config constructor. |

## tests/test_sensor.py

Verifies cancellation, polarity, physical winding amplitudes, and symmetric cubic behavior.

Source snapshot SHA-256: `a355dda4b0a7e7b833538fe1c3ecd232b68431c5de01bfc1ad174d7a637ed24e`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>import pytest</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>from lvdt_sim.trajectories import time_vector</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>from lvdt_sim.sensor import simulate</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code>@pytest.mark.parametrize(&quot;position&quot;, [-5, -2, 0, 2, 5])</code> | Runs the linear sensor test at -5, -2, 0, +2, and +5 mm. |
| 9 | <code>def test_linear_identity(position):</code> | Defines the position-parametrized physics test. |
| 10 | <code>    c = Config(duration_s=.01)</code> | Creates one clean 200-sample window. |
| 11 | <code>    t = time_vector(c)</code> | Generates its times. |
| 12 | <code>    s = simulate(t, np.full(t.size, position), c)</code> | Runs the sensor at constant position. |
| 13 | <code>    np.testing.assert_allclose(s.differential_v, .24 * position * np.sin(2*np.pi*1000*t), atol=1e-15)</code> | Checks V1-V2 matches K*x*sin(2*pi*fc*t) to floating precision. |
| 14 | <code>    assert 2 - abs(.24 * position) / 2 &gt; 0</code> | Checks the smaller default secondary peak amplitude remains positive. |
| 15 | <code>    if position:</code> | Only nonzero positions have a meaningful polarity sign. |
| 16 | <code>        assert np.sign(np.dot(s.differential_v, s.primary_v)) == np.sign(position)</code> | Requires correlation with primary to have the same sign as displacement. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code></code> | Blank separator for readability; no operation. |
| 19 | <code>def test_nonlinear_symmetric():</code> | Defines symmetric nonlinear sensor verification. |
| 20 | <code>    c = Config(duration_s=.01, cubic_v_per_mm3=.002, phase_deg=30)</code> | Enables alpha=0.002 V/mm^3 and a 30-degree sensor phase. |
| 21 | <code>    t = time_vector(c)</code> | Creates sample times. |
| 22 | <code>    s = simulate(t, np.full(t.size, 2), c)</code> | Runs the sensor at +2 mm. |
| 23 | <code>    np.testing.assert_allclose(s.differential_v, (.48 + .002*8)*np.sin(2*np.pi*1000*t + np.pi/6), atol=1e-15)</code> | Checks the cubic differential amplitude and phase against the explicit formula. |
| 24 | <code>    np.testing.assert_allclose(s.secondary_1_v + s.secondary_2_v, 4*np.sin(2*np.pi*1000*t + np.pi/6), atol=1e-15)</code> | Checks common secondary sum still equals 2*A0 times the shifted carrier; cubic terms cancel symmetrically. |

## tests/test_noise.py

Checks Gaussian statistics, deterministic streams, and each additive voltage source independently.

Source snapshot SHA-256: `ea85a5bb701afd4817bb829f474a094b4e16a4c9bac6d51944a4528f0df26beb`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>import pytest</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>from lvdt_sim.noise import components, gaussian</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code></code> | Blank separator for readability; no operation. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code>def test_gaussian_statistics_and_streams():</code> | Defines statistical and reproducibility testing. |
| 8 | <code>    a = gaussian(500000, .2, 42)</code> | Draws 500,000 samples at sigma=0.2 V. |
| 9 | <code>    assert abs(np.mean(a)) &lt; .001</code> | Requires sampled noise mean near zero. |
| 10 | <code>    assert abs(np.var(a) - .04) &lt; .0003</code> | Requires variance near sigma^2=0.04 V^2. |
| 11 | <code>    np.testing.assert_array_equal(a, gaussian(500000, .2, 42))</code> | Requires identical seed/stream to reproduce every sample exactly. |
| 12 | <code>    assert not np.array_equal(a, gaussian(500000, .2, 42, 1))</code> | Requires a different stream ID to produce a different realization. |
| 13 | <code></code> | Blank separator for readability; no operation. |
| 14 | <code></code> | Blank separator for readability; no operation. |
| 15 | <code>def test_components():</code> | Defines deterministic additive-component testing. |
| 16 | <code>    t = np.arange(10000) / 20000</code> | Creates half a second of sampled times. |
| 17 | <code>    c = Config(hum_peak_v=.3, hum_phase_deg=17, dc_offset_v=.2,</code> | Configures hum amplitude/phase and DC voltage. |
| 18 | <code>               interference_peak_v=.4, interference_hz=950, interference_phase_deg=21,</code> | Also configures a 950 Hz narrowband interferer. |
| 19 | <code>               drift_peak_v=.1, drift_hz=.2)</code> | Also configures slow drift. |
| 20 | <code>    v = components(t, c)</code> | Generates every component separately. |
| 21 | <code>    np.testing.assert_array_equal(v[&quot;gaussian_v&quot;], 0)</code> | Requires the disabled Gaussian component to be zero. |
| 22 | <code>    np.testing.assert_allclose(v[&quot;hum_v&quot;], .3*np.sin(2*np.pi*50*t + np.deg2rad(17)))</code> | Compares hum against its explicit sine equation. |
| 23 | <code>    np.testing.assert_allclose(v[&quot;dc_v&quot;], .2)</code> | Compares DC against the expected constant voltage. |
| 24 | <code>    np.testing.assert_allclose(v[&quot;interference_v&quot;], .4*np.sin(2*np.pi*950*t + np.deg2rad(21)))</code> | Compares narrowband interference against its frequency/amplitude/phase equation. |
| 25 | <code>    np.testing.assert_allclose(v[&quot;drift_v&quot;], .1*np.sin(2*np.pi*.2*t))</code> | Compares drift against its slow sinusoidal equation. |
| 26 | <code></code> | Blank separator for readability; no operation. |
| 27 | <code></code> | Blank separator for readability; no operation. |
| 28 | <code>def test_invalid_noise():</code> | Defines rejection of invalid Gaussian input. |
| 29 | <code>    with pytest.raises(ValueError):</code> | Requires a ValueError. |
| 30 | <code>        gaussian(10, -.1, 42)</code> | Passes negative standard deviation to trigger rejection. |

## tests/test_adc.py

Checks code limits, ties-to-even rounding, two definitions of clipping, and half-LSB error bounds.

Source snapshot SHA-256: `2bdbc65f61b65f7dc78769a18320f068986e5f02da3635f158fa68538c8b3ae3`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>import pytest</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>from lvdt_sim.adc import quantize, codes_to_voltage</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code></code> | Blank separator for readability; no operation. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code>def test_extremes_and_rounding():</code> | Defines the quantizer boundary/rounding test. |
| 8 | <code>    c = Config()</code> | Selects the default ADC configuration. |
| 9 | <code>    lsb = 2.5 / 2048</code> | Calculates one ADC code's voltage, 2.5/2048 V. |
| 10 | <code>    a = quantize(np.array([0, lsb, -lsb, 2.5, -2.5, 3, -3, .5*lsb, 1.5*lsb, -.5*lsb, -1.5*lsb]), c)</code> | Quantizes zero, +/-one code, both rails, overrange voltages, and positive/negative half-step rounding ties. |
| 11 | <code>    np.testing.assert_array_equal(a.codes, [0, 1, -1, 2047, -2048, 2047, -2048, 0, 2, 0, -2])</code> | Requires exact signed integer outputs, including asymmetric rails and ties-to-even examples. |
| 12 | <code>    assert a.codes.dtype == np.int16</code> | Checks the storage dtype is signed int16. |
| 13 | <code>    assert a.clipped_count == 3</code> | Checks saturation count is three: +full scale and the two overrange values. |
| 14 | <code>    assert np.count_nonzero(a.analog_overrange_mask) == 2</code> | Checks only the +/-3 V inputs count as physical analog overrange. |
| 15 | <code>    assert a.clipped_percent == 100*3/11</code> | Checks clipping percentage against the known sample count. |
| 16 | <code>    np.testing.assert_allclose(codes_to_voltage(a.codes, c), a.codes * lsb)</code> | Verifies inverse scaling reconstructs code*LSB. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code></code> | Blank separator for readability; no operation. |
| 19 | <code>def test_quantization_bound():</code> | Defines an extensive quantization error-bound test. |
| 20 | <code>    c = Config()</code> | Creates default ADC settings. |
| 21 | <code>    v = np.linspace(-3, 3, 100001)</code> | Samples a fine voltage sweep from -3 to +3 V. |
| 22 | <code>    a = quantize(v, c)</code> | Quantizes the sweep. |
| 23 | <code>    assert np.max(np.abs(a.reconstructed_v[~a.clipped_mask] - v[~a.clipped_mask])) &lt;= 2.5/4096 + 1e-15</code> | Checks absolute reconstruction error on nonclipped samples is at most half an LSB, plus floating tolerance. |
| 24 | <code></code> | Blank separator for readability; no operation. |
| 25 | <code></code> | Blank separator for readability; no operation. |
| 26 | <code>def test_invalid_adc():</code> | Defines invalid-input tests. |
| 27 | <code>    with pytest.raises(ValueError):</code> | Requires a ValueError. |
| 28 | <code>        quantize(np.array([np.nan]), Config())</code> | Checks ADC rejects NaN voltage. |
| 29 | <code>    with pytest.raises(ValueError):</code> | Requires another ValueError. |
| 30 | <code>        codes_to_voltage(np.array([2048]), Config())</code> | Checks inverse scaling rejects +2048, which is outside signed 12-bit numerical range. |

## tests/test_reference.py

A compact executable description of reference LUT size, sign, amplitude, rounding precision, and continuous indexing.

Source snapshot SHA-256: `146b305947fcc14924aa655cc9fcda628ef0f081393b48da532379355604153d`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>from lvdt_sim.reference import sine_lut, reference_samples, Q_SCALE</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 3 | <code></code> | Blank separator for readability; no operation. |
| 4 | <code></code> | Blank separator for readability; no operation. |
| 5 | <code>def test_lut_contract():</code> | Defines the LUT contract test. |
| 6 | <code>    r = sine_lut()</code> | Generates the default rounded sine table. |
| 7 | <code>    assert len(r) == 20 and r[0] == 0 and r[10] == 0</code> | Requires exactly 20 entries and zeros at phase indices 0 and 10. |
| 8 | <code>    assert np.all(r[1:10] &gt; 0) and np.all(r[11:] &lt; 0)</code> | Requires positive samples in the first half-cycle and negative in the second. |
| 9 | <code>    assert r[5] == 16384 and r[15] == -16384</code> | Requires positive/negative peaks at +/-16384. |
| 10 | <code>    np.testing.assert_array_equal(r[1:10], -r[11:])</code> | Checks half-cycle antisymmetry for corresponding nonzero entries. |
| 11 | <code>    np.testing.assert_allclose(r / Q_SCALE, np.sin(2*np.pi*np.arange(20)/20), atol=.5/Q_SCALE)</code> | Divides by Q scale and checks sine approximation error stays within half a Q-code. |
| 12 | <code>    np.testing.assert_array_equal(reference_samples(47, start_sample=13), np.tile(r, 3)[13:60])</code> | Checks a 47-sample reference beginning at global sample 13 matches the equivalent slice from three repeated LUTs. |

## tests/test_export.py

Independent HEX decoding catches signed encoding, order, width, and truncation mistakes.

Source snapshot SHA-256: `64f3bbfdaeb250e9b4e40f0792975912a06dfd1c2f53bd6ab2a08ea562016974`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import re</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>import pytest</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from lvdt_sim.export import write_hex, read_hex</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code></code> | Blank separator for readability; no operation. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code>def test_independent_hex_round_trip(tmp_path):</code> | Defines signed HEX round-trip testing in a temporary directory. |
| 8 | <code>    a = np.array([0, 1, -1, -2048, 2047, -32768, 32767], dtype=np.int16)</code> | Creates ADC and general signed-16 boundary examples. |
| 9 | <code>    path = tmp_path / &quot;samples.hex&quot;</code> | Chooses the vector filename. |
| 10 | <code>    write_hex(path, a)</code> | Writes the signed values to HEX. |
| 11 | <code>    lines = path.read_text().splitlines()</code> | Reads raw text independently. |
| 12 | <code>    assert all(re.fullmatch(&quot;[0-9A-F]{4}&quot;, s) for s in lines)</code> | Requires four uppercase HEX digits on every line. |
| 13 | <code>    decoded = []</code> | Starts an independent decoded-value list. |
| 14 | <code>    for line in lines:</code> | Loops over raw words in original order. |
| 15 | <code>        word = int(line, 16)</code> | Parses each word as unsigned base 16. |
| 16 | <code>        decoded.append(word if word &lt; 2**15 else word - 2**16)</code> | Converts bit-15-set words to signed values by subtracting 65536. |
| 17 | <code>    np.testing.assert_array_equal(a, decoded)</code> | Checks independent decoding exactly reproduces the input order/values. |
| 18 | <code>    np.testing.assert_array_equal(a, read_hex(path))</code> | Checks the package reader agrees too. |
| 19 | <code>    assert &quot;0800&quot; not in lines</code> | Checks these values never emit the invalid positive default ADC code 0800. |
| 20 | <code>    assert lines[3] == &quot;F800&quot;</code> | Checks -2048 is sign-extended to F800. |
| 21 | <code></code> | Blank separator for readability; no operation. |
| 22 | <code></code> | Blank separator for readability; no operation. |
| 23 | <code>@pytest.mark.parametrize(&quot;value&quot;, [32768, -32769, 1.5])</code> | Repeats rejection testing for values above/below signed-16 range and a fractional input. |
| 24 | <code>def test_bad_hex_input(tmp_path, value):</code> | Defines invalid HEX writer input testing. |
| 25 | <code>    with pytest.raises(ValueError):</code> | Requires a ValueError. |
| 26 | <code>        write_hex(tmp_path / &quot;bad.hex&quot;, np.array([value]))</code> | Tries exporting the invalid value; it must not truncate or wrap. |

## tests/test_pipeline.py

End-to-end tests exercise export contracts, independent runs, all standard scenarios, calibration, and byte-for-byte reproducibility.

Source snapshot SHA-256: `fafc2b5f0d6487c267b44629ada491b3060964298f6e51c64156ec32a00c946e`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import csv</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>import json</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>from lvdt_sim.pipeline import run, export_simulation, standard_scenarios</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from lvdt_sim.export import read_hex, GROUND_TRUTH_COLUMNS, EXPECTED_COLUMNS</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code>from lvdt_sim.metrics import calibration</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code></code> | Blank separator for readability; no operation. |
| 10 | <code>def test_exports_and_independent_streams(tmp_path):</code> | Defines a complete pipeline/export test with independent streams. |
| 11 | <code>    c = Config(duration_s=.01995, noise_std_v=.1)</code> | Chooses 399 samples and Gaussian noise so there is one result and a 199-sample tail. |
| 12 | <code>    a = run(c, 7)</code> | Runs stream ID 7. |
| 13 | <code>    run(c, 8)</code> | Runs a different stream between repetitions to expose accidental global RNG contamination. |
| 14 | <code>    b = run(c, 7)</code> | Runs stream ID 7 again. |
| 15 | <code>    np.testing.assert_array_equal(a.adc.codes, b.adc.codes)</code> | Requires its ADC codes to reproduce exactly. |
| 16 | <code>    paths = export_simulation(a, tmp_path, &quot;test&quot;)</code> | Exports the first run into a temporary scenario. |
| 17 | <code>    from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 18 | <code>    v, g = Path(paths[&quot;vectors&quot;]), Path(paths[&quot;ground_truth&quot;])</code> | Converts the returned vector/truth directory strings into Paths. |
| 19 | <code>    np.testing.assert_array_equal(read_hex(v / &quot;adc_samples.hex&quot;), a.adc.codes)</code> | Checks written/decoded ADC HEX exactly matches the in-memory codes. |
| 20 | <code>    meta = json.loads((v / &quot;metadata.json&quot;).read_text())</code> | Reads metadata JSON. |
| 21 | <code>    assert meta[&quot;number_of_samples&quot;] == 399 and meta[&quot;number_of_windows&quot;] == 1</code> | Checks 399 samples produce one completed result. |
| 22 | <code>    assert meta[&quot;discarded_trailing_samples&quot;] == 199</code> | Checks the 199 incomplete trailing samples are explicitly reported. |
| 23 | <code>    with (g / &quot;ground_truth.csv&quot;).open() as handle:</code> | Opens the exported physical CSV. |
| 24 | <code>        rows = list(csv.reader(handle))</code> | Reads its rows. |
| 25 | <code>    assert rows[0] == GROUND_TRUTH_COLUMNS and len(rows) == 400</code> | Requires exact header ordering and 399 sample rows plus one header. |
| 26 | <code>    with (v / &quot;expected_results.csv&quot;).open() as handle:</code> | Opens expected results CSV. |
| 27 | <code>        expected = list(csv.DictReader(handle))</code> | Reads result rows keyed by their headers. |
| 28 | <code>    assert list(expected[0]) == EXPECTED_COLUMNS</code> | Checks exact expected-results column ordering. |
| 29 | <code>    assert int(expected[0][&quot;end_sample&quot;]) == 199</code> | Checks inclusive end_sample=199 for the first complete result. |
| 30 | <code>    assert int(expected[0][&quot;expected_accumulator&quot;]) == a.fixed.accumulator[0]</code> | Checks exported accumulator remains exactly the original integer. |
| 31 | <code></code> | Blank separator for readability; no operation. |
| 32 | <code></code> | Blank separator for readability; no operation. |
| 33 | <code>def test_all_standard_scenarios_and_calibration():</code> | Defines a test running every standard scenario. |
| 34 | <code>    configs = standard_scenarios()</code> | Gets the complete scenario catalog. |
| 35 | <code>    assert len(configs) == 10</code> | Requires ten standard scenarios. |
| 36 | <code>    sims = {name: run(c, i) for i, (name, c) in enumerate(configs.items())}</code> | Runs each independently with a distinct stream ID. |
| 37 | <code>    s = sims[&quot;calibration&quot;]</code> | Selects calibration output. |
| 38 | <code>    metrics = calibration(s.true_window_mean_mm, s.fixed.displacement_mm, .24)</code> | Computes calibration regression/accuracy statistics. |
| 39 | <code>    assert metrics[&quot;r_squared&quot;] &gt; .999999</code> | Requires R-squared above 0.999999. |
| 40 | <code>    assert metrics[&quot;max_absolute_error_mm&quot;] &lt; .003</code> | Requires maximum error below 0.003 mm. |
| 41 | <code>    assert abs(metrics[&quot;estimated_sensitivity_v_per_mm&quot;] - .24) &lt; .0001</code> | Requires fitted electrical sensitivity close to 0.24 Vpeak/mm. |
| 42 | <code>    assert sims[&quot;adc_overrange&quot;].adc.clipped_count &gt; 0</code> | Requires the intentionally overrange scenario to report clipping. |
| 43 | <code>    assert sims[&quot;step&quot;].fixed.displacement_mm[49] &lt; 0</code> | Checks the last complete pre-step window remains negative. |
| 44 | <code>    assert sims[&quot;step&quot;].fixed.displacement_mm[50] &gt; 0</code> | Checks the first full post-step window becomes positive. |
| 45 | <code></code> | Blank separator for readability; no operation. |
| 46 | <code></code> | Blank separator for readability; no operation. |
| 47 | <code>def test_byte_reproducibility(tmp_path):</code> | Defines byte-for-byte deterministic export verification. |
| 48 | <code>    c = Config(duration_s=.02, noise_std_v=.4)</code> | Creates a short noisy run. |
| 49 | <code>    export_simulation(run(c, 4), tmp_path / &quot;first&quot;, &quot;seeded&quot;)</code> | Exports stream ID 4 under a first independent output root. |
| 50 | <code>    export_simulation(run(c, 4), tmp_path / &quot;second&quot;, &quot;seeded&quot;)</code> | Repeats the same run/export under a second root. |
| 51 | <code>    for path in (tmp_path / &quot;first&quot;).rglob(&quot;*&quot;):</code> | Walks all generated paths beneath the first root. |
| 52 | <code>        if path.is_file():</code> | Selects files rather than directories. |
| 53 | <code>            assert path.read_bytes() == (tmp_path / &quot;second&quot; / path.relative_to(tmp_path / &quot;first&quot;)).read_bytes()</code> | Requires every corresponding file to have identical bytes, including metadata/CSV formatting. |

## tests/test_lockin.py

Tests the numerical specification your friend's HDL must meet. The valid-gap test describes accepted-sample behavior in Python; it does not execute RTL or prove pipeline timing.

Source snapshot SHA-256: `1829d6a047237113e45725cd9152d00db87d7f2504de0df74e0543c7345a6a6d`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 2 | <code>import pytest</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 3 | <code>from lvdt_sim.config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>from lvdt_sim.pipeline import run</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>from lvdt_sim.lockin_reference import fixed, floating</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from lvdt_sim.reference import sine_lut</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code>@pytest.mark.parametrize(&quot;position&quot;, [0, 2, -2])</code> | Runs signed baseline testing at zero and both displacement directions. |
| 10 | <code>def test_static_signed_estimates(position):</code> | Defines the static-position detector test. |
| 11 | <code>    s = run(Config(duration_s=.02, trajectory={&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: position}))</code> | Runs two clean measurement windows at the selected position. |
| 12 | <code>    np.testing.assert_allclose(s.floating.displacement_mm, position, atol=1e-12)</code> | Requires floating analog correlation to recover position within numerical precision. |
| 13 | <code>    np.testing.assert_allclose(s.fixed.displacement_mm, position, atol=.003)</code> | Allows small ADC/LUT quantization error in the fixed path. |
| 14 | <code>    if not position:</code> | Selects the null case. |
| 15 | <code>        np.testing.assert_array_equal(s.fixed.accumulator, 0)</code> | Requires its integer sums to be exactly zero. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code>@pytest.mark.parametrize(&quot;length,outputs&quot;, [(199, 0), (200, 1), (399, 1), (400, 2)])</code> | Tests 199, 200, 399, and 400 samples with expected zero/one/one/two completed outputs. |
| 19 | <code>def test_window_boundaries(length, outputs):</code> | Defines incomplete-window behavior testing. |
| 20 | <code>    result = fixed(np.ones(length, dtype=np.int16), Config())</code> | Processes an integer input vector of the specified length. |
| 21 | <code>    assert len(result.accumulator) == outputs</code> | Checks completed-result count. |
| 22 | <code>    np.testing.assert_array_equal(result.end_sample, np.arange(outputs)*200+199)</code> | Checks inclusive output boundaries occur at 199, 399, and so on. |
| 23 | <code></code> | Blank separator for readability; no operation. |
| 24 | <code></code> | Blank separator for readability; no operation. |
| 25 | <code>def test_exact_independent_integer_loop():</code> | Defines exact agreement with an independent scalar integer reference. |
| 26 | <code>    q = np.random.default_rng(112).integers(-2048, 2048, 1400, dtype=np.int16)</code> | Draws 1400 deterministic signed ADC codes. |
| 27 | <code>    lut = sine_lut()</code> | Builds the reference table. |
| 28 | <code>    expected = [sum(int(q[n])*int(lut[n % 20]) for n in range(a, a+200)) for a in range(0, 1400, 200)]</code> | Calculates seven window sums with Python ints and continuous modulo reference phase. |
| 29 | <code>    np.testing.assert_array_equal(fixed(q, Config()).accumulator, expected)</code> | Requires exact accumulator agreement with the vectorized fixed implementation. |
| 30 | <code></code> | Blank separator for readability; no operation. |
| 31 | <code></code> | Blank separator for readability; no operation. |
| 32 | <code>def test_continuous_phase_noncycle_windows():</code> | Defines global reference-phase testing when windows do not contain an integer carrier-cycle count. |
| 33 | <code>    c = Config(window_samples=213)</code> | Uses 213-sample windows, which must not reset phase each window. |
| 34 | <code>    q = np.arange(852, dtype=np.int16)</code> | Creates four such windows of valid ADC codes. |
| 35 | <code>    full = fixed(q, c)</code> | Processes the full sequence. |
| 36 | <code>    second = fixed(q[213:], c, start_sample=213)</code> | Processes the sequence after the first window with global start_sample=213. |
| 37 | <code>    np.testing.assert_array_equal(full.accumulator[1:], second.accumulator)</code> | Requires chunked and full-stream integer sums to agree after the first window. |
| 38 | <code>    np.testing.assert_array_equal(full.center_time_s[1:], second.center_time_s)</code> | Requires chunked timestamps to preserve their global positions. |
| 39 | <code>    assert full.center_time_s[0] == 212/(2*20000)</code> | Checks first center time is halfway between index 0 and 212. |
| 40 | <code></code> | Blank separator for readability; no operation. |
| 41 | <code></code> | Blank separator for readability; no operation. |
| 42 | <code>@pytest.mark.parametrize(&quot;phase&quot;, [0, 15, 30, 45, 90])</code> | Repeats phase testing at five sensor phases. |
| 43 | <code>def test_phase_cosine(phase):</code> | Defines the cosine-response test. |
| 44 | <code>    s = run(Config(duration_s=.01, phase_deg=phase))</code> | Runs one clean +2 mm window with the selected phase. |
| 45 | <code>    np.testing.assert_allclose(s.floating.displacement_mm, 2*np.cos(np.deg2rad(phase)), atol=1e-12)</code> | Requires floating response to equal 2*cos(phi). |
| 46 | <code>    np.testing.assert_allclose(s.fixed.displacement_mm, 2*np.cos(np.deg2rad(phase)), atol=.003)</code> | Requires fixed response near that same value with quantization tolerance. |
| 47 | <code></code> | Blank separator for readability; no operation. |
| 48 | <code></code> | Blank separator for readability; no operation. |
| 49 | <code>def test_dc_and_same_frequency():</code> | Defines complete-cycle DC rejection and coherent-interference limitation testing. |
| 50 | <code>    dc = run(Config(duration_s=.02, dc_offset_v=.6))</code> | Runs +2 mm with a 0.6 V DC measurement offset. |
| 51 | <code>    np.testing.assert_allclose(dc.floating.displacement_mm, 2, atol=1e-12)</code> | Requires floating correlation to retain +2 mm despite ideal complete-cycle DC. |
| 52 | <code>    tone = run(Config(duration_s=.02, interference_peak_v=.24, interference_hz=1000))</code> | Runs +2 mm with a 0.24 Vpeak same-frequency, same-phase added tone. |
| 53 | <code>    np.testing.assert_allclose(tone.floating.displacement_mm, 3, atol=1e-12)</code> | Requires +3 mm result: the coherent added tone is indistinguishable from +1 mm displacement. |
| 54 | <code></code> | Blank separator for readability; no operation. |
| 55 | <code></code> | Blank separator for readability; no operation. |
| 56 | <code>@pytest.mark.parametrize(&quot;frequency&quot;, [400, 950, 1000, 1050, 1600])</code> | Repeats finite-window projection checks at five interferer frequencies. |
| 57 | <code>def test_tone_projection(frequency):</code> | Defines the frequency-parametrized test. |
| 58 | <code>    c = Config(duration_s=.01, interference_hz=frequency, interference_peak_v=.24)</code> | Creates one 200-sample observation with the selected interferer. |
| 59 | <code>    s = run(c)</code> | Runs the physical/measurement pipeline. |
| 60 | <code>    # Analytic finite rectangular-window projection (not a universal rejection claim).</code> | Explanatory comment for the following code; Python does not execute it. |
| 61 | <code>    n = np.arange(200)</code> | Creates independent within-window sample indices. |
| 62 | <code>    projection = 2/200*np.sum(.24*np.sin(2*np.pi*frequency*n/20000)*np.sin(2*np.pi*n/20))/.24</code> | Calculates the actual finite-window interference projection, including voltage-to-mm scaling. |
| 63 | <code>    np.testing.assert_allclose(s.floating.displacement_mm, 2+projection, atol=1e-12)</code> | Requires the detector result to equal true position plus that projection. |
| 64 | <code></code> | Blank separator for readability; no operation. |
| 65 | <code></code> | Blank separator for readability; no operation. |
| 66 | <code>def test_sine_weighted_dynamic_truth():</code> | Defines dynamic-motion interpretation testing. |
| 67 | <code>    c = Config(trajectory={&quot;mode&quot;: &quot;sine&quot;, &quot;frequency_hz&quot;: 2, &quot;amplitude_mm&quot;: 3})</code> | Configures a 3 mm, 2 Hz mechanical sine motion. |
| 68 | <code>    s = run(c)</code> | Runs the pipeline. |
| 69 | <code>    ref = np.sin(2*np.pi*np.arange(c.sample_count)/20)</code> | Generates an independent baseline carrier reference. |
| 70 | <code>    weighted = (2*s.displacement_mm*ref**2).reshape(-1, 200).mean(axis=1)</code> | Calculates per-window sine-squared-weighted position, not merely instantaneous position. |
| 71 | <code>    np.testing.assert_allclose(s.floating.displacement_mm, weighted, atol=2e-12)</code> | Requires floating demodulation to match that weighted truth. |
| 72 | <code>    assert np.max(np.abs(s.fixed.displacement_mm - s.true_window_mean_mm)) &lt; .01</code> | Checks fixed estimates remain within 0.01 mm of arithmetic means for this slow example. |
| 73 | <code></code> | Blank separator for readability; no operation. |
| 74 | <code></code> | Blank separator for readability; no operation. |
| 75 | <code>def test_200th_sample_included():</code> | Defines a targeted final-product inclusion test. |
| 76 | <code>    q = np.zeros(400, dtype=np.int16)</code> | Creates two zero-filled windows. |
| 77 | <code>    q[199] = 123</code> | Makes only the 200th accepted sample nonzero. |
| 78 | <code>    result = fixed(q, Config())</code> | Runs integer demodulation. |
| 79 | <code>    assert result.accumulator[0] == 123*int(sine_lut()[19])</code> | Requires the first sum to include sample 199 times LUT index 19. |
| 80 | <code>    assert result.accumulator[1] == 0</code> | Requires the second window sum to remain zero. |
| 81 | <code></code> | Blank separator for readability; no operation. |
| 82 | <code></code> | Blank separator for readability; no operation. |
| 83 | <code>def test_sample_valid_gaps_and_reset_contract():</code> | Defines a behavioral model of accepted samples, inserted gaps, and independent reruns. |
| 84 | <code>    # Independent clocked behavioral checker: stalled clocks never consume data.</code> | Explanatory comment for the following code; Python does not execute it. |
| 85 | <code>    rng = np.random.default_rng(5)</code> | Creates reproducible gap/code randomness. |
| 86 | <code>    q = rng.integers(-2048, 2048, 400, dtype=np.int16)</code> | Creates 400 valid signed codes. |
| 87 | <code>    lut = [int(v) for v in sine_lut()]</code> | Promotes coefficients to Python ints. |
| 88 | <code>    accumulator, count, phase = 0, 0, 0</code> | Initializes independent accumulator, accepted count, and phase. |
| 89 | <code>    outputs = []</code> | Starts completed outputs. |
| 90 | <code>    for value in q:</code> | Processes each real accepted ADC value. |
| 91 | <code>        for _ in range(int(rng.integers(0, 7))):</code> | Inserts zero to six simulated invalid clock opportunities before accepting this value. |
| 92 | <code>            state_before = (accumulator, count, phase)</code> | Records the model state before a gap. |
| 93 | <code>            sample_valid = False</code> | Declares that simulated clock invalid. |
| 94 | <code>            if sample_valid:</code> | Would enter this branch only if the invalid flag were unexpectedly true. |
| 95 | <code>                raise AssertionError(&quot;stall unexpectedly accepted&quot;)</code> | Raises if the gap were incorrectly marked accepted. |
| 96 | <code>            assert state_before == (accumulator, count, phase)</code> | Checks the local model's state remains unchanged during a gap; this is not an actual RTL stall test. |
| 97 | <code>        accumulator += int(value) * lut[phase]</code> | Accepts the next real value and adds its signed product. |
| 98 | <code>        phase = (phase+1) % 20</code> | Advances reference phase modulo 20 exactly once per real accepted sample. |
| 99 | <code>        count += 1</code> | Advances accepted count. |
| 100 | <code>        if count == 200:</code> | Detects completion of a 200-sample measurement. |
| 101 | <code>            outputs.append(accumulator)</code> | Latches the sum including that final sample. |
| 102 | <code>            accumulator, count = 0, 0</code> | Clears running sum/count for the next window; does not reset phase. |
| 103 | <code>    np.testing.assert_array_equal(outputs, fixed(q, Config()).accumulator)</code> | Requires the behavioral model outputs to match the fixed batch reference. |
| 104 | <code>    # A fresh independent stream starts with phase 0, regardless of prior tail.</code> | Explanatory comment for the following code; Python does not execute it. |
| 105 | <code>    fixed(q[:213], Config())</code> | Calls the stateless detector on a partial-length independent stream. |
| 106 | <code>    np.testing.assert_array_equal(fixed(q, Config()).accumulator, outputs)</code> | Checks a subsequent independent full call still starts clean and matches previous expected outputs. |

