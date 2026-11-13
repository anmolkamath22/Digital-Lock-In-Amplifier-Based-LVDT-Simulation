# Digital Lock-In Amplifier for LVDT Displacement Sensing

This project takes an LVDT (Linear Variable Differential Transformer) displacement sensor from
physics to hardware. **Python** models the sensor, noise and a 12-bit ADC, and exports bit-exact
test vectors. **Verilog** implements a digital lock-in amplifier (sine-reference correlator plus a
200-sample integrator). A **web dashboard** lets you tune the signal, run the real RTL in
Icarus Verilog, and read the displacement, magnitude and phase angle. Every Verilog accumulator is
checked against the Python golden model, bit for bit.

> Teaching model: the parameters describe a chosen model, not a commercial sensor.

## Features

- Physical LVDT model with static, step, sine, ramp and calibration motion, a sensor phase error
  and cubic nonlinearity
- Tunable impairments: Gaussian noise, mains hum, DC offset, a tone interferer and baseline drift
- 12-bit ADC with saturation, and a 20-entry Q1.14 sine LUT exported as `$readmemh` HEX
- Verilog lock-in (`lockin_top.v`) simulated with Icarus Verilog and compared with exact Python sums
- I/Q demodulation: the same RTL runs once with a sine LUT and once with a cosine LUT, giving
  **magnitude √(I²+Q²)** and **phase angle atan2(Q, I)** for each window
- Dashboard charts: winding signals, ADC codes, spectrum, displacement, magnitude, phase and error,
  plus a downloadable vector bundle
- 58 unit tests, numerical validation (Monte Carlo, calibration, phase) and an export audit

## Architecture

```text
 ┌───────────────────────── Browser (web/static) ─────────────────────────┐
 │ index.html + app.js + Chart.js                                         │
 │ sliders / presets → ① Generate → ② Run Verilog → results and charts    │
 └──────────────┬────────────────────────────────────────▲────────────────┘
                │ JSON (fetch)                           │ JSON
 ┌──────────────▼────────── Flask backend (web/app.py) ──┴────────────────┐
 │ POST /api/generate     POST /api/simulate/<run>     GET /api/download  │
 └──────┬──────────────────────────────┬──────────────────────────────────┘
        │                              │
 ┌──────▼──────── Python model ──┐  ┌──▼──────── web/hdl_runner.py ─────────┐
 │ src/lvdt_sim                  │  │ stage HEX files → data/               │
 │ trajectory → sensor → noise   │  │ iverilog tb_lockin.v lockin_top.v     │
 │ → 12-bit ADC → golden lock-in │─▶│ vvp  (I: sine LUT, Q: cosine LUT)     │
 │ exports adc_samples.hex,      │  │ fallback: xsim → Python RTL model     │
 │ reference_lut.hex,            │  └──┬────────────────────────────────────┘
 │ expected_results.csv          │     │ bit-exact compare; → V, mm, |V|, φ
 └───────────────────────────────┘     ▼
                          ┌──────── hdl/ (Verilog) ─────────┐
                          │ rtl/lockin_top.v  16×16 MAC,    │
                          │  40-bit acc, 200-sample window  │
                          │ sim/tb_lockin.v   testbench     │
                          └─────────────────────────────────┘
```

Signal chain:

```text
x(t) → LVDT  D = Kx + αx³ → + noise/hum/offset/tone/drift → ADC q = clip(rint(v·2048/2.5))
     → Verilog  S = Σ q[n]·LUT[n mod 20] over 200 samples → x = 2S/(200·16384)·(2.5/2048)/K
```

| Layer | Technology |
|---|---|
| Simulation | Python 3.11+, NumPy |
| Plots / tests | Matplotlib, pytest |
| Hardware | Verilog-2005, Icarus Verilog 12/13 (Vivado xsim also supported) |
| Web backend | Flask, served by Waitress |
| Web frontend | HTML, CSS, vanilla JavaScript, Chart.js 4 (CDN) |

