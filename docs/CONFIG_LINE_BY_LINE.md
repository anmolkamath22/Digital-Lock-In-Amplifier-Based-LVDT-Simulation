# Configuration and project setup: every source line explained

JSON keys not supplied in a file use Config defaults. JSON is data, not Python; object braces group settings and commas separate entries. All voltages are peak volts unless explicitly stated otherwise.

## configs/baseline.json

A clean constant +2 mm signal; all noise sources and phase shift remain at defaults of zero.

Source snapshot SHA-256: `11ab8167c677469c9e961de3adca8d84cd2de6736b622d63c89b28da8d7907af`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>{</code> | Opens the JSON configuration object. |
| 2 | <code>  &quot;duration_s&quot;: 1.0,</code> | Requests one second: 20,000 samples with the default sampling frequency. |
| 3 | <code>  &quot;seed&quot;: 42,</code> | Selects reproducible random seed 42, even though baseline Gaussian noise is disabled. |
| 4 | <code>  &quot;trajectory&quot;: {&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: 2.0}</code> | Selects static displacement at +2 mm. |
| 5 | <code>}</code> | Closes the configuration object. |

## configs/calibration.json

Stable positions aligned to complete windows. Duration is derived from 11 positions, five windows each.

Source snapshot SHA-256: `14d6a9e1e38b116d0c45c1626e1cd8e985b4c0b5b81c55b4dada35446b273f61`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>{</code> | Opens the JSON object. |
| 2 | <code>  &quot;duration_s&quot;: 0.55,</code> | Requests 0.55 seconds: 11,000 samples or 55 windows at default settings. |
| 3 | <code>  &quot;seed&quot;: 42,</code> | Chooses base random seed 42. |
| 4 | <code>  &quot;trajectory&quot;: {&quot;mode&quot;: &quot;calibration&quot;, &quot;values_mm&quot;: [-5,-4,-3,-2,-1,0,1,2,3,4,5], &quot;hold_windows&quot;: 5}</code> | Selects every integer mm position from -5 to +5, holding each five complete 200-sample windows (50 ms). |
| 5 | <code>}</code> | Closes the configuration object. |

## configs/dynamic.json

Slow sinusoidal mechanical motion modulates a much faster electrical carrier.

Source snapshot SHA-256: `4aacf3eb70d56baeedfdd01519efadf5581f70bb7222e4fbba4ee9a61f2a395a`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>{</code> | Opens the JSON object. |
| 2 | <code>  &quot;duration_s&quot;: 1.0,</code> | Requests one second of motion. |
| 3 | <code>  &quot;seed&quot;: 42,</code> | Selects reproducible base seed 42. |
| 4 | <code>  &quot;trajectory&quot;: {&quot;mode&quot;: &quot;sine&quot;, &quot;center_mm&quot;: 0.0, &quot;amplitude_mm&quot;: 3.0, &quot;frequency_hz&quot;: 2.0}</code> | Selects center 0 mm, mechanical amplitude 3 mm, and mechanical frequency 2 Hz; the electrical carrier remains 1 kHz. |
| 5 | <code>}</code> | Closes the JSON object. |

## configs/noisy.json

Constant +2 mm with several measurement additions. Use this config without --all to keep these exact scenario settings.

Source snapshot SHA-256: `d06ea6f358dc6dfb5d622a649da61aef34c48c4c72df45d87bc161116d33f8fa`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>{</code> | Opens the JSON object. |
| 2 | <code>  &quot;duration_s&quot;: 1.0,</code> | Requests one second, or 20,000 input samples. |
| 3 | <code>  &quot;noise_std_v&quot;: 0.2,</code> | Sets Gaussian standard deviation to 0.2 V. |
| 4 | <code>  &quot;hum_peak_v&quot;: 0.1,</code> | Sets 50 Hz default-frequency hum amplitude to 0.1 Vpeak. |
| 5 | <code>  &quot;dc_offset_v&quot;: 0.15,</code> | Adds a constant +0.15 V measurement offset. |
| 6 | <code>  &quot;interference_peak_v&quot;: 0.1,</code> | Sets the additional narrowband interferer amplitude to 0.1 Vpeak. |
| 7 | <code>  &quot;interference_hz&quot;: 950.0,</code> | Sets that interferer to 950 Hz, close to but different from the 1 kHz carrier. |
| 8 | <code>  &quot;seed&quot;: 42,</code> | Sets seed 42 for reproducible Gaussian noise. |
| 9 | <code>  &quot;trajectory&quot;: {&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: 2.0}</code> | Keeps physical displacement static at +2 mm. |
| 10 | <code>}</code> | Closes the JSON object. |