## Repository structure

```text
.
├── src/lvdt_sim/          # Python package: config, trajectories, sensor, noise, adc,
│                          # reference LUT, lock-in reference, metrics, export, pipeline
├── scripts/               # CLI: generate scenarios/vectors, validation, plots, audit
├── tests/                 # pytest suite
├── configs/               # JSON experiment configs (baseline, noisy, calibration, dynamic)
├── hdl/
│   ├── rtl/lockin_top.v   # lock-in datapath (unchanged from the Vivado project)
│   └── sim/tb_lockin.v    # testbench with `ADC_HEX` / `NUM_SAMPLES` macros
├── web/
│   ├── app.py             # Flask server and REST API
│   ├── hdl_runner.py      # runs iverilog/xsim (or the Python RTL model), parses results
│   └── static/            # index.html, app.js
├── output/
│   ├── vectors/<scenario>/      # adc_samples.hex, reference_lut.hex, expected_results.csv, metadata.json
│   ├── ground_truth/<scenario>/ # ground_truth.csv
│   ├── diagnostics/             # 8 PNG plots
│   ├── reports/                 # validation and audit reports
│   └── web_runs/                # per-run dashboard output (git-ignored)
├── requirements.txt
└── pyproject.toml
```

## Install

### 1. Python environment

```powershell
git clone https://github.com/anmolkamath22/Digital-Lock-In-Amplifier-Based-LVDT-Simulation.git
cd Digital-Lock-In-Amplifier-Based-LVDT-Simulation
python -m venv .venv
.\.venv\Scripts\Activate.ps1                 # Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e . --no-build-isolation --no-deps
```

### 2. Icarus Verilog (needed to run the real RTL)

Icarus is a standalone program, not a pip package.

| OS | Command |
|---|---|
| Windows | Download and run `https://bleyer.org/icarus/iverilog-v12-20220611-x64_setup.exe`, and tick **"Add executable folder(s) to the user PATH"**. Or, from an admin shell: `choco install iverilog -y` |
| Ubuntu/Debian | `sudo apt install iverilog` |
| macOS | `brew install icarus-verilog` |

Reopen the terminal and check with `iverilog -V`. If Icarus is installed but not on PATH, set
`IVERILOG_BIN` to its `bin` folder. The runner also checks `C:\iverilog\bin` and
`~/iverilog/ucrt64/bin`. Without Icarus, the dashboard still runs using a cycle-accurate Python
model of `lockin_top.v`, and it labels that engine on the page.

## Run

### Web dashboard

```powershell
python web/app.py                 # http://127.0.0.1:5000 (Waitress)
```

Environment variables: `HOST` (default `127.0.0.1`; use `0.0.0.0` to expose on a network),
`PORT` (default `5000`), `FLASK_DEV=1` (Flask debug server with auto-reload).

Workflow on the page:

1. Pick a preset or tune the sliders: motion, sensitivity, phase error, noise σ, hum, offset,
   tone, drift and seed.
2. **① Generate signal & vectors** runs the Python model and writes HEX/CSV vectors to
   `output/web_runs/`.
3. **② Run Verilog lock-in** runs Icarus on `tb_lockin.v` + `lockin_top.v` twice (I and Q).
4. Read the results: magnitude (V and mm), phase angle (°), signed displacement, the per-window
   table with ✓ for bit-exact I/Q, the charts, and the simulator log. **Download** gives the
   vector bundle.

### Command-line simulation and vectors

```powershell
python scripts/generate_scenarios.py --config configs/baseline.json --all   # 10 standard scenarios
python scripts/generate_hdl_vectors.py --config configs/noisy.json --name my_case --stream-id 3
python scripts/run_validation.py          # pytest and numerical acceptance checks
python scripts/generate_diagnostic_plots.py
python scripts/audit_exports.py           # independent HEX/CSV/accumulator audit
python -m pytest -q
```

### Verilog only (manual)

`lockin_top.v` reads `data/reference_lut.hex` relative to the working directory:

```powershell
mkdir sim_run\data -Force
copy output\vectors\baseline\*.hex sim_run\data\
cd sim_run
iverilog -g2005 -DNUM_SAMPLES=20000 -o tb.vvp ..\hdl\sim\tb_lockin.v ..\hdl\rtl\lockin_top.v
vvp tb.vvp                                # TEST PASSED; writes rtl_results.csv
```

Compare `rtl_results.csv` (`accumulator`) with `output/vectors/baseline/expected_results.csv`
(`expected_accumulator`). They must be identical.

### Deploying the dashboard on a server

Any Linux VM works (for example AWS, Azure or GCP):

```bash
sudo apt install -y python3-venv iverilog
git clone https://github.com/anmolkamath22/Digital-Lock-In-Amplifier-Based-LVDT-Simulation.git
cd Digital-Lock-In-Amplifier-Based-LVDT-Simulation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && pip install -e . --no-build-isolation --no-deps
HOST=0.0.0.0 PORT=8000 python web/app.py
```

Static-only hosts (GitHub Pages, Vercel, Streamlit Cloud) cannot run Icarus Verilog, so they
are not suitable for the live RTL simulation.

## Configuration reference

### Physical and numerical assumptions

Every sample time is `t[n] = n/fs`; no cumulative time stepping is used. Duration
must contain an integer number of samples. Defaults: fs=20 kHz, fc=1 kHz,
K=0.24 Vpeak/mm, A0=2 Vpeak, primary=5 Vpeak, displacement range ±5 mm,
phase=0 degrees, cubic coefficient alpha=0, seed=42. All amplitudes are peak
voltages, not RMS. The primary amplitude is informational in this fixed-coupling
model; changing it does not automatically change K or A0.

```text
Vp = Ap sin(2 pi fc t)
D  = K x + alpha x^3
V1 = (A0 + D/2) sin(2 pi fc t + phi)
V2 = (A0 - D/2) sin(2 pi fc t + phi)
Vdiff = V1 - V2 = D sin(2 pi fc t + phi)
```

At null the secondaries cancel exactly. Negative displacement reverses phase.
At ±5 mm in the default linear model, winding peak amplitudes are 1.4 and 2.6 V.
Configuration validates positive secondary amplitudes over the entire range,
including stationary points when a cubic term is enabled. Secondary amplitudes
need not equal the primary amplitude. The estimator always divides by linear K;
it does not invert optional nonlinearity or silently compensate phase.

Noise is added to the differential output after the sensor: Gaussian white
noise, 50 Hz hum, DC offset, a configurable narrowband tone, and optional slow
sinusoidal baseline drift. All default to zero. Sensor phase shifts both
secondaries together. `default_rng(SeedSequence([seed, stream_id]))` provides
reproducible separate streams. `--all` assigns IDs 0 through 9 in the scenario
order below (or offsets them by `--stream-id`). A standalone scenario defaults
to ID 0; its metadata always records the actual ID. No waveform is rescaled to
avoid saturation.

### Trajectories

Set `trajectory.mode` and the following keys in JSON. Unknown keys are rejected.