## pyproject.toml

Makes the src-layout package installable and tells pytest where source/tests live. Distribution name lvdt-sim is installed with pip; import name is lvdt_sim.

Source snapshot SHA-256: `b01211191a9719e0b52c77524287a66066c14879af1d2c94e7ebf3f28ec438cd`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>[build-system]</code> | Opens the build-system TOML table. |
| 2 | <code>requires = [&quot;setuptools&gt;=68&quot;]</code> | Requires setuptools version 68 or newer to build the package. |
| 3 | <code>build-backend = &quot;setuptools.build_meta&quot;</code> | Selects setuptools' standardized Python build backend. |
| 4 | <code></code> | Blank separator for readability; no operation. |
| 5 | <code>[project]</code> | Opens package distribution metadata. |
| 6 | <code>name = &quot;lvdt-sim&quot;</code> | Defines the installable distribution name lvdt-sim. |
| 7 | <code>version = &quot;1.0.0&quot;</code> | Sets distribution version 1.0.0. |
| 8 | <code>description = &quot;Physical LVDT simulation and bit-exact lock-in verification vectors&quot;</code> | Supplies the short package description. |
| 9 | <code>requires-python = &quot;&gt;=3.11&quot;</code> | Declares Python 3.11 or newer. |
| 10 | <code>dependencies = [&quot;numpy&gt;=1.24&quot;, &quot;matplotlib&gt;=3.7&quot;]</code> | Declares runtime dependencies: NumPy for numerical work and Matplotlib for diagnostic plots. |
| 11 | <code></code> | Blank separator for readability; no operation. |
| 12 | <code>[tool.setuptools.packages.find]</code> | Opens setuptools package-discovery settings. |
| 13 | <code>where = [&quot;src&quot;]</code> | Tells package discovery to look under src, locating the lvdt_sim package. |
| 14 | <code></code> | Blank separator for readability; no operation. |
| 15 | <code>[tool.pytest.ini_options]</code> | Opens pytest configuration. |
| 16 | <code>testpaths = [&quot;tests&quot;]</code> | Makes tests the default test discovery directory. |
| 17 | <code>pythonpath = [&quot;src&quot;]</code> | Adds src to pytest's import path; installed CLI usage still uses the actual installed package. |

## requirements.txt

One installation list covering both runtime and testing dependencies. Standard-library csv handles CSV export, so pandas/SciPy are not required.

Source snapshot SHA-256: `ffa1e7ee8f11c0b1a3ffbb469b9c0da6621dc91117df6f39d7fe2a92c7c74c50`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>numpy&gt;=1.24</code> | Requires NumPy 1.24 or newer for vectorized arrays, arithmetic, and reproducible generators. |
| 2 | <code>matplotlib&gt;=3.7</code> | Requires Matplotlib 3.7 or newer for static engineering PNGs. |
| 3 | <code>pytest&gt;=7.4</code> | Requires pytest 7.4 or newer for automated verification. |

## .gitignore

Tells Git to ignore reproducible build/environment/output products; these rules do not delete files or stop scripts from generating them.

Source snapshot SHA-256: `0bf6aa1d81099bb126ad08309bc42e871310ef560257323b96ee753b36bda0b5`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>__pycache__/</code> | Ignores Python bytecode cache directories. |
| 2 | <code>*.py[cod]</code> | Ignores .pyc, .pyo, and .pyd files matched by the bracket pattern. |
| 3 | <code>.pytest_cache/</code> | Ignores pytest's temporary cache. |
| 4 | <code>*.egg-info/</code> | Ignores generated Python package installation metadata directories. |
| 5 | <code>.venv/</code> | Ignores the local virtual environment and its third-party packages. |
| 6 | <code>output/</code> | Ignores generated output vectors, truth CSVs, plots, and reports; handoff copies may still be shared explicitly. |