| Mode | Parameters and defaults |
|---|---|
| static | `value_mm=0` (Config's default trajectory selects +2) |
| step | `before_mm=-3`, `after_mm=3`, `step_s=0.5`; after value starts at t >= step_s |
| sine | `center_mm=0`, `amplitude_mm=3`, `frequency_hz=2`, `phase_deg=0` |
| ramp | `start_mm=-5`, `end_mm=5`; endpoints at first and last sample |
| calibration | `values_mm=[-5,-3,-1,0,1,3,5]`, `hold_windows=5` |
| custom | `csv_path`; CSV columns `time_s,displacement_mm` |

Calibration duration must exactly match number of positions times hold windows
times window samples divided by fs. Custom CSV times must be finite and strictly
increasing, contain at least two points, and cover every requested sample time.
Values are linearly interpolated with no extrapolation. Relative CSV paths are
resolved against the config file directory. All CSV displacement entries and all
generated physical samples must be in range; no physical input is clipped.

### ADC and reference

ADC: nominal 12 bits, bipolar ±2.5 V, signed codes −2048…+2047 in an int16 container.

```text
q = clip(rint(v * 2048 / 2.5), -2048, +2047)
v_reconstructed = q * 2.5 / 2048
r[k] = rint(16384 * sin(2 pi k/20)), k=0...19
```

All rounding uses NumPy `rint` (nearest, ties to even). Implementation bounds the
voltage before scaling, then rounds/saturates; this is equivalent for finite
inputs and avoids overflow. `clipped_count` includes rounded codes outside the
representable range and analog overrange. Analog overrange counts only |v|>2.5 V.
Thus +2.5 V is clipped to +2047, while −2.5 V maps exactly to −2048. Positive
saturation begins half an LSB below +2.5 V under ties-to-even rounding. For
nonclipped inputs error is at most half an LSB (0.6103515625 mV).

HEX has one uppercase four-character word per line, no header, no `0x`.
−1 is `FFFF`, −2048 is `F800`, +2047 is `07FF`; `0800` never occurs as a default
ADC value. The LUT has exactly 20 entries with zero at index 0, peaks ±16384,
and signed 16-bit Q1.14 scaling (divide by 16384). Load these exact rounded words
in RTL. Coherence requires fs/fc = LUT length; different integral ratios may be
configured but must be coordinated with the HDL implementation.

### Reference measurement and timing

```text
I = (2/N) sum(measured_analog_v[n] * sin(2 pi n/20))
x_float = I/K
S = sum(int(q[n]) * int(r[n mod 20]))
x_fixed_mm = 2*S/(N*16384) * (2.5/2048) / K
```

N=200 accepted samples by default. The fixed path multiplies and sums signed
int64 integers; conversion to millimeters happens only after the exact sum.
No I/Q, phase compensation, filters, or RTL are used. Each independent stream
starts its reference at zero. Reference phase is continuous across nonoverlapping
windows, including when a configurable window does not span full cycles. Such
windows can have DC leakage and gain ripple; the baseline uses exactly ten cycles.

Incomplete trailing samples are rejected from measurement (discarded, never
padded); they remain in the ADC and ground-truth exports. Their count is in
metadata. A chunk API can supply `start_sample` at a window boundary to retain
global phase; it does not retain partial chunks internally.

Window i uses samples i*N through (i+1)*N−1 inclusive. Center time is the mean of
the first and last sample times: first window 0.004975 s, last accepted sample
0.00995 s. The first result becomes available only after that last sample, plus
the implementation's processing latency. The cadence is 10 ms. Relative to its
reported center, acquisition latency is 4.975 ms. For an arbitrary step inside a
window, the crossing window mixes old/new positions and the next full window is
settled (within at most about 20 ms after the step, before HDL latency).

For varying x, the ideal result is `(2/N)*sum(x[n]*sin(...)^2)`, not necessarily
the arithmetic mean or the exact position at center. This finite-window
smoothing explains dynamic errors. The expected-results file includes the
arithmetic truth mean as a diagnostic comparison, not a claim of equality.

### Data contract (version 1.0.0)

`ground_truth.csv`, exact column order:

```text
sample_index,time_s,displacement_mm,primary_voltage_v,secondary_1_v,secondary_2_v,differential_voltage_v,measured_analog_voltage_v,adc_code
```

`expected_results.csv`, exact column order:

```text
window_index,start_sample,end_sample,center_time_s,expected_accumulator,estimated_displacement_mm,true_window_mean_mm,absolute_error_mm
```

Indices are zero-based; end_sample is inclusive. Accumulators are integer text,
not rounded floating-point values. Error is the absolute difference of the fixed
estimate and arithmetic truth mean. `metadata.json` records the full effective
configuration, units, frequencies, ADC/LUT scales and formats, seed/stream ID,
sample/window/trailing counts, clipping, column order, widths, and limitations.
Changing scenario configuration replaces that scenario's files; use a different
name or output directory to retain multiple runs.

### HDL integration rules

1. Reset independently for each scenario. Load its `adc_samples.hex` and
   `reference_lut.hex` with `$readmemh` into signed 16-bit memories/registers.
2. On each `sample_valid=1`, multiply the current signed ADC code by the signed
   LUT entry. The first accepted ADC sample multiplies LUT index 0. Increment
   reference index modulo 20 and measurement count only on accepted samples.
3. Use signed multiplication with a sufficiently wide product (32 bits is safe)
   and sign extension into a signed accumulator of at least 40 bits.
4. The 200th accepted sample (index 199) is part of the first result. Latch
   `old_accumulator + current_product`, assert output valid after completing that
   addition, and clear the running sum/count for the next accepted sample. The
   next sample begins the next window; keep LUT phase continuous.
5. Reset clears running accumulation, sample count, output valid, and reference
   phase. `sample_valid=0` advances neither counter and adds nothing. Arbitrary
   gaps therefore change wall-clock timing but never expected sums.
6. Compare each signed output integer, in order, exactly against the
   `expected_accumulator` column. Do not compare HDL sums against rounded
   displacement or apply engineering-unit scaling before this comparison.

Default maximum absolute product is 2048*16384 = **33,554,432**. Conservative
maximum absolute accumulation is 200 times that = **6,710,886,400**, requiring
34 signed bits. A 40-bit accumulator spans −549,755,813,888 through
+549,755,813,887 and cannot overflow. The bound is intentionally conservative:
not all sine entries have peak magnitude. Width recommendations and conservative
bounds for custom settings are included in metadata; retain at least 40 bits.
Signed declarations/casts are essential because both ADC codes and LUT words can
be negative. Sample-valid gaps do not appear as zero-valued samples in HEX.

### Scenarios and verification

`--all` creates, in order: null (0 mm), positive (+2), negative (−2), calibration
(−5…+5, 1 mm increments, five windows per level), high_noise (sigma 0.4 V and
0.1 Vpeak hum), step (−3 to +3 at duration/2), sinusoidal (3 mm, 2 Hz),
phase_mismatch (45 degrees), adc_overrange (3 Vpeak coherent added tone), and
same_frequency_interference (0.24 Vpeak coherent added tone).

Tests cover physical identities and bounds, every trajectory mode, custom CSV,
RNG statistics/reproducibility/independence, individual additive components,
ADC rounding/full scale/quantization bounds, independent HEX decoding,
LUT sign/scaling/continuity, zero/positive/negative estimates, calibration,
200/400/399-sample windows, inclusion of the last sample, exact scalar integer
agreement, non-cycle-window continuity, phase cosine response, DC rejection,
400/950/1000/1050/1600 Hz interference projections, dynamic weighting, standard
scenario execution, and export contracts. The final executed suite passed 58
tests with zero failures/errors/skips; the study runner passed 23 numerical
acceptance checks. The independent export audit decoded 251,000 samples across
13 scenario directories and matched all 1,255 emitted integer accumulator
results. Per-file SHA-256 hashes are in `output/reports/export_audit.json`.

`output/reports/validation.md` contains measured results. Calibration reports
regression slope (mm/mm), equivalent estimated electrical sensitivity (V/mm),
offset, R², MAE, and maximum error. Monte Carlo uses 1000 independent windows at
each sigma=0,0.05,0.10,0.20,0.40 V, reporting distribution samples, bias, RMSE,
standard deviation, clipping, and a normal-approximation 95% interval for the
mean. Unclipped white-noise theory is sigma/(K*sqrt(N/2)); deterministic ADC/LUT
rounding contributes an additional small baseline error. Phase tests verify
`x*cos(phi)` at 0,15,30,45,90 degrees. Eight PNGs show winding voltages,
differential output, noise, quantization, dynamic displacement, calibration,
Monte Carlo error, and phase sensitivity.

### Limitations

A coherent interferer is indistinguishable from an additional displacement
projection: 0.24 Vpeak at 1 kHz and zero relative phase adds 1 mm; at 30 degrees
it adds cos(30 degrees) mm. Nearby tones leak through rectangular windows and
beat across measurements. Full-cycle averaging suppresses ideal DC, not every
noise source. Phase mismatch produces cosine gain error and 90 degrees removes
the in-phase component. Clipping distorts correlation and is explicitly counted.

The model is sampled analog-equivalent; it does not model intersample peaks,
anti-alias filtering, hysteresis, temperature, core dynamics, electromagnetic
fields, ADC aperture/jitter, or hardware analog front-end behavior. Aliasing can
still occur in optional nonlinear/dynamic waveforms. No industrial accuracy or
hardware equivalence is claimed. I/Q detection, compensation, filtering,
dashboard, and hardware deployment remain later-stage extensions.

### Config file quick guide

The main settings are controlled through JSON files in `configs/`. Copy an
existing file, then change only the values needed for the experiment. For
example, in `configs/noisy.json`:

```json
{
  "duration_s": 1.0,
  "noise_std_v": 0.20,
  "hum_peak_v": 0.10,
  "dc_offset_v": 0.15,
  "interference_peak_v": 0.10,
  "interference_hz": 950.0,
  "trajectory": {"mode": "static", "value_mm": 2.0}
}
```

Useful settings include `noise_std_v` for Gaussian noise, `hum_peak_v` and
`hum_hz` for power-line interference, `dc_offset_v` for DC offset,
`interference_peak_v`, `interference_hz`, and `interference_phase_deg` for a
narrowband tone, `phase_deg` for sensor phase error, and `drift_peak_v` and
`drift_hz` for slow drift. The trajectory object selects `static`, `step`,
`sine`, `ramp`, `calibration`, or `custom` motion.

Use the scripts as follows from the repository root:

```powershell
# Generate one scenario and its Python/HDL handoff files
python scripts/generate_scenarios.py --config configs/baseline.json

# Generate calibration vectors for an HDL testbench
python scripts/generate_hdl_vectors.py --config configs/calibration.json

# Generate all ten standard scenarios
python scripts/generate_scenarios.py --config configs/baseline.json --all

# Run unit tests and numerical validation
python scripts/run_validation.py

# Generate the eight static diagnostic plots
python scripts/generate_diagnostic_plots.py

# Independently check HEX formatting, CSV ordering, and exact accumulators
python scripts/audit_exports.py
```

For a custom output folder or scenario name:

```powershell
python scripts/generate_hdl_vectors.py `
  --config configs/noisy.json `
  --output-dir my_output `
  --name noisy_experiment `
  --stream-id 3
```

The HDL input files are stored at:

```text
output/vectors/<scenario>/adc_samples.hex
output/vectors/<scenario>/reference_lut.hex
output/vectors/<scenario>/expected_results.csv
output/vectors/<scenario>/metadata.json
```

The matching physical debug file is stored at:

```text
output/ground_truth/<scenario>/ground_truth.csv
```

`adc_samples.hex` is the signed 16-bit ADC stream. `reference_lut.hex` is the
20-entry signed Q1.14 sine table. An HDL testbench should compare each
completed accumulator against the `expected_accumulator` column in
`expected_results.csv`. `metadata.json` records the exact settings and scaling
used to create those files. Re-running with the same configuration and stream
ID reproduces the same bytes; changing the configuration or name creates a new
experiment or replaces files under the same scenario name.
