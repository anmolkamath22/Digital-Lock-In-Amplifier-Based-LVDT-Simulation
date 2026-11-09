# Core Python: every source line explained

Read [START_HERE](START_HERE.md) for architecture and Verilog connectors. Each table preserves the original line numbers; a multi-line statement is explained across its constituent rows. Type annotations describe intended types but do not themselves validate values.

## src/lvdt_sim/__init__.py

Package entry point. It makes Config available as from lvdt_sim import Config; it does not run a simulation.

Source snapshot SHA-256: `4c6e8dd27d0c4f56f02205062d18c3f19817668ae8ff3fb6f02c5a8d16e45410`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Phase 1 LVDT physical simulation; all voltages are peak-referenced volts.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code></code> | Blank separator for readability; no operation. |
| 5 | <code>__version__ = &quot;1.0.0&quot;</code> | Records the package version string. |
| 6 | <code>__all__ = [&quot;Config&quot;]</code> | Declares Config as the name exported by wildcard imports; other submodules remain directly importable. |

## src/lvdt_sim/config.py

All instrument knobs and configuration checks. Edit JSON for normal use; extend this dataclass when introducing a new instrument parameter.

Source snapshot SHA-256: `f7ea332d57e1c58797ae7d15d898067e132ba8212cbcbbcc16db2f6646294465`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Validated configuration. Frequencies in Hz, time in s, displacement in mm.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from dataclasses import asdict, dataclass, field</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>import json</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>import math</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code>@dataclass(frozen=True)</code> | Creates constructor/record behavior automatically and prevents reassigning fields; contained arrays/dictionaries remain mutable. |
| 10 | <code>class Config:</code> | Defines the Config record and its default instrument settings. |
| 11 | <code>    fs_hz: float = 20000.0</code> | Samples per second: 20,000 by default; each sample is separated by 50 microseconds. |
| 12 | <code>    fc_hz: float = 1000.0</code> | Electrical carrier frequency: 1,000 Hz, giving 20 samples per carrier cycle. |
| 13 | <code>    duration_s: float = 1.0</code> | Requested simulation length in seconds. |
| 14 | <code>    sensitivity_v_per_mm: float = 0.24</code> | K: differential peak-voltage sensitivity per millimeter; used in both physics and mm conversion. |
| 15 | <code>    secondary_null_v: float = 2.0</code> | A0: each secondary winding's peak amplitude when the core is at null. |
| 16 | <code>    primary_peak_v: float = 5.0</code> | Ap: primary excitation peak voltage; changing it alone does not change the fixed K/A0 coupling. |
| 17 | <code>    min_mm: float = -5.0</code> | Lowest accepted physical core displacement, in mm. |
| 18 | <code>    max_mm: float = 5.0</code> | Highest accepted physical core displacement, in mm. |
| 19 | <code>    phase_deg: float = 0.0</code> | Sensor electrical phase shift relative to the reference, in degrees. |
| 20 | <code>    cubic_v_per_mm3: float = 0.0</code> | Optional cubic differential coefficient; zero keeps the sensor linear. |
| 21 | <code>    adc_full_scale_v: float = 2.5</code> | Magnitude F of the bipolar ADC input voltage range. |
| 22 | <code>    adc_bits: int = 12</code> | Nominal ADC resolution; default signed numerical codes are -2048 through +2047. |
| 23 | <code>    lut_length: int = 20</code> | Reference LUT length; must equal fs/fc. |
| 24 | <code>    window_samples: int = 200</code> | Accepted ADC samples per nonoverlapping correlation result. |
| 25 | <code>    seed: int = 42</code> | Base random seed used to reproduce noise. |
| 26 | <code>    noise_std_v: float = 0.0</code> | Gaussian noise standard deviation in volts; zero disables this component. |
| 27 | <code>    hum_peak_v: float = 0.0</code> | Hum peak voltage; zero disables hum. |
| 28 | <code>    hum_hz: float = 50.0</code> | Hum frequency, usually 50 Hz for this simulation. |
| 29 | <code>    hum_phase_deg: float = 0.0</code> | Hum phase, in degrees. |
| 30 | <code>    dc_offset_v: float = 0.0</code> | Constant additive voltage offset at the measurement input. |
| 31 | <code>    interference_peak_v: float = 0.0</code> | Additional sinusoidal interferer peak voltage. |
| 32 | <code>    interference_hz: float = 400.0</code> | Additional interferer frequency; used only in a nonzero-amplitude contribution. |
| 33 | <code>    interference_phase_deg: float = 0.0</code> | Additional interferer phase in degrees. |
| 34 | <code>    drift_peak_v: float = 0.0</code> | Optional slow baseline-drift peak voltage. |
| 35 | <code>    drift_hz: float = 0.1</code> | Drift frequency in Hz. |
| 36 | <code>    trajectory: dict = field(default_factory=lambda: {&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: 2.0})</code> | Creates a separate trajectory dictionary per Config instance; the default selects constant +2 mm. |
| 37 | <code></code> | Blank separator for readability; no operation. |
| 38 | <code>    def __post_init__(self) -&gt; None:</code> | Runs validation automatically after the dataclass constructor sets fields. |
| 39 | <code>        for name, value in asdict(self).items():</code> | Walks through a dictionary copy of every configuration field. |
| 40 | <code>            if name != &quot;trajectory&quot; and (not isinstance(value, (int, float)) or not math.isfinite(value)):</code> | Requires each non-trajectory scalar to be a finite Python int or float. |
| 41 | <code>                raise ValueError(f&quot;{name} must be a finite number&quot;)</code> | Stops construction with a field-specific error if the scalar check fails. |
| 42 | <code>        for name in (&quot;fs_hz&quot;, &quot;fc_hz&quot;, &quot;duration_s&quot;, &quot;sensitivity_v_per_mm&quot;, &quot;secondary_null_v&quot;,</code> | Lists scalar parameters that must be strictly positive. |
| 43 | <code>                     &quot;primary_peak_v&quot;, &quot;adc_full_scale_v&quot;):</code> | Lists scalar parameters that must be strictly positive. |
| 44 | <code>            if getattr(self, name) &lt;= 0:</code> | Fetches each named attribute and checks its value is greater than zero. |
| 45 | <code>                raise ValueError(f&quot;{name} must be positive&quot;)</code> | Rejects a nonpositive value with an informative name. |
| 46 | <code>        for name in (&quot;adc_bits&quot;, &quot;lut_length&quot;, &quot;window_samples&quot;, &quot;seed&quot;):</code> | Lists settings that must be actual Python integers. |
| 47 | <code>            if type(getattr(self, name)) is not int:</code> | Checks exact int type, so floating counts and boolean count fields are rejected. |
| 48 | <code>                raise ValueError(f&quot;{name} must be an integer&quot;)</code> | Rejects a noninteger count/width/seed. |
| 49 | <code>        if not 2 &lt;= self.adc_bits &lt;= 16 or self.lut_length &lt; 4 or self.window_samples &lt; 1 or self.seed &lt; 0:</code> | Checks ADC width 2..16, LUT length >=4, positive window length, and nonnegative seed. |
| 50 | <code>            raise ValueError(&quot;Invalid ADC bits, LUT length, window length or seed&quot;)</code> | Rejects invalid discrete settings before simulation starts. |
| 51 | <code>        if self.min_mm &gt;= self.max_mm:</code> | Requires the physical lower bound to be strictly below the upper bound. |
| 52 | <code>            raise ValueError(&quot;min_mm must be less than max_mm&quot;)</code> | Rejects reversed/equal physical bounds. |
| 53 | <code>        if not math.isclose(self.fs_hz / self.fc_hz, self.lut_length, rel_tol=0, abs_tol=1e-10):</code> | Checks coherent sampling: fs/fc must match the integer LUT length within a small absolute tolerance. |
| 54 | <code>            raise ValueError(&quot;Coherent reference requires fs_hz / fc_hz == lut_length&quot;)</code> | Rejects a carrier/reference ratio that the repeating LUT cannot represent. |
| 55 | <code>        if not math.isclose(self.duration_s * self.fs_hz, round(self.duration_s * self.fs_hz), abs_tol=1e-8):</code> | Checks duration*fs is approximately an integer sample count. |
| 56 | <code>            raise ValueError(&quot;duration_s must contain an integral number of samples&quot;)</code> | Rejects a fractional-sample duration. |
| 57 | <code>        if self.sample_count &lt; 1:</code> | Ensures the rounded duration includes at least one sample. |
| 58 | <code>            raise ValueError(&quot;duration must contain at least one sample&quot;)</code> | Rejects a duration too small to generate data. |
| 59 | <code>        for name in (&quot;noise_std_v&quot;, &quot;hum_peak_v&quot;, &quot;interference_peak_v&quot;, &quot;drift_peak_v&quot;):</code> | Lists peak amplitudes and standard deviation that cannot be negative. |
| 60 | <code>            if getattr(self, name) &lt; 0:</code> | Checks each listed value for negativity. |
| 61 | <code>                raise ValueError(f&quot;{name} must be nonnegative&quot;)</code> | Rejects a negative noise amplitude or standard deviation. |
| 62 | <code>        for name in (&quot;hum_hz&quot;, &quot;interference_hz&quot;, &quot;drift_hz&quot;):</code> | Lists modeled additive sinusoid frequencies. |
| 63 | <code>            if not 0 &lt;= getattr(self, name) &lt; self.fs_hz / 2:</code> | Requires each tone frequency to be nonnegative and strictly below fs/2 (Nyquist). |
| 64 | <code>                raise ValueError(f&quot;{name} must be below Nyquist and nonnegative&quot;)</code> | Rejects invalid tone frequencies, even if their amplitudes happen to be zero. |
| 65 | <code>        if not isinstance(self.trajectory, dict):</code> | Checks trajectory settings are supplied as a dictionary. |
| 66 | <code>            raise ValueError(&quot;trajectory must be a JSON object&quot;)</code> | Rejects a trajectory of the wrong container type. |
| 67 | <code>        # Check endpoints AND stationary points of the cubic across the full range.</code> | Explanatory comment for the following code; Python does not execute it. |
| 68 | <code>        points = [self.min_mm, self.max_mm]</code> | Starts with both endpoints of the supported displacement range. |
| 69 | <code>        if self.cubic_v_per_mm3 &lt; 0:</code> | For negative cubic coefficient, the cubic amplitude can also have interior extrema. |
| 70 | <code>            root = math.sqrt(-self.sensitivity_v_per_mm / (3 * self.cubic_v_per_mm3))</code> | Solves K+3*alpha*x^2=0 to find the positive stationary-point displacement. |
| 71 | <code>            points += [p for p in (-root, root) if self.min_mm &lt;= p &lt;= self.max_mm]</code> | Adds stationary points of either sign that fall inside the configured physical range. |
| 72 | <code>        if any(abs(self.sensitivity_v_per_mm * p + self.cubic_v_per_mm3 * p**3)</code> | Requires absolute differential amplitude below 2*A0 at every possible extremum. |
| 73 | <code>               &gt;= 2 * self.secondary_null_v for p in points):</code> | Requires absolute differential amplitude below 2*A0 at every possible extremum. |
| 74 | <code>            raise ValueError(&quot;Differential amplitude would make a secondary amplitude nonpositive&quot;)</code> | Rejects a model that would make either secondary winding's peak amplitude zero or negative. |
| 75 | <code></code> | Blank separator for readability; no operation. |
| 76 | <code>    @property</code> | Exposes the following method as a read-only calculated attribute, accessed without parentheses. |
| 77 | <code>    def sample_count(self) -&gt; int:</code> | Defines sample_count as a calculated property. |
| 78 | <code>        return round(self.duration_s * self.fs_hz)</code> | Returns the nearest integral duration*fs count; validation above requires near-integral input. |
| 79 | <code></code> | Blank separator for readability; no operation. |
| 80 | <code>    def to_dict(self) -&gt; dict:</code> | Provides a plain-dictionary representation for metadata. |
| 81 | <code>        return asdict(self)</code> | Converts all dataclass fields into a dictionary. |
| 82 | <code></code> | Blank separator for readability; no operation. |
| 83 | <code>    @classmethod</code> | Passes the class as cls, allowing construction through Config.load(...). |
| 84 | <code>    def load(cls, path: str &#124; Path) -&gt; &quot;Config&quot;:</code> | Defines the config-file factory; accepts a string or pathlib Path. |
| 85 | <code>        &quot;&quot;&quot;Resolve a custom trajectory CSV relative to its configuration file.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 86 | <code>        path = Path(path)</code> | Converts the supplied filename into a portable Path object. |
| 87 | <code>        data = json.loads(path.read_text(encoding=&quot;utf-8&quot;))</code> | Reads UTF-8 JSON into ordinary Python dictionaries/numbers. |
| 88 | <code>        trajectory = data.get(&quot;trajectory&quot;, {})</code> | Gets the trajectory object if present; otherwise uses an empty dictionary for this check. |
| 89 | <code>        if trajectory.get(&quot;mode&quot;) == &quot;custom&quot; and &quot;csv_path&quot; in trajectory:</code> | Only custom CSV trajectories need filename resolution. |
| 90 | <code>            csv_path = Path(trajectory[&quot;csv_path&quot;])</code> | Converts the supplied CSV filename into a Path. |
| 91 | <code>            if not csv_path.is_absolute():</code> | Checks whether the CSV path is relative. |
| 92 | <code>                trajectory[&quot;csv_path&quot;] = str((path.parent / csv_path).resolve())</code> | Resolves a relative CSV against the JSON file's directory, not the script directory. |
| 93 | <code>        return cls(**data)</code> | Unpacks JSON keys as Config constructor arguments; omitted keys use defaults and construction runs validation. |

## src/lvdt_sim/trajectories.py

Creates ground-truth displacement, not voltage. Connector: generate(config) returns a finite one-dimensional mm array, aligned with time_vector(config).

Source snapshot SHA-256: `73194c13f5a8ec032ed8dbfabd0f03201ce20c4e2a4cab5e4403e8333040ae3e`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Ground-truth trajectories on t[n] = n/fs, with explicit physical bounds.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code>def time_vector(config: Config) -&gt; NDArray[np.float64]:</code> | Defines the shared sampled-time generator. |
| 10 | <code>    return np.arange(config.sample_count, dtype=np.float64) / config.fs_hz</code> | Creates exact integer indices 0..sample_count-1 as floats and divides by fs; avoids cumulative timestep drift. |
| 11 | <code></code> | Blank separator for readability; no operation. |
| 12 | <code></code> | Blank separator for readability; no operation. |
| 13 | <code>def validate_displacement(x_mm: NDArray, config: Config) -&gt; NDArray[np.float64]:</code> | Defines reusable validation for physical displacement arrays. |
| 14 | <code>    x = np.asarray(x_mm, dtype=np.float64)</code> | Converts the input to a float64 NumPy array. |
| 15 | <code>    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):</code> | Checks one dimension, at least one element, and no NaN or infinity. |
| 16 | <code>        raise ValueError(&quot;displacement must be a nonempty finite one-dimensional array&quot;)</code> | Rejects an invalid displacement array shape or numerical content. |
| 17 | <code>    if np.any(x &lt; config.min_mm) or np.any(x &gt; config.max_mm):</code> | Detects any sample below min_mm or above max_mm. |
| 18 | <code>        raise ValueError(f&quot;displacement outside [{config.min_mm}, {config.max_mm}] mm&quot;)</code> | Raises an error instead of silently clipping physical position. |
| 19 | <code>    return x</code> | Returns the validated float64 displacement array. |
| 20 | <code></code> | Blank separator for readability; no operation. |
| 21 | <code></code> | Blank separator for readability; no operation. |
| 22 | <code>def generate(config: Config) -&gt; NDArray[np.float64]:</code> | Defines the mode-selecting trajectory generator. |
| 23 | <code>    &quot;&quot;&quot;Generate static, step, sine, ramp, calibration, or interpolated custom motion.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 24 | <code></code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 25 | <code>    Ramps include both endpoints at the first/last sample. CSV requires strictly</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 26 | <code>    increasing time_s and displacement_mm columns covering all requested times;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 27 | <code>    linear interpolation is used, with no extrapolation.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 28 | <code>    &quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 29 | <code>    t = time_vector(config)</code> | Creates the sample-time vector. |
| 30 | <code>    p = dict(config.trajectory)</code> | Copies the trajectory dictionary so popping mode does not mutate Config's nested dictionary. |
| 31 | <code>    mode = p.pop(&quot;mode&quot;, &quot;static&quot;)</code> | Removes/reads mode from the copy, defaulting to static when absent. |
| 32 | <code>    allowed = {</code> | Starts a dictionary of accepted keys for every motion mode. |
| 33 | <code>        &quot;static&quot;: {&quot;value_mm&quot;}, &quot;step&quot;: {&quot;before_mm&quot;, &quot;after_mm&quot;, &quot;step_s&quot;},</code> | Allows only value_mm for static, and before/after/time for a step. |
| 34 | <code>        &quot;sine&quot;: {&quot;center_mm&quot;, &quot;amplitude_mm&quot;, &quot;frequency_hz&quot;, &quot;phase_deg&quot;},</code> | Allows sine center, amplitude, mechanical frequency, and mechanical starting phase. |
| 35 | <code>        &quot;ramp&quot;: {&quot;start_mm&quot;, &quot;end_mm&quot;}, &quot;calibration&quot;: {&quot;values_mm&quot;, &quot;hold_windows&quot;},</code> | Allows ramp endpoints or calibration positions/hold length. |
| 36 | <code>        &quot;custom&quot;: {&quot;csv_path&quot;},</code> | Allows a CSV filename for custom motion. |
| 37 | <code>    }</code> | Closes the multi-line container or expression opened above. |
| 38 | <code>    if mode not in allowed or set(p) - allowed[mode]:</code> | Rejects an unknown mode or any unexpected trajectory parameter. |
| 39 | <code>        raise ValueError(f&quot;Unknown trajectory mode or parameters: {mode}, {set(p)}&quot;)</code> | Reports the invalid mode/parameter names. |
| 40 | <code>    if mode == &quot;static&quot;:</code> | Selects stationary motion. |
| 41 | <code>        x = np.full(t.size, p.get(&quot;value_mm&quot;, 0.0))</code> | Fills the entire vector with one constant displacement; this branch's missing value defaults to zero. |
| 42 | <code>    elif mode == &quot;step&quot;:</code> | Selects an abrupt step. |
| 43 | <code>        step_s = p.get(&quot;step_s&quot;, 0.5)</code> | Reads the transition time, default 0.5 seconds. |
| 44 | <code>        if not np.isfinite(step_s) or not 0 &lt;= step_s &lt;= config.duration_s:</code> | Checks the step time is finite and inside the simulation interval. |
| 45 | <code>            raise ValueError(&quot;step_s must be within the simulated interval&quot;)</code> | Rejects an invalid transition time. |
| 46 | <code>        x = np.where(t &lt; step_s, p.get(&quot;before_mm&quot;, -3.0), p.get(&quot;after_mm&quot;, 3.0))</code> | Chooses before_mm when t<step_s and after_mm otherwise, including the exact transition sample. |
| 47 | <code>    elif mode == &quot;sine&quot;:</code> | Selects sinusoidal mechanical motion. |
| 48 | <code>        amplitude = p.get(&quot;amplitude_mm&quot;, 3.0)</code> | Reads mechanical amplitude in mm. |
| 49 | <code>        frequency = p.get(&quot;frequency_hz&quot;, 2.0)</code> | Reads mechanical frequency in Hz; this is not the electrical carrier frequency. |
| 50 | <code>        center = p.get(&quot;center_mm&quot;, 0.0)</code> | Reads the central displacement offset. |
| 51 | <code>        if not np.isfinite(amplitude) or amplitude &lt; 0 or not np.isfinite(frequency) or not 0 &lt;= frequency &lt; config.fs_hz / 2:</code> | Checks finite, nonnegative amplitude and finite frequency within sampled Nyquist limits. |
| 52 | <code>            raise ValueError(&quot;Invalid mechanical amplitude or frequency&quot;)</code> | Rejects invalid sine motion parameters. |
| 53 | <code>        if center - amplitude &lt; config.min_mm or center + amplitude &gt; config.max_mm:</code> | Checks the entire continuous sine envelope center +/- amplitude against physical limits. |
| 54 | <code>            raise ValueError(&quot;Sinusoid envelope exceeds the displacement range&quot;)</code> | Rejects an out-of-range envelope even if discrete samples might miss its extreme. |
| 55 | <code>        x = center + amplitude * np.sin(2 * np.pi * frequency * t + np.deg2rad(p.get(&quot;phase_deg&quot;, 0.0)))</code> | Evaluates center+A*sin(2*pi*fm*t+theta); converts the mechanical phase from degrees to radians. |
| 56 | <code>    elif mode == &quot;ramp&quot;:</code> | Selects a linear ramp. |
| 57 | <code>        x = np.linspace(p.get(&quot;start_mm&quot;, -5.0), p.get(&quot;end_mm&quot;, 5.0), t.size)</code> | Generates uniformly spaced positions with both chosen endpoints included at first/last sample. |
| 58 | <code>    elif mode == &quot;calibration&quot;:</code> | Selects piecewise stationary calibration. |
| 59 | <code>        values = validate_displacement(p.get(&quot;values_mm&quot;, [-5, -3, -1, 0, 1, 3, 5]), config)</code> | Reads calibration positions and validates every one against physical bounds. |
| 60 | <code>        hold = p.get(&quot;hold_windows&quot;, 5)</code> | Reads complete windows to hold each position. |
| 61 | <code>        if type(hold) is not int or hold &lt; 1:</code> | Requires a positive integer hold length. |
| 62 | <code>            raise ValueError(&quot;hold_windows must be a positive integer&quot;)</code> | Rejects a fractional, zero, or negative window hold. |
| 63 | <code>        x = np.repeat(values, hold * config.window_samples)</code> | Repeats each position for hold_windows*window_samples samples. |
| 64 | <code>        if x.size != t.size:</code> | Checks the resulting calibration vector fits the configured duration exactly. |
| 65 | <code>            raise ValueError(&quot;Calibration duration must equal values * hold_windows * window_samples / fs_hz&quot;)</code> | Rejects mismatched calibration duration rather than truncating or padding. |
| 66 | <code>    else:</code> | Runs the alternative branch when the preceding condition is false. |
| 67 | <code>        data = np.genfromtxt(Path(p[&quot;csv_path&quot;]), delimiter=&quot;,&quot;, names=True)</code> | Loads a comma-separated named-column CSV using the first row as column headers. |
| 68 | <code>        if not data.dtype.names or not {&quot;time_s&quot;, &quot;displacement_mm&quot;} &lt;= set(data.dtype.names):</code> | Checks required time_s and displacement_mm fields are present. |
| 69 | <code>            raise ValueError(&quot;Custom CSV requires time_s,displacement_mm columns&quot;)</code> | Rejects a CSV with missing required columns. |
| 70 | <code>        times = np.atleast_1d(data[&quot;time_s&quot;])</code> | Makes the time column at least one-dimensional even for a one-record input. |
| 71 | <code>        values = validate_displacement(np.atleast_1d(data[&quot;displacement_mm&quot;]), config)</code> | Makes the displacement column one-dimensional and validates every supplied position. |
| 72 | <code>        if times.size &lt; 2 or not np.all(np.isfinite(times)) or np.any(np.diff(times) &lt;= 0):</code> | Requires two or more finite timestamps, strictly increasing with no duplicate/reversed times. |
| 73 | <code>            raise ValueError(&quot;Custom CSV times must be finite and strictly increasing&quot;)</code> | Rejects malformed timestamps. |
| 74 | <code>        if times[0] &gt; t[0] or times[-1] &lt; t[-1]:</code> | Checks the CSV starts no later and ends no earlier than the requested sampled interval. |
| 75 | <code>            raise ValueError(&quot;Custom CSV does not cover requested sample times&quot;)</code> | Rejects missing time coverage; extrapolation is not allowed. |
| 76 | <code>        x = np.interp(t, times, values)</code> | Linearly interpolates supplied positions onto the simulation's sample-time grid. |
| 77 | <code>    return validate_displacement(x, config)</code> | Runs common output validation on all generated modes before returning the mm vector. |

## src/lvdt_sim/sensor.py

Physics connector: simulate(time, displacement, config) returns primary, both secondaries, and their difference, all in volts.

Source snapshot SHA-256: `96d63c2be1a5a4144cd3d4dd17db1fc01b78ae38fd8fb4fb438ba30aed2e598d`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Symmetric differential transformer model, not a commercial sensor specification.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from dataclasses import dataclass</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code>from .trajectories import validate_displacement</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code></code> | Blank separator for readability; no operation. |
| 10 | <code>@dataclass(frozen=True)</code> | Creates constructor/record behavior automatically and prevents reassigning fields; contained arrays/dictionaries remain mutable. |
| 11 | <code>class SensorSignals:</code> | Defines the voltage-array output record. |
| 12 | <code>    primary_v: NDArray</code> | Stores primary excitation voltage at every sample time. |
| 13 | <code>    secondary_1_v: NDArray</code> | Stores the first secondary winding voltage. |
| 14 | <code>    secondary_2_v: NDArray</code> | Stores the second secondary winding voltage. |
| 15 | <code>    differential_v: NDArray</code> | Stores the differential voltage, V1-V2. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code>def simulate(t_s: NDArray, displacement_mm: NDArray, config: Config) -&gt; SensorSignals:</code> | Defines the physical sensor calculation using aligned time and displacement arrays. |
| 19 | <code>    &quot;&quot;&quot;V1,2 = (A0 +/- (K*x + alpha*x**3)/2) sin(w*t + phase).&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 20 | <code>    x = validate_displacement(displacement_mm, config)</code> | Validates the displacement and converts it to a float64 vector. |
| 21 | <code>    t = np.asarray(t_s, dtype=float)</code> | Converts the sample times into a floating NumPy array. |
| 22 | <code>    if t.shape != x.shape or not np.all(np.isfinite(t)):</code> | Requires time/displacement shapes to match and time values to be finite. |
| 23 | <code>        raise ValueError(&quot;time and displacement must have matching finite vectors&quot;)</code> | Rejects inconsistent input arrays. |
| 24 | <code>    angle = 2 * np.pi * config.fc_hz * t</code> | Computes the carrier angle 2*pi*fc*t, in radians. |
| 25 | <code>    carrier = np.sin(angle + np.deg2rad(config.phase_deg))</code> | Generates a sine carrier including the configured sensor phase relative to primary/reference. |
| 26 | <code>    amplitude = config.sensitivity_v_per_mm * x + config.cubic_v_per_mm3 * x**3</code> | Computes differential peak amplitude D=K*x+alpha*x^3 at every sample. |
| 27 | <code>    v1 = (config.secondary_null_v + amplitude / 2) * carrier</code> | Assigns half the differential amplitude positively to secondary 1 around A0. |
| 28 | <code>    v2 = (config.secondary_null_v - amplitude / 2) * carrier</code> | Assigns half negatively to secondary 2 around A0, preserving symmetric coupling. |
| 29 | <code>    return SensorSignals(config.primary_peak_v * np.sin(angle), v1, v2, v1 - v2)</code> | Returns unshifted primary excitation, V1, V2, and the explicit subtraction V1-V2. |

## src/lvdt_sim/noise.py

Measurement nonidealities are separate voltage arrays. The pipeline sums them onto Vdiff; ideal winding arrays are retained for diagnostics.

Source snapshot SHA-256: `4bc40b782561a66bd81779852c031c7f4a86656aafa3a74c2beb06f37b5d02a6`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Additive voltage components, using local reproducible independent RNG streams.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code>def gaussian(count: int, std_v: float, seed: int, stream_id: int = 0) -&gt; NDArray:</code> | Defines reproducible Gaussian voltage noise with an independent stream identifier. |
| 9 | <code>    &quot;&quot;&quot;SeedSequence [seed, stream_id] separates scenarios without global RNG state.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 10 | <code>    if type(count) is not int or count &lt; 0 or not np.isfinite(std_v) or std_v &lt; 0:</code> | Requires a nonnegative integer sample count and finite nonnegative standard deviation. |
| 11 | <code>        raise ValueError(&quot;count and standard deviation must be nonnegative&quot;)</code> | Rejects invalid count or noise strength. |
| 12 | <code>    if type(seed) is not int or type(stream_id) is not int or min(seed, stream_id) &lt; 0:</code> | Requires nonnegative integer seed and stream ID. |
| 13 | <code>        raise ValueError(&quot;seed and stream_id must be nonnegative integers&quot;)</code> | Rejects an invalid random-stream description. |
| 14 | <code>    return np.random.default_rng(np.random.SeedSequence([seed, stream_id])).normal(0, std_v, count)</code> | Builds a local generator seeded by [seed,stream_id] and returns count normal samples with mean 0 and standard deviation std_v. |
| 15 | <code></code> | Blank separator for readability; no operation. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code>def components(t_s: NDArray, config: Config, stream_id: int = 0) -&gt; dict[str, NDArray]:</code> | Defines all additive nonidealities on a shared time vector. |
| 18 | <code>    &quot;&quot;&quot;Noise acts on the differential measurement after the ideal sensor.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 19 | <code>    t = np.asarray(t_s, dtype=float)</code> | Converts times into floating NumPy values. |
| 20 | <code>    if t.ndim != 1 or not np.all(np.isfinite(t)):</code> | Checks times form a finite one-dimensional vector. |
| 21 | <code>        raise ValueError(&quot;time must be a finite vector&quot;)</code> | Rejects invalid time input. |
| 22 | <code>    def tone(peak: float, hz: float, phase_deg: float = 0) -&gt; NDArray:</code> | Defines a local reusable sinusoidal-voltage helper. |
| 23 | <code>        return peak * np.sin(2 * np.pi * hz * t + np.deg2rad(phase_deg))</code> | Evaluates peak*sin(2*pi*frequency*t+phase), converting degrees to radians. |
| 24 | <code>    return {</code> | Returns a dictionary so components can be inspected independently. |
| 25 | <code>        &quot;gaussian_v&quot;: gaussian(t.size, config.noise_std_v, config.seed, stream_id),</code> | Generates independent Gaussian samples; zero standard deviation yields zeros. |
| 26 | <code>        &quot;hum_v&quot;: tone(config.hum_peak_v, config.hum_hz, config.hum_phase_deg),</code> | Generates configured mains hum. |
| 27 | <code>        &quot;dc_v&quot;: np.full(t.size, config.dc_offset_v),</code> | Creates a constant DC voltage vector. |
| 28 | <code>        &quot;interference_v&quot;: tone(config.interference_peak_v, config.interference_hz, config.interference_phase_deg),</code> | Generates the additional narrowband sinusoidal interferer. |
| 29 | <code>        &quot;drift_v&quot;: tone(config.drift_peak_v, config.drift_hz),</code> | Generates optional slow sinusoidal baseline drift with zero initial phase. |
| 30 | <code>    }</code> | Closes the multi-line container or expression opened above. |

## src/lvdt_sim/adc.py

Digital acquisition connector: quantize(voltage,config).codes is the signed int16 data passed to the HEX writer and future HDL.

Source snapshot SHA-256: `76a351dc4d2bba2207d8430048074a5795370b95df7009ee05ed280e21ce6890`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Bipolar ADC: NumPy rint (ties to even), saturation, signed int16 container.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from dataclasses import dataclass</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code>@dataclass(frozen=True)</code> | Creates constructor/record behavior automatically and prevents reassigning fields; contained arrays/dictionaries remain mutable. |
| 10 | <code>class ADCResult:</code> | Defines the ADC output record. |
| 11 | <code>    codes: NDArray[np.int16]</code> | Stores signed ADC integer codes inside 16-bit elements. |
| 12 | <code>    reconstructed_v: NDArray[np.float64]</code> | Stores decoded code voltages for verification. |
| 13 | <code>    clipped_mask: NDArray[np.bool_]</code> | Boolean array marking analog overrange or numerical-code saturation. |
| 14 | <code>    analog_overrange_mask: NDArray[np.bool_]</code> | Boolean array marking only physical input outside +/- full-scale voltage. |
| 15 | <code></code> | Blank separator for readability; no operation. |
| 16 | <code>    @property</code> | Exposes the following method as a read-only calculated attribute, accessed without parentheses. |
| 17 | <code>    def clipped_count(self) -&gt; int:</code> | Defines clipped_count as a computed statistic. |
| 18 | <code>        return int(np.count_nonzero(self.clipped_mask))</code> | Counts true entries in the clipping mask and returns an ordinary Python integer. |
| 19 | <code></code> | Blank separator for readability; no operation. |
| 20 | <code>    @property</code> | Exposes the following method as a read-only calculated attribute, accessed without parentheses. |
| 21 | <code>    def clipped_percent(self) -&gt; float:</code> | Defines the clipped percentage statistic. |
| 22 | <code>        return 100 * self.clipped_count / self.codes.size if self.codes.size else 0.0</code> | Computes 100*clipped/count; returns zero for an empty vector to avoid division by zero. |
| 23 | <code></code> | Blank separator for readability; no operation. |
| 24 | <code></code> | Blank separator for readability; no operation. |
| 25 | <code>def codes_to_voltage(codes: NDArray, config: Config) -&gt; NDArray:</code> | Defines inverse ADC scaling for valid integer codes. |
| 26 | <code>    codes = np.asarray(codes)</code> | Converts input codes to a NumPy array without silently coercing floats to integers. |
| 27 | <code>    limit = 1 &lt;&lt; (config.adc_bits - 1)</code> | Computes 2^(bits-1), equal to 2048 for the default 12-bit ADC. |
| 28 | <code>    if codes.dtype.kind not in &quot;iu&quot; or np.any(codes &lt; -limit) or np.any(codes &gt;= limit):</code> | Checks integer dtype and signed ADC numerical range; i/u mean signed/unsigned integer dtypes. |
| 29 | <code>        raise ValueError(&quot;ADC codes must be signed-range integers&quot;)</code> | Rejects invalid codes rather than wrapping them. |
| 30 | <code>    return codes.astype(np.float64) * (config.adc_full_scale_v / limit)</code> | Converts each code to volts using F/2^(bits-1). |
| 31 | <code></code> | Blank separator for readability; no operation. |
| 32 | <code></code> | Blank separator for readability; no operation. |
| 33 | <code>def quantize(voltage_v: NDArray, config: Config) -&gt; ADCResult:</code> | Defines the saturating quantizer from sampled voltage to signed ADC codes. |
| 34 | <code>    &quot;&quot;&quot;Clipped includes rounded codes outside range; overrange means &#124;v&#124; &gt; F.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 35 | <code></code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 36 | <code>    +F rounds to +2048 and saturates to +2047; -F is representable exactly.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 37 | <code>    Analog bounds are applied before scaling to avoid numerical overflow.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 38 | <code>    &quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 39 | <code>    v = np.asarray(voltage_v, dtype=np.float64)</code> | Converts voltages to float64. |
| 40 | <code>    if v.ndim != 1 or not np.all(np.isfinite(v)):</code> | Checks one dimension and finite voltages. |
| 41 | <code>        raise ValueError(&quot;ADC input must be a finite one-dimensional voltage vector&quot;)</code> | Rejects invalid ADC input. |
| 42 | <code>    f = config.adc_full_scale_v</code> | Reads bipolar full-scale magnitude F. |
| 43 | <code>    limit = 1 &lt;&lt; (config.adc_bits - 1)</code> | Computes negative-code magnitude, 2048 by default. |
| 44 | <code>    overrange = (v &lt; -f) &#124; (v &gt; f)</code> | Flags physical input below -F or above +F. |
| 45 | <code>    rounded = np.rint(np.clip(v, -f, f) * (limit / f))</code> | Bounds input voltage, scales to code units, and rounds to nearest with ties to even. |
| 46 | <code>    clipped = overrange &#124; (rounded &lt; -limit) &#124; (rounded &gt; limit - 1)</code> | Flags either physical overrange or rounded values outside the numerical code range. |
| 47 | <code>    codes = np.clip(rounded, -limit, limit - 1).astype(np.int16)</code> | Saturates rounded values to [-limit,limit-1], then stores them as signed int16. |
| 48 | <code>    return ADCResult(codes, codes_to_voltage(codes, config), clipped, overrange)</code> | Returns codes, reconstructed voltage, and both clipping definitions in one record. |

## src/lvdt_sim/reference.py

Reference connector: export the exact rounded LUT and use that same word order in Verilog. Numerical scaling is 16384, not 32768.

Source snapshot SHA-256: `c6875a463fdadfa03eee820c5391bc2394ab1c74dfffa69d122a1d6262609f98`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Exported sine reference is the sole Q1.14 rounding authority for RTL.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code></code> | Blank separator for readability; no operation. |
| 6 | <code>Q_SCALE = 1 &lt;&lt; 14</code> | Computes 2^14=16384 using an integer left shift; this is the Q1.14 scale. |
| 7 | <code></code> | Blank separator for readability; no operation. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code>def sine_lut(length: int = 20) -&gt; NDArray[np.int16]:</code> | Defines the periodic sine LUT generator; default length is 20. |
| 10 | <code>    if type(length) is not int or length &lt; 4:</code> | Requires an integer period of at least four entries. |
| 11 | <code>        raise ValueError(&quot;LUT length must be an integer &gt;= 4&quot;)</code> | Rejects invalid LUT lengths. |
| 12 | <code>    return np.rint(Q_SCALE * np.sin(2 * np.pi * np.arange(length) / length)).astype(np.int16)</code> | Evaluates one equally spaced sine cycle, scales by 16384, rounds ties to even, and stores signed int16 coefficients. |
| 13 | <code></code> | Blank separator for readability; no operation. |
| 14 | <code></code> | Blank separator for readability; no operation. |
| 15 | <code>def reference_samples(count: int, length: int = 20, start_sample: int = 0, fixed: bool = True) -&gt; NDArray:</code> | Defines fixed or floating reference samples for a global accepted-sample interval. |
| 16 | <code>    &quot;&quot;&quot;Global accepted-sample indexing; independent streams start at sample zero.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 17 | <code>    if type(count) is not int or count &lt; 0 or type(start_sample) is not int or start_sample &lt; 0:</code> | Requires nonnegative integer sample count and global starting sample index. |
| 18 | <code>        raise ValueError(&quot;count and start_sample must be nonnegative integers&quot;)</code> | Rejects invalid lengths or offsets. |
| 19 | <code>    lut = sine_lut(length)</code> | Generates the rounded one-cycle lookup table. |
| 20 | <code>    index = (np.arange(count) + start_sample) % length</code> | Computes global reference positions modulo the table period; start_sample preserves phase across chunks. |
| 21 | <code>    return lut[index] if fixed else np.sin(2 * np.pi * index / length)</code> | Returns rounded LUT entries for the integer path or exact floating sine values for the floating path. |

## src/lvdt_sim/lockin_reference.py

Your friend's main numerical specification. fixed() returns the exact signed integer sum to reproduce in RTL; floating() is a separate analog check.

Source snapshot SHA-256: `f3215e265e036195bc9eb883eedd5ab183b60ea1eb652f5eb76763b317e6576d`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Rectangular, single-channel synchronous detection; incomplete tails discarded.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from dataclasses import dataclass</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code>from .reference import Q_SCALE, reference_samples</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code></code> | Blank separator for readability; no operation. |
| 9 | <code></code> | Blank separator for readability; no operation. |
| 10 | <code>@dataclass(frozen=True)</code> | Creates constructor/record behavior automatically and prevents reassigning fields; contained arrays/dictionaries remain mutable. |
| 11 | <code>class LockInResult:</code> | Defines one record containing arrays of per-window results. |
| 12 | <code>    start_sample: NDArray</code> | Stores the first accepted-sample index of each window. |
| 13 | <code>    end_sample: NDArray</code> | Stores each last sample index, inclusive. |
| 14 | <code>    center_time_s: NDArray</code> | Stores the midpoint time between each window's first and last samples. |
| 15 | <code>    displacement_mm: NDArray</code> | Stores one estimated displacement in mm per complete window. |
| 16 | <code>    accumulator: NDArray &#124; None = None</code> | Optional integer sum array; the floating path leaves it as None. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code></code> | Blank separator for readability; no operation. |
| 19 | <code>def _windows(values: NDArray, config: Config, start_sample: int) -&gt; tuple[NDArray, NDArray, NDArray, NDArray]:</code> | Defines the shared window slicer; underscore marks an internal helper by convention. |
| 20 | <code>    a = np.asarray(values)</code> | Converts the incoming sequence to an array. |
| 21 | <code>    if a.ndim != 1 or not np.all(np.isfinite(a)):</code> | Requires a finite one-dimensional input sequence. |
| 22 | <code>        raise ValueError(&quot;Lock-in input must be a finite vector&quot;)</code> | Rejects invalid waveform dimensions or values. |
| 23 | <code>    if type(start_sample) is not int or start_sample &lt; 0 or start_sample % config.window_samples:</code> | Requires a nonnegative integer global start index aligned to a measurement-window boundary. |
| 24 | <code>        raise ValueError(&quot;start_sample must be a nonnegative measurement-window boundary&quot;)</code> | Rejects a chunk that does not begin at a complete window boundary. |
| 25 | <code>    count = a.size // config.window_samples</code> | Uses integer division to count complete windows; incomplete trailing samples cannot produce an answer. |
| 26 | <code>    start = start_sample + np.arange(count, dtype=np.int64) * config.window_samples</code> | Computes each window's global first sample index. |
| 27 | <code>    end = start + config.window_samples - 1</code> | Computes each inclusive last index as start+N-1. |
| 28 | <code>    center = (start + end) / (2 * config.fs_hz)</code> | Converts the midpoint of the first and last indices into seconds. |
| 29 | <code>    return a[:count * config.window_samples].reshape(count, config.window_samples), start, end, center</code> | Discards incomplete tail for this call, reshapes samples into rows of N, and returns window data plus indices/times. |
| 30 | <code></code> | Blank separator for readability; no operation. |
| 31 | <code></code> | Blank separator for readability; no operation. |
| 32 | <code>def floating(voltage_v: NDArray, config: Config, start_sample: int = 0) -&gt; LockInResult:</code> | Defines the floating analog-reference detector; start_sample preserves global phase. |
| 33 | <code>    &quot;&quot;&quot;Use measured analog-equivalent volts, not reconstructed ADC volts.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 34 | <code>    windows, start, end, center = _windows(voltage_v, config, start_sample)</code> | Splits analog volts into complete measurement windows. |
| 35 | <code>    ref = reference_samples(windows.size, config.lut_length, start_sample, fixed=False).reshape(windows.shape)</code> | Generates unquantized sine reference values for the same global sample indices and matrix shape. |
| 36 | <code>    amplitude_v = 2 * np.sum(windows * ref, axis=1) / config.window_samples</code> | Multiplies measured volts by reference and sums along each window row; 2/N recovers peak amplitude for coherent full-cycle windows. |
| 37 | <code>    return LockInResult(start, end, center, amplitude_v / config.sensitivity_v_per_mm)</code> | Divides peak differential volts by K to obtain mm and returns the result record. |
| 38 | <code></code> | Blank separator for readability; no operation. |
| 39 | <code></code> | Blank separator for readability; no operation. |
| 40 | <code>def accumulator_to_mm(accumulator: NDArray, config: Config) -&gt; NDArray:</code> | Defines conversion of completed integer accumulator values to mm. |
| 41 | <code>    &quot;&quot;&quot;Only the final engineering-unit conversion uses floating point.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 42 | <code>    return (2 * np.asarray(accumulator, dtype=np.float64) / (config.window_samples * Q_SCALE)</code> | Converts completed sums to float and removes the 200-sample/Q1.14 correlation scale (using configurable N). |
| 43 | <code>            * config.adc_full_scale_v / (1 &lt;&lt; (config.adc_bits - 1)) / config.sensitivity_v_per_mm)</code> | Multiplies by volts per ADC code and divides by K; default scale is 2.5/2048/0.24. |
| 44 | <code></code> | Blank separator for readability; no operation. |
| 45 | <code></code> | Blank separator for readability; no operation. |
| 46 | <code>def fixed(codes: NDArray, config: Config, start_sample: int = 0) -&gt; LockInResult:</code> | Defines the bit-exact integer ADC/reference correlation path. |
| 47 | <code>    a = np.asarray(codes)</code> | Converts codes to an array without rounding or changing their type. |
| 48 | <code>    limit = 1 &lt;&lt; (config.adc_bits - 1)</code> | Computes the configured signed ADC limit. |
| 49 | <code>    if a.dtype.kind not in &quot;iu&quot; or np.any(a &lt; -limit) or np.any(a &gt;= limit):</code> | Requires integer dtype and every code inside the nominal ADC range. |
| 50 | <code>        raise ValueError(&quot;Fixed lock-in requires valid signed ADC integer codes&quot;)</code> | Rejects float or out-of-range samples. |
| 51 | <code>    max_sum = config.window_samples * limit * Q_SCALE</code> | Computes a conservative bound N*ADC_limit*16384 for the absolute sum. |
| 52 | <code>    if max_sum &gt; np.iinfo(np.int64).max:</code> | Checks that the configured bound fits Python's chosen NumPy int64 accumulation. |
| 53 | <code>        raise ValueError(&quot;Configured window could overflow int64 accumulation&quot;)</code> | Rejects an int64-unsafe window size. |
| 54 | <code>    windows, start, end, center = _windows(a, config, start_sample)</code> | Obtains complete windows and their global boundaries/timestamps. |
| 55 | <code>    ref = reference_samples(windows.size, config.lut_length, start_sample).reshape(windows.shape)</code> | Builds rounded signed reference entries, continuously indexed across windows. |
| 56 | <code>    sums = np.sum(windows.astype(np.int64) * ref.astype(np.int64), axis=1, dtype=np.int64)</code> | Promotes BOTH operands before multiplication, then accumulates in int64; this avoids int16 product overflow. |
| 57 | <code>    return LockInResult(start, end, center, accumulator_to_mm(sums, config), sums)</code> | Returns exact integer sums separately from the floating engineering-unit estimates. |

## src/lvdt_sim/metrics.py

Analysis only: these calculations describe accuracy. They are not part of the HDL multiply-and-accumulate input path.

Source snapshot SHA-256: `1e31c424fed2656c5f56a590a3aba7e7cc28b2d1e578c211da6184f2b365c5d9`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Numerical calibration, estimation error, and Monte Carlo summary metrics.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code></code> | Blank separator for readability; no operation. |
| 6 | <code></code> | Blank separator for readability; no operation. |
| 7 | <code>def error_metrics(truth: NDArray, estimate: NDArray) -&gt; dict[str, float]:</code> | Defines common error statistics for matching truth and estimate arrays. |
| 8 | <code>    a, b = np.asarray(truth, dtype=float), np.asarray(estimate, dtype=float)</code> | Converts truth and estimates into floating arrays. |
| 9 | <code>    if a.shape != b.shape or a.size == 0 or not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):</code> | Checks matching shapes, nonempty truth, and finite values on both sides. |
| 10 | <code>        raise ValueError(&quot;metrics require matching nonempty finite inputs&quot;)</code> | Rejects inputs that cannot define useful accuracy statistics. |
| 11 | <code>    e = b - a</code> | Computes signed error estimate minus truth. |
| 12 | <code>    return {&quot;bias_mm&quot;: float(np.mean(e)), &quot;rmse_mm&quot;: float(np.sqrt(np.mean(e**2))),</code> | Returns mean error (bias) and root mean squared error, converted to JSON-friendly Python floats. |
| 13 | <code>            &quot;mae_mm&quot;: float(np.mean(np.abs(e))), &quot;max_absolute_error_mm&quot;: float(np.max(np.abs(e))),</code> | Adds mean absolute error and largest absolute error. |
| 14 | <code>            &quot;std_mm&quot;: float(np.std(e))}</code> | Adds population standard deviation of the errors; this is spread around their mean, not RMSE. |
| 15 | <code></code> | Blank separator for readability; no operation. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code>def calibration(truth_mm: NDArray, estimate_mm: NDArray, sensitivity_v_per_mm: float) -&gt; dict[str, float]:</code> | Defines linear calibration/regression metrics. |
| 18 | <code>    result = error_metrics(truth_mm, estimate_mm)</code> | Starts with the shared estimation-error statistics. |
| 19 | <code>    x, y = np.asarray(truth_mm), np.asarray(estimate_mm)</code> | Names the independent true position x and measured position y. |
| 20 | <code>    if np.unique(x).size &lt; 2:</code> | Requires at least two distinct truth positions to fit a slope. |
| 21 | <code>        raise ValueError(&quot;Calibration requires at least two distinct positions&quot;)</code> | Rejects degenerate calibration data. |
| 22 | <code>    slope, offset = np.polyfit(x, y, 1)</code> | Fits y=slope*x+offset using a degree-one least-squares polynomial. |
| 23 | <code>    residual = np.sum((y - (slope*x + offset))**2)</code> | Sums squared residuals about the fitted line. |
| 24 | <code>    total = np.sum((y - np.mean(y))**2)</code> | Sums squared variation of y about its own mean. |
| 25 | <code>    result.update(slope_mm_per_mm=float(slope), offset_mm=float(offset),</code> | Adds displacement slope and displacement offset to the metrics dictionary. |
| 26 | <code>                  estimated_sensitivity_v_per_mm=float(slope * sensitivity_v_per_mm),</code> | Expresses the fitted slope as equivalent electrical sensitivity by multiplying by nominal K. |
| 27 | <code>                  r_squared=float(1 - residual/total) if total else 0.0)</code> | Computes R-squared; reports zero for constant y where the usual denominator vanishes. |
| 28 | <code>    return result</code> | Returns the merged calibration and error metrics. |

## src/lvdt_sim/export.py

File-format boundary. These functions preserve signed values as bit patterns and column ordering. They do not simulate physical signals.

Source snapshot SHA-256: `65cc79437089961b17451fd7cad8b06207d9dbd75b40f1553f92afd5d1ae3c86`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Strict signed-16 HEX and explicit ordered CSV/JSON data contracts.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>import csv</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 4 | <code>import json</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 6 | <code>import re</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 7 | <code>from collections.abc import Mapping, Sequence</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 9 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 10 | <code></code> | Blank separator for readability; no operation. |
| 11 | <code>GROUND_TRUTH_COLUMNS = [&quot;sample_index&quot;, &quot;time_s&quot;, &quot;displacement_mm&quot;, &quot;primary_voltage_v&quot;,</code> | Starts the exact ground-truth CSV header order: sample index, time, displacement, primary voltage. |
| 12 | <code>                        &quot;secondary_1_v&quot;, &quot;secondary_2_v&quot;, &quot;differential_voltage_v&quot;,</code> | Continues that header with both secondary voltages and their difference. |
| 13 | <code>                        &quot;measured_analog_voltage_v&quot;, &quot;adc_code&quot;]</code> | Finishes it with measured analog voltage and signed ADC code. |
| 14 | <code>EXPECTED_COLUMNS = [&quot;window_index&quot;, &quot;start_sample&quot;, &quot;end_sample&quot;, &quot;center_time_s&quot;,</code> | Starts the expected-result header order with window index, first/last index, and center time. |
| 15 | <code>                    &quot;expected_accumulator&quot;, &quot;estimated_displacement_mm&quot;, &quot;true_window_mean_mm&quot;, &quot;absolute_error_mm&quot;]</code> | Finishes with exact sum, estimated mm, arithmetic truth mean, and absolute error. |
| 16 | <code></code> | Blank separator for readability; no operation. |
| 17 | <code></code> | Blank separator for readability; no operation. |
| 18 | <code>def write_hex(path: str &#124; Path, values: NDArray) -&gt; None:</code> | Defines strict signed-16 HEX output. |
| 19 | <code>    a = np.asarray(values)</code> | Turns the values into an array so dimensions and type can be validated. |
| 20 | <code>    if a.ndim != 1 or a.dtype.kind not in &quot;iu&quot; or np.any(a &lt; -32768) or np.any(a &gt; 32767):</code> | Requires one-dimensional integer data in [-32768,32767]. |
| 21 | <code>        raise ValueError(&quot;HEX values must be a signed-16-range integer vector&quot;)</code> | Rejects truncation/wrapping and noninteger values. |
| 22 | <code>    path = Path(path)</code> | Converts the output filename to Path. |
| 23 | <code>    path.parent.mkdir(parents=True, exist_ok=True)</code> | Creates the parent directories if needed. |
| 24 | <code>    path.write_text(&quot;&quot;.join(f&quot;{int(v) &amp; 0xffff:04X}\n&quot; for v in a), encoding=&quot;ascii&quot;)</code> | Masks each signed integer to its low 16 bits, formats four uppercase HEX digits plus newline, and writes ASCII. |
| 25 | <code></code> | Blank separator for readability; no operation. |
| 26 | <code></code> | Blank separator for readability; no operation. |
| 27 | <code>def read_hex(path: str &#124; Path) -&gt; NDArray[np.int16]:</code> | Defines a strict HEX reader used for verification. |
| 28 | <code>    lines = Path(path).read_text(encoding=&quot;ascii&quot;).splitlines()</code> | Reads ASCII lines without retaining newline characters. |
| 29 | <code>    if any(not re.fullmatch(r&quot;[0-9a-fA-F]{4}&quot;, line) for line in lines):</code> | Requires exactly four hexadecimal characters on every line; upper/lower case are both accepted here. |
| 30 | <code>        raise ValueError(&quot;Each HEX line must contain exactly four hexadecimal characters&quot;)</code> | Rejects malformed words, prefixes, headers, or blank records. |
| 31 | <code>    words = [int(line, 16) for line in lines]</code> | Parses each line as an unsigned hexadecimal integer. |
| 32 | <code>    return np.array([w - 65536 if w &gt;= 32768 else w for w in words], dtype=np.int16)</code> | Interprets bit 15 as sign by subtracting 65536 for words >=32768; returns signed int16 values. |
| 33 | <code></code> | Blank separator for readability; no operation. |
| 34 | <code></code> | Blank separator for readability; no operation. |
| 35 | <code>def write_csv(path: str &#124; Path, columns: Mapping[str, Sequence]) -&gt; None:</code> | Defines ordered CSV output from a mapping of column names to equal-length sequences. |
| 36 | <code>    if not columns or len({len(v) for v in columns.values()}) != 1:</code> | Requires at least one named column and identical lengths for all columns; zero-length columns themselves are allowed. |
| 37 | <code>        raise ValueError(&quot;CSV columns must be nonempty and have matching lengths&quot;)</code> | Rejects a missing column mapping or mismatched lengths. |
| 38 | <code>    path = Path(path)</code> | Converts the CSV filename to Path. |
| 39 | <code>    path.parent.mkdir(parents=True, exist_ok=True)</code> | Creates the output parent directories. |
| 40 | <code>    with path.open(&quot;w&quot;, newline=&quot;&quot;, encoding=&quot;utf-8&quot;) as handle:</code> | Opens UTF-8 CSV with newline handling appropriate for the csv module on Windows/Linux. |
| 41 | <code>        writer = csv.writer(handle)</code> | Creates a CSV formatter attached to the open file. |
| 42 | <code>        writer.writerow(columns)</code> | Writes dictionary keys as the header, preserving insertion order. |
| 43 | <code>        writer.writerows(zip(*columns.values()))</code> | Transposes column arrays into rows using zip and writes all rows. |
| 44 | <code></code> | Blank separator for readability; no operation. |
| 45 | <code></code> | Blank separator for readability; no operation. |
| 46 | <code>def write_json(path: str &#124; Path, data: dict) -&gt; None:</code> | Defines JSON metadata/report output. |
| 47 | <code>    path = Path(path)</code> | Converts the filename to Path. |
| 48 | <code>    path.parent.mkdir(parents=True, exist_ok=True)</code> | Creates the output parent directories. |
| 49 | <code>    path.write_text(json.dumps(data, indent=2, allow_nan=False) + &quot;\n&quot;, encoding=&quot;utf-8&quot;)</code> | Writes indented UTF-8 JSON and a final newline; rejects nonstandard NaN/Infinity JSON values. |

## src/lvdt_sim/pipeline.py

System integration hub. run() connects physics to acquisition to numerical reference results; export_simulation() is the file handoff; standard_scenarios() is the scenario catalog.

Source snapshot SHA-256: `86105389686704d24a49eea77403408d54fa6642a72a395d3967792f19741af6`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;End-to-end independent simulation streams and self-describing HDL exports.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from dataclasses import dataclass, replace</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 6 | <code>from numpy.typing import NDArray</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code>from . import trajectories, sensor, noise, adc, reference, lockin_reference, export</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 9 | <code></code> | Blank separator for readability; no operation. |
| 10 | <code></code> | Blank separator for readability; no operation. |
| 11 | <code>@dataclass(frozen=True)</code> | Creates constructor/record behavior automatically and prevents reassigning fields; contained arrays/dictionaries remain mutable. |
| 12 | <code>class Simulation:</code> | Defines the Simulation record bundling a complete independently initialized stream. |
| 13 | <code>    config: Config</code> | Stores the exact effective configuration used by the run. |
| 14 | <code>    stream_id: int</code> | Stores the RNG stream ID used with the base seed. |
| 15 | <code>    time_s: NDArray</code> | Stores sample timestamps in seconds. |
| 16 | <code>    displacement_mm: NDArray</code> | Stores the true core displacement in mm. |
| 17 | <code>    sensor: sensor.SensorSignals</code> | Stores primary/secondary/differential sensor voltage arrays. |
| 18 | <code>    noise_components: dict[str, NDArray]</code> | Stores each additive measurement nonideality separately. |
| 19 | <code>    measured_v: NDArray</code> | Stores ADC-input voltage after all measurement additions. |
| 20 | <code>    adc: adc.ADCResult</code> | Stores digitized samples, reconstructed volts, and clipping information. |
| 21 | <code>    floating: lockin_reference.LockInResult</code> | Stores floating analog-reference measurements. |
| 22 | <code>    fixed: lockin_reference.LockInResult</code> | Stores bit-exact integer correlation results and their mm conversion. |
| 23 | <code>    true_window_mean_mm: NDArray</code> | Stores the arithmetic truth mean per complete window for diagnostic comparison. |
| 24 | <code></code> | Blank separator for readability; no operation. |
| 25 | <code></code> | Blank separator for readability; no operation. |
| 26 | <code>def run(config: Config, stream_id: int = 0) -&gt; Simulation:</code> | Defines the single-call simulation connector; no files are written by run itself. |
| 27 | <code>    t = trajectories.time_vector(config)</code> | Creates sample times n/fs. |
| 28 | <code>    x = trajectories.generate(config)</code> | Creates the chosen displacement trajectory. |
| 29 | <code>    signals = sensor.simulate(t, x, config)</code> | Transforms displacement into primary/secondary/differential voltages. |
| 30 | <code>    components = noise.components(t, config, stream_id)</code> | Generates deterministic noise and interference arrays for this independent stream. |
| 31 | <code>    measured = signals.differential_v + sum(components.values())</code> | Sums all voltage additions onto the clean differential signal. |
| 32 | <code>    digitized = adc.quantize(measured, config)</code> | Quantizes the measured voltage; clipping is handled and recorded by the ADC. |
| 33 | <code>    fp = lockin_reference.floating(measured, config)</code> | Runs floating correlation on the actual measured voltage, not reconstructed ADC voltage. |
| 34 | <code>    fx = lockin_reference.fixed(digitized.codes, config)</code> | Runs exact integer correlation on the ADC codes. |
| 35 | <code>    complete = len(fx.start_sample) * config.window_samples</code> | Counts how many samples belong to complete measurement windows. |
| 36 | <code>    mean = x[:complete].reshape(-1, config.window_samples).mean(axis=1)</code> | Reshapes those truth samples into windows and averages each row. |
| 37 | <code>    return Simulation(config, stream_id, t, x, signals, components, measured, digitized, fp, fx, mean)</code> | Returns all signals and measurements in one Simulation record. |
| 38 | <code></code> | Blank separator for readability; no operation. |
| 39 | <code></code> | Blank separator for readability; no operation. |
| 40 | <code>def export_simulation(sim: Simulation, output_dir: str &#124; Path, name: str = &quot;baseline&quot;) -&gt; dict[str, str]:</code> | Defines complete named-scenario export and returns directory paths. |
| 41 | <code>    &quot;&quot;&quot;Each named scenario is an independently reset stream with its own metadata.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 42 | <code>    if not name or Path(name).name != name or name in {&quot;.&quot;, &quot;..&quot;}:</code> | Requires a nonempty single directory name; disallows dot and parent-directory names. |
| 43 | <code>        raise ValueError(&quot;scenario name must be a single safe path component&quot;)</code> | Rejects an unsafe or nested scenario name. |
| 44 | <code>    root = Path(output_dir)</code> | Converts the requested output root to Path. |
| 45 | <code>    vectors, truth = root / &quot;vectors&quot; / name, root / &quot;ground_truth&quot; / name</code> | Builds parallel vectors/name and ground_truth/name output directories. |
| 46 | <code>    vectors.mkdir(parents=True, exist_ok=True)</code> | Creates the vector directory and any missing parents. |
| 47 | <code>    truth.mkdir(parents=True, exist_ok=True)</code> | Creates the truth directory and any missing parents. |
| 48 | <code>    c, fx = sim.config, sim.fixed</code> | Uses short local names for configuration and fixed-reference measurements. |
| 49 | <code>    export.write_hex(vectors / &quot;adc_samples.hex&quot;, sim.adc.codes)</code> | Writes the exact ADC integer sequence as signed-16 HEX words. |
| 50 | <code>    export.write_hex(vectors / &quot;reference_lut.hex&quot;, reference.sine_lut(c.lut_length))</code> | Writes the matching rounded reference LUT; this is the table HDL must consume. |
| 51 | <code>    columns = [np.arange(c.sample_count), sim.time_s, sim.displacement_mm, sim.sensor.primary_v,</code> | Begins the ordered ground-truth arrays with sample index, time, position, and primary voltage. |
| 52 | <code>               sim.sensor.secondary_1_v, sim.sensor.secondary_2_v, sim.sensor.differential_v,</code> | Continues those arrays with the two secondary voltages and their difference. |
| 53 | <code>               sim.measured_v, sim.adc.codes]</code> | Appends measured ADC-input volts and integer codes. |
| 54 | <code>    export.write_csv(truth / &quot;ground_truth.csv&quot;, dict(zip(export.GROUND_TRUTH_COLUMNS, columns)))</code> | Associates arrays with the fixed header names and writes ground_truth.csv. |
| 55 | <code>    expected = [np.arange(len(fx.start_sample)), fx.start_sample, fx.end_sample, fx.center_time_s,</code> | Begins expected-result arrays with window identity, sample boundaries, and center times. |
| 56 | <code>                fx.accumulator, fx.displacement_mm, sim.true_window_mean_mm,</code> | Appends exact integer sums, converted estimates, and arithmetic truth means. |
| 57 | <code>                np.abs(fx.displacement_mm - sim.true_window_mean_mm)]</code> | Computes absolute estimate-minus-truth-mean differences for diagnostics. |
| 58 | <code>    export.write_csv(vectors / &quot;expected_results.csv&quot;, dict(zip(export.EXPECTED_COLUMNS, expected)))</code> | Writes expected_results.csv in the documented column order. |
| 59 | <code>    limit = 1 &lt;&lt; (c.adc_bits - 1)</code> | Computes the configured maximum negative ADC code magnitude. |
| 60 | <code>    product_bound = limit * reference.Q_SCALE</code> | Computes a conservative product magnitude bound using the reference scale. |
| 61 | <code>    sum_bound = c.window_samples * product_bound</code> | Bounds N products by N times that magnitude. |
| 62 | <code>    metadata = {</code> | Starts the self-describing metadata object. |
| 63 | <code>        &quot;data_contract_version&quot;: &quot;1.0.0&quot;, &quot;configuration&quot;: c.to_dict(),</code> | Records the contract version and full effective configuration, including defaults. |
| 64 | <code>        &quot;units&quot;: {&quot;displacement&quot;: &quot;mm&quot;, &quot;voltage&quot;: &quot;V&quot;, &quot;time&quot;: &quot;s&quot;, &quot;frequency&quot;: &quot;Hz&quot;},</code> | Defines units explicitly for the exported physical quantities. |
| 65 | <code>        &quot;sampling_frequency_hz&quot;: c.fs_hz, &quot;excitation_frequency_hz&quot;: c.fc_hz,</code> | Records electrical sampling/carrier frequencies prominently. |
| 66 | <code>        &quot;adc&quot;: {&quot;nominal_bits&quot;: c.adc_bits, &quot;full_scale_v&quot;: c.adc_full_scale_v,</code> | Starts ADC metadata with resolution and full-scale input voltage. |
| 67 | <code>                &quot;code_min&quot;: -limit, &quot;code_max&quot;: limit-1, &quot;volts_per_code&quot;: c.adc_full_scale_v/limit,</code> | Records numerical ADC limits and volts-per-code conversion. |
| 68 | <code>                &quot;word_format&quot;: &quot;signed 16-bit two&#x27;s complement, four uppercase HEX characters&quot;,</code> | Documents the signed 16-bit container and textual HEX format. |
| 69 | <code>                &quot;rounding&quot;: &quot;numpy.rint, nearest ties to even&quot;,</code> | Documents the one shared rounding convention. |
| 70 | <code>                &quot;clipped_count&quot;: sim.adc.clipped_count, &quot;clipped_percent&quot;: sim.adc.clipped_percent,</code> | Records clipping count and percentage. |
| 71 | <code>                &quot;analog_overrange_count&quot;: int(np.count_nonzero(sim.adc.analog_overrange_mask))},</code> | Records physical analog overrange separately from rounded-code saturation. |
| 72 | <code>        &quot;reference&quot;: {&quot;length&quot;: c.lut_length, &quot;scale&quot;: reference.Q_SCALE, &quot;format&quot;: &quot;signed 16-bit Q1.14&quot;,</code> | Records LUT period, scale 16384, and signed Q1.14 format. |
| 73 | <code>                      &quot;initial_index&quot;: 0, &quot;phase&quot;: &quot;continuous across windows; advance only on accepted samples&quot;},</code> | Records initial index zero and reference advancement on accepted samples only. |
| 74 | <code>        &quot;window_samples&quot;: c.window_samples, &quot;number_of_samples&quot;: c.sample_count,</code> | Records measurement-window size and total input sample count. |
| 75 | <code>        &quot;number_of_windows&quot;: len(fx.start_sample), &quot;discarded_trailing_samples&quot;: c.sample_count % c.window_samples,</code> | Records completed result count and discarded trailing-sample count. |
| 76 | <code>        &quot;end_sample_convention&quot;: &quot;inclusive&quot;, &quot;timestamp&quot;: &quot;midpoint of first and last accepted sample times&quot;,</code> | Defines inclusive end indices and midpoint timestamp convention. |
| 77 | <code>        &quot;random_seed&quot;: c.seed, &quot;rng_stream_id&quot;: sim.stream_id, &quot;rng&quot;: &quot;default_rng(SeedSequence([seed, stream_id]))&quot;,</code> | Records enough RNG information to reproduce a scenario independently. |
| 78 | <code>        &quot;width_bounds&quot;: {&quot;maximum_absolute_product&quot;: product_bound, &quot;conservative_absolute_sum&quot;: sum_bound,</code> | Begins integer-width metadata with product and conservative sum bounds. |
| 79 | <code>                         &quot;minimum_signed_accumulator_bits&quot;: sum_bound.bit_length()+1,</code> | Computes signed storage bits as magnitude bit length plus one sign bit. |
| 80 | <code>                         &quot;recommended_accumulator_bits&quot;: max(40, sum_bound.bit_length()+1)},</code> | Recommends at least 40 bits, or more when the custom bound requires them. |
| 81 | <code>        &quot;ground_truth_columns&quot;: export.GROUND_TRUTH_COLUMNS, &quot;expected_results_columns&quot;: export.EXPECTED_COLUMNS,</code> | Records both exact CSV column orders in metadata. |
| 82 | <code>        &quot;known_limitations&quot;: [&quot;single in-phase channel has cosine phase error&quot;, &quot;coherent interference is inseparable&quot;,</code> | Begins scientific limitations: in-phase cosine phase error and inseparable coherent interference. |
| 83 | <code>                              &quot;changing motion is sine-squared weighted within a window; arithmetic truth mean is diagnostic&quot;,</code> | Clarifies the difference between dynamic weighted estimates and arithmetic truth means. |
| 84 | <code>                              &quot;rectangular windows cause frequency leakage&quot;, &quot;analog-equivalent sampled model; no analog anti-alias filter&quot;,</code> | Records rectangular-window leakage and absence of an analog anti-alias filter. |
| 85 | <code>                              &quot;ADC quantization and saturation; positive full scale is asymmetric&quot;,</code> | Records quantization, saturation, and asymmetric positive ADC limit. |
| 86 | <code>                              &quot;cubic nonlinearity is not inverted by the linear estimator&quot;,</code> | Records that linear mm conversion does not invert optional cubic physics. |
| 87 | <code>                              &quot;non-integral-cycle windows can have gain ripple and DC leakage&quot;],</code> | Warns of gain/DC leakage with non-integral-cycle measurement windows. |
| 88 | <code>    }</code> | Closes the multi-line container or expression opened above. |
| 89 | <code>    export.write_json(vectors / &quot;metadata.json&quot;, metadata)</code> | Writes the completed metadata.json next to the HDL vectors. |
| 90 | <code>    return {&quot;vectors&quot;: str(vectors), &quot;ground_truth&quot;: str(truth)}</code> | Returns the two output directories as strings for callers. |
| 91 | <code></code> | Blank separator for readability; no operation. |
| 92 | <code></code> | Blank separator for readability; no operation. |
| 93 | <code>def standard_scenarios(base: Config &#124; None = None) -&gt; dict[str, Config]:</code> | Defines the standard reproducible ten-scenario catalog. |
| 94 | <code>    &quot;&quot;&quot;Clean default instruments; override only common acquisition/physics with base.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 95 | <code></code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 96 | <code>    Scenario-specific noise and trajectories are explicit to prevent accidental</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 97 | <code>    contamination of baseline cases by a noisy configuration.</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 98 | <code>    &quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 99 | <code>    c = base or Config()</code> | Uses the provided base instrument configuration, or creates defaults when absent. |
| 100 | <code>    clean = replace(c, noise_std_v=0, hum_peak_v=0, dc_offset_v=0, interference_peak_v=0,</code> | Copies the base configuration and zeroes Gaussian noise, hum, DC, and extra interference. |
| 101 | <code>                    drift_peak_v=0, phase_deg=0, cubic_v_per_mm3=0)</code> | Also disables drift, phase mismatch, and cubic terms for clean scenario baselines. |
| 102 | <code>    def static(x: float, **kwargs) -&gt; Config:</code> | Defines a small helper to create a static-displacement Config with explicit overrides. |
| 103 | <code>        return replace(clean, trajectory={&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: x}, **kwargs)</code> | Copies the clean config, selecting the constant displacement and any scenario-specific overrides. |
| 104 | <code>    return {</code> | Returns an ordered dictionary of scenario names to validated configurations. |
| 105 | <code>        &quot;null&quot;: static(0), &quot;positive&quot;: static(2), &quot;negative&quot;: static(-2),</code> | Defines null, positive +2 mm, and negative -2 mm baseline cases. |
| 106 | <code>        &quot;calibration&quot;: replace(clean, duration_s=11*5*c.window_samples/c.fs_hz,</code> | Sets calibration duration from 11 positions * 5 windows * N/fs. |
| 107 | <code>                               trajectory={&quot;mode&quot;: &quot;calibration&quot;, &quot;values_mm&quot;: list(range(-5, 6)), &quot;hold_windows&quot;: 5}),</code> | Selects every integer position -5 through +5, each held five windows. |
| 108 | <code>        &quot;high_noise&quot;: static(2, noise_std_v=.4, hum_peak_v=.1),</code> | Defines +2 mm with sigma=0.4 V Gaussian noise and 0.1 Vpeak hum. |
| 109 | <code>        &quot;step&quot;: replace(clean, trajectory={&quot;mode&quot;: &quot;step&quot;, &quot;before_mm&quot;: -3, &quot;after_mm&quot;: 3, &quot;step_s&quot;: c.duration_s/2}),</code> | Defines a -3 to +3 mm step halfway through the base duration. |
| 110 | <code>        &quot;sinusoidal&quot;: replace(clean, trajectory={&quot;mode&quot;: &quot;sine&quot;, &quot;amplitude_mm&quot;: 3, &quot;frequency_hz&quot;: 2}),</code> | Defines a 3 mm amplitude, 2 Hz mechanical sinusoid. |
| 111 | <code>        &quot;phase_mismatch&quot;: static(2, phase_deg=45),</code> | Defines +2 mm with an uncompensated 45-degree sensor phase. |
| 112 | <code>        &quot;adc_overrange&quot;: static(2, interference_peak_v=3, interference_hz=c.fc_hz),</code> | Defines a large 3 Vpeak coherent interferer to force ADC saturation. |
| 113 | <code>        &quot;same_frequency_interference&quot;: static(2, interference_peak_v=.24, interference_hz=c.fc_hz),</code> | Defines a 0.24 Vpeak coherent interferer to demonstrate displacement ambiguity. |
| 114 | <code>    }</code> | Closes the multi-line container or expression opened above. |

## src/lvdt_sim/validation.py

Engineering experiments for the default instrument, not a configurable replacement for pipeline.run. Several constants (20, 200, .24, .48) deliberately represent the baseline study; update these studies if you redefine that baseline.

Source snapshot SHA-256: `d2e4fa0728189ce6fbd35b9d1f4f38a3274136efa35e1ada6eda683ffdf6a3c9`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Reproducible engineering studies with explicit numerical acceptance checks.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from dataclasses import replace</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 5 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 6 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 7 | <code>from .pipeline import run, standard_scenarios</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 8 | <code>from .adc import quantize</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 9 | <code>from .lockin_reference import fixed</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 10 | <code>from .noise import gaussian</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 11 | <code>from .metrics import calibration, error_metrics</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 12 | <code>from .export import write_json, write_csv</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 13 | <code></code> | Blank separator for readability; no operation. |
| 14 | <code></code> | Blank separator for readability; no operation. |
| 15 | <code>def studies(output_dir: str &#124; Path, trials: int = 1000) -&gt; dict:</code> | Defines the numerical-study runner and chooses 1000 Monte Carlo trials per noise level by default. |
| 16 | <code>    &quot;&quot;&quot;Monte Carlo uses one independent 200-sample observation per trial.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 17 | <code>    if type(trials) is not int or trials &lt; 200:</code> | Requires an integer trial count of at least 200. |
| 18 | <code>        raise ValueError(&quot;At least 200 Monte Carlo trials are required&quot;)</code> | Rejects a statistically too-small requested run. |
| 19 | <code>    out = Path(output_dir) / &quot;reports&quot;</code> | Selects the reports directory below the supplied output root. |
| 20 | <code>    out.mkdir(parents=True, exist_ok=True)</code> | Creates that directory when absent. |
| 21 | <code>    c = Config(duration_s=.01)</code> | Creates the default instrument with one 10 ms, 200-sample observation. |
| 22 | <code>    checks = []</code> | Starts the acceptance-check record list. |
| 23 | <code>    def require(name: str, condition: bool) -&gt; None:</code> | Defines a local named-check helper. |
| 24 | <code>        checks.append({&quot;name&quot;: name, &quot;passed&quot;: bool(condition)})</code> | Records each condition as a plain boolean for JSON. |
| 25 | <code>        if not condition:</code> | Checks whether the numerical acceptance condition failed. |
| 26 | <code>            raise RuntimeError(f&quot;Numerical validation failed: {name}&quot;)</code> | Raises immediately on failure so the CLI cannot report a successful study. |
| 27 | <code></code> | Blank separator for readability; no operation. |
| 28 | <code>    static_results = []</code> | Starts the static-position report list. |
| 29 | <code>    for x in (0, 2, -2):</code> | Runs the null, positive, and negative baseline positions. |
| 30 | <code>        sim = run(replace(c, trajectory={&quot;mode&quot;: &quot;static&quot;, &quot;value_mm&quot;: x}))</code> | Copies the instrument with each static displacement, then runs the full pipeline. |
| 31 | <code>        estimate = float(sim.fixed.displacement_mm[0])</code> | Reads the first fixed-reference displacement as a plain float. |
| 32 | <code>        static_results.append({&quot;true_mm&quot;: x, &quot;float_mm&quot;: float(sim.floating.displacement_mm[0]),</code> | Begins a report record containing truth and floating-reference estimate. |
| 33 | <code>                               &quot;fixed_mm&quot;: estimate, &quot;absolute_error_mm&quot;: abs(estimate-x),</code> | Adds fixed estimate and its absolute error. |
| 34 | <code>                               &quot;accumulator&quot;: int(sim.fixed.accumulator[0])})</code> | Adds the exact integer accumulator; it is not serialized as a float. |
| 35 | <code>        require(f&quot;static {x} mm&quot;, abs(estimate-x) &lt; .003)</code> | Requires each fixed estimate to be within 0.003 mm of its truth. |
| 36 | <code>    cal = run(standard_scenarios()[&quot;calibration&quot;])</code> | Runs the catalog's full calibration sweep. |
| 37 | <code>    cal_metrics = calibration(cal.true_window_mean_mm, cal.fixed.displacement_mm, .24)</code> | Fits accuracy/regression metrics using nominal K=0.24 Vpeak/mm. |
| 38 | <code>    require(&quot;calibration linearity&quot;, cal_metrics[&quot;r_squared&quot;] &gt; .999999 and cal_metrics[&quot;max_absolute_error_mm&quot;] &lt; .003)</code> | Requires near-perfect linearity and maximum error below 0.003 mm. |
| 39 | <code>    write_csv(out / &quot;calibration.csv&quot;, {&quot;true_mm&quot;: cal.true_window_mean_mm,</code> | Starts writing calibration truth positions to CSV. |
| 40 | <code>                                      &quot;estimated_mm&quot;: cal.fixed.displacement_mm})</code> | Adds matching fixed estimates to that CSV. |
| 41 | <code>    n = np.arange(c.window_samples)</code> | Creates within-window sample indices. |
| 42 | <code>    clean = .48 * np.sin(2*np.pi*n/20)</code> | Creates the clean +2 mm voltage waveform: 0.24*2=0.48 Vpeak at 20 samples per cycle. |
| 43 | <code>    noise_results = []</code> | Starts per-noise-level summary results. |
| 44 | <code>    distribution = {&quot;sigma_v&quot;: [], &quot;trial_index&quot;: [], &quot;estimated_mm&quot;: []}</code> | Starts raw Monte Carlo CSV columns for every trial estimate. |
| 45 | <code>    for level, sigma in enumerate((0, .05, .1, .2, .4)):</code> | Enumerates five Gaussian noise standard deviations. |
| 46 | <code>        v = np.tile(clean, trials) + gaussian(trials*200, sigma, c.seed, 10000+level)</code> | Repeats the clean window trials times and adds independently drawn Gaussian samples from a level-specific stream. |
| 47 | <code>        digitized = quantize(v, c)</code> | Quantizes every trial sample with the actual ADC model. |
| 48 | <code>        estimates = fixed(digitized.codes, c).displacement_mm</code> | Demodulates the complete code sequence to obtain one estimate per trial window. |
| 49 | <code>        metrics = error_metrics(np.full(trials, 2.0), estimates)</code> | Compares each trial estimate to the +2 mm truth. |
| 50 | <code>        theory = sigma / (c.sensitivity_v_per_mm*np.sqrt(c.window_samples/2))</code> | Computes ideal unclipped white-noise standard deviation sigma/(K*sqrt(N/2)). |
| 51 | <code>        metrics.update(sigma_v=sigma, trials=trials, theoretical_std_mm=float(theory),</code> | Adds noise strength, trial count, and theoretical spread to summary metrics. |
| 52 | <code>                       mean_estimate_mm=float(np.mean(estimates)),</code> | Adds the mean measured displacement. |
| 53 | <code>                       mean_95_percent_halfwidth_mm=float(1.96*np.std(estimates, ddof=1)/np.sqrt(trials)),</code> | Computes a normal-approximation 95% mean-confidence halfwidth using sample std (ddof=1). |
| 54 | <code>                       clipped_count=digitized.clipped_count)</code> | Records any clipping over the full trial batch. |
| 55 | <code>        noise_results.append(metrics)</code> | Stores this noise level's completed metrics. |
| 56 | <code>        require(f&quot;Monte Carlo sigma={sigma} bias&quot;, abs(metrics[&quot;bias_mm&quot;]) &lt; 5*theory/np.sqrt(trials)+.003)</code> | Checks bias against a generous five-standard-error allowance plus 0.003 mm quantization allowance. |
| 57 | <code>        if sigma:</code> | Only positive sigma has nonzero theoretical random spread. |
| 58 | <code>            require(f&quot;Monte Carlo sigma={sigma} variance&quot;, abs(metrics[&quot;std_mm&quot;]-theory) &lt; .15*theory)</code> | Requires measured standard deviation to be within 15% of unclipped theory. |
| 59 | <code>        distribution[&quot;sigma_v&quot;].extend([sigma]*trials)</code> | Appends this sigma value once per trial in the raw distribution CSV. |
| 60 | <code>        distribution[&quot;trial_index&quot;].extend(range(trials))</code> | Appends trial numbers 0 through trials-1. |
| 61 | <code>        distribution[&quot;estimated_mm&quot;].extend(estimates)</code> | Appends all trial estimates, preserving trial order. |
| 62 | <code>    write_csv(out / &quot;monte_carlo_trials.csv&quot;, distribution)</code> | Writes all raw Monte Carlo trial results. |
| 63 | <code>    write_csv(out / &quot;noise_summary.csv&quot;, {key: [row[key] for row in noise_results] for key in noise_results[0]})</code> | Transposes summary dictionaries into CSV columns and writes one row per noise level. |
| 64 | <code>    phase_results = []</code> | Starts phase-sensitivity results. |
| 65 | <code>    for phase in (0, 15, 30, 45, 90):</code> | Selects five sensor phases, including quadrature at 90 degrees. |
| 66 | <code>        s = run(replace(c, phase_deg=phase))</code> | Runs the +2 mm sensor with each phase. |
| 67 | <code>        expected = 2*np.cos(np.deg2rad(phase))</code> | Computes the expected single-channel cosine response. |
| 68 | <code>        phase_results.append({&quot;phase_deg&quot;: phase, &quot;expected_mm&quot;: float(expected),</code> | Starts the phase result with phase angle and ideal response. |
| 69 | <code>                              &quot;floating_mm&quot;: float(s.floating.displacement_mm[0]),</code> | Adds the floating-reference estimate. |
| 70 | <code>                              &quot;fixed_mm&quot;: float(s.fixed.displacement_mm[0])})</code> | Adds the quantized fixed-reference estimate. |
| 71 | <code>        require(f&quot;phase {phase} cosine response&quot;, abs(s.floating.displacement_mm[0]-expected) &lt; 1e-12)</code> | Checks the floating result follows cosine dependence within numerical precision. |
| 72 | <code>    interference = []</code> | Starts narrowband interference results. |
| 73 | <code>    for frequency in (400, 950, 1000, 1050, 1600):</code> | Selects five interfering frequencies below, near, at, and above the carrier. |
| 74 | <code>        # 1 s demonstrates the beating of nearby tones across 100 windows.</code> | Explanatory comment for the following code; Python does not execute it. |
| 75 | <code>        s = run(replace(c, duration_s=1, interference_peak_v=.24, interference_hz=frequency,</code> | Runs one second with a 0.24 Vpeak interferer at the chosen frequency. |
| 76 | <code>                        interference_phase_deg=30))</code> | Sets its electrical phase to 30 degrees, making nearby-tone leakage visible across windows. |
| 77 | <code>        error = s.floating.displacement_mm - 2</code> | Computes each floating-reference estimate's signed error from +2 mm. |
| 78 | <code>        interference.append({&quot;frequency_hz&quot;: frequency, &quot;interference_phase_deg&quot;: 30,</code> | Starts an interference result recording tone frequency and phase. |
| 79 | <code>                             &quot;mean_bias_mm&quot;: float(error.mean()), &quot;rms_error_mm&quot;: float(np.sqrt(np.mean(error**2))),</code> | Adds the mean bias and root mean squared error across windows. |
| 80 | <code>                             &quot;max_absolute_error_mm&quot;: float(np.max(np.abs(error)))})</code> | Adds the largest absolute window error. |
| 81 | <code>        if frequency == 1000:</code> | Selects the special same-carrier-frequency case. |
| 82 | <code>            require(&quot;same-frequency interference bias&quot;, abs(error.mean()-np.cos(np.pi/6)) &lt; 1e-12)</code> | Verifies persistent bias equals cos(30 degrees) mm; correlation cannot reject this projection. |
| 83 | <code>    dynamic = run(standard_scenarios()[&quot;sinusoidal&quot;])</code> | Runs the standard moving sinusoidal trajectory. |
| 84 | <code>    ref = np.sin(2*np.pi*np.arange(dynamic.config.sample_count)/20)</code> | Builds the baseline floating carrier reference across the whole stream. |
| 85 | <code>    weighted = (2*dynamic.displacement_mm*ref**2).reshape(-1, 200).mean(axis=1)</code> | Computes ideal dynamic sine-squared-weighted position independently, window by window. |
| 86 | <code>    require(&quot;dynamic sine-squared window interpretation&quot;, np.max(np.abs(dynamic.floating.displacement_mm-weighted)) &lt; 2e-12)</code> | Checks floating demodulation matches that weighted interpretation, not an assumed instantaneous position. |
| 87 | <code>    dc = run(replace(c, dc_offset_v=.6))</code> | Runs a clean +2 mm signal with 0.6 V additive DC. |
| 88 | <code>    require(&quot;complete-cycle DC rejection&quot;, abs(dc.floating.displacement_mm[0]-2) &lt; 1e-12)</code> | Checks complete-cycle coherent averaging suppresses the DC component. |
| 89 | <code>    over = run(standard_scenarios()[&quot;adc_overrange&quot;])</code> | Runs the intentionally saturated ADC scenario. |
| 90 | <code>    require(&quot;overrange reported&quot;, over.adc.clipped_count &gt; 0)</code> | Requires nonzero clipping statistics. |
| 91 | <code>    rng = np.random.default_rng(99)</code> | Creates a separate deterministic generator for the integer-reference check. |
| 92 | <code>    codes = rng.integers(-2048, 2048, size=400, dtype=np.int16)</code> | Draws 400 valid signed ADC samples across the full default numerical range. |
| 93 | <code>    # Deliberately independent scalar integer correlation.</code> | Explanatory comment for the following code; Python does not execute it. |
| 94 | <code>    from .reference import sine_lut</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 95 | <code>    lut = [int(x) for x in sine_lut()]</code> | Converts LUT coefficients to arbitrary-precision Python ints for an independent scalar calculation. |
| 96 | <code>    expected_sums = [sum(int(codes[i])*lut[i % 20] for i in range(start, start+200)) for start in (0, 200)]</code> | Computes two exact 200-product sums with Python integer multiplication/addition and continuous LUT indices. |
| 97 | <code>    require(&quot;exact independent integer accumulators&quot;, np.array_equal(fixed(codes, c).accumulator, expected_sums))</code> | Requires NumPy's integer correlation sums to match the independent loop exactly. |
| 98 | <code>    report = {&quot;status&quot;: &quot;passed&quot;, &quot;seed&quot;: c.seed, &quot;trials_per_noise_level&quot;: trials,</code> | Starts the final machine-readable report with status, seed, and trial count. |
| 99 | <code>              &quot;static&quot;: static_results, &quot;calibration&quot;: cal_metrics, &quot;noise&quot;: noise_results,</code> | Attaches static, calibration, and Monte Carlo study results. |
| 100 | <code>              &quot;phase&quot;: phase_results, &quot;interference&quot;: interference,</code> | Attaches phase and interference study results. |
| 101 | <code>              &quot;dynamic&quot;: error_metrics(dynamic.true_window_mean_mm, dynamic.fixed.displacement_mm),</code> | Adds dynamic accuracy relative to the arithmetic truth mean as a diagnostic. |
| 102 | <code>              &quot;overrange_clipped_count&quot;: over.adc.clipped_count, &quot;checks&quot;: checks}</code> | Attaches overrange clipping count and all named acceptance checks. |
| 103 | <code>    write_json(out / &quot;validation.json&quot;, report)</code> | Writes validation.json. |
| 104 | <code>    lines = [&quot;# Phase 1 numerical validation&quot;, &quot;&quot;, f&quot;All {len(checks)} numerical checks passed; seed 42.&quot;, &quot;&quot;,</code> | Starts Markdown report text with heading and total check count. |
| 105 | <code>             &quot;## Static positions&quot;, &quot;&quot;, &quot;&#124; Truth (mm) &#124; Fixed estimate (mm) &#124; Absolute error (mm) &#124; Integer sum &#124;&quot;,</code> | Adds the static-position table heading and column names. |
| 106 | <code>             &quot;&#124;---:&#124;---:&#124;---:&#124;---:&#124;&quot;]</code> | Adds the Markdown table alignment row. |
| 107 | <code>    lines += [f&quot;&#124; {r[&#x27;true_mm&#x27;]} &#124; {r[&#x27;fixed_mm&#x27;]:.9f} &#124; {r[&#x27;absolute_error_mm&#x27;]:.9f} &#124; {r[&#x27;accumulator&#x27;]} &#124;&quot; for r in static_results]</code> | Formats one static result row with nine decimal places and exact integer sum. |
| 108 | <code>    lines += [&quot;&quot;, &quot;## Calibration&quot;, &quot;&quot;] + [f&quot;- {k}: {v:.12g}&quot; for k, v in cal_metrics.items()]</code> | Adds all calibration metrics with twelve significant figures. |
| 109 | <code>    lines += [&quot;&quot;, f&quot;## Gaussian Monte Carlo ({trials} independent windows per level)&quot;, &quot;&quot;,</code> | Starts the Monte Carlo section including the trial count. |
| 110 | <code>              &quot;&#124; Sigma (V) &#124; Bias (mm) &#124; RMSE (mm) &#124; Std (mm) &#124; Theory std (mm) &#124;&quot;, &quot;&#124;---:&#124;---:&#124;---:&#124;---:&#124;---:&#124;&quot;]</code> | Defines the noise summary table headings/alignment. |
| 111 | <code>    lines += [f&quot;&#124; {r[&#x27;sigma_v&#x27;]} &#124; {r[&#x27;bias_mm&#x27;]:.7f} &#124; {r[&#x27;rmse_mm&#x27;]:.7f} &#124; {r[&#x27;std_mm&#x27;]:.7f} &#124; {r[&#x27;theoretical_std_mm&#x27;]:.7f} &#124;&quot; for r in noise_results]</code> | Formats noise-level bias, RMSE, std, and theory into report rows. |
| 112 | <code>    lines += [&quot;&quot;, &quot;## Interference (0.24 Vpeak, 30 degree phase)&quot;, &quot;&quot;,</code> | Starts the interference section, documenting the tested amplitude and phase. |
| 113 | <code>              &quot;&#124; Frequency (Hz) &#124; Mean bias (mm) &#124; RMS error (mm) &#124;&quot;, &quot;&#124;---:&#124;---:&#124;---:&#124;&quot;]</code> | Defines its frequency/bias/RMS table headings. |
| 114 | <code>    lines += [f&quot;&#124; {r[&#x27;frequency_hz&#x27;]} &#124; {r[&#x27;mean_bias_mm&#x27;]:.7f} &#124; {r[&#x27;rms_error_mm&#x27;]:.7f} &#124;&quot; for r in interference]</code> | Formats each interference result. |
| 115 | <code>    lines += [&quot;&quot;, &quot;Near-carrier interference beats across windows. Same-frequency interference persists as a signed projection.&quot;,</code> | Adds the scientific interpretation of nearby beating and persistent coherent projection. |
| 116 | <code>              &quot;No phase correction, noise removal guarantee, or hardware accuracy claim is implied.&quot;, &quot;&quot;]</code> | Adds a reminder that these results are not universal noise rejection or hardware-accuracy guarantees. |
| 117 | <code>    (out / &quot;validation.md&quot;).write_text(&quot;\n&quot;.join(lines), encoding=&quot;utf-8&quot;)</code> | Joins the Markdown lines with newlines and writes UTF-8 validation.md. |
| 118 | <code>    return report</code> | Returns the report dictionary so scripts/plotting can reuse the same results. |

## src/lvdt_sim/diagnostics.py

Plotting only. It creates its own baseline demonstration signals and uses numerical-study metrics for noise/phase plots; it does not read a custom scenario's exported CSV.

Source snapshot SHA-256: `8dd9f7d50e42f0501af6c2445aff072d1b036c7d1113b30c0589ffb2c44a36a0`.

| Line | Original source | Explanation |
|---:|---|---|
| 1 | <code>&quot;&quot;&quot;Headless static engineering diagnostics; no GUI or interactive dashboard.&quot;&quot;&quot;</code> | Documentation text (a docstring), explaining the module/function/model; it does not perform a calculation. |
| 2 | <code></code> | Blank separator for readability; no operation. |
| 3 | <code>from pathlib import Path</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 4 | <code>import matplotlib</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 5 | <code>matplotlib.use(&quot;Agg&quot;)</code> | Selects the noninteractive Agg raster backend before importing pyplot; no GUI window is opened. |
| 6 | <code>import matplotlib.pyplot as plt</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 7 | <code>import numpy as np</code> | Loads the named library/module; 'as' supplies its shorter local name (np for NumPy, plt for plotting). |
| 8 | <code>from .config import Config</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 9 | <code>from .pipeline import run, standard_scenarios</code> | Imports the listed names from this module. A leading dot refers to another module in the same lvdt_sim package. |
| 10 | <code></code> | Blank separator for readability; no operation. |
| 11 | <code></code> | Blank separator for readability; no operation. |
| 12 | <code>def generate(output_dir: str &#124; Path, report: dict) -&gt; list[str]:</code> | Defines the eight-PNG diagnostic generator and returns saved filenames. |
| 13 | <code>    root = Path(output_dir) / &quot;diagnostics&quot;</code> | Chooses an output diagnostics subdirectory. |
| 14 | <code>    root.mkdir(parents=True, exist_ok=True)</code> | Creates the directory and parents if needed. |
| 15 | <code>    paths = []</code> | Starts the saved-path list. |
| 16 | <code>    def save(name: str, title: str, xlabel: str, ylabel: str) -&gt; None:</code> | Defines a local helper that labels, saves, closes, and records the current plot. |
| 17 | <code>        plt.title(title)</code> | Sets the figure title. |
| 18 | <code>        plt.xlabel(xlabel)</code> | Labels the horizontal axis. |
| 19 | <code>        plt.ylabel(ylabel)</code> | Labels the vertical axis. |
| 20 | <code>        plt.grid(alpha=.3)</code> | Adds a lightly transparent grid. |
| 21 | <code>        plt.legend()</code> | Shows labels of plotted traces in a legend. |
| 22 | <code>        plt.tight_layout()</code> | Adjusts margins to fit labels. |
| 23 | <code>        path = root / f&quot;{name}.png&quot;</code> | Builds the PNG filename. |
| 24 | <code>        plt.savefig(path, dpi=160)</code> | Saves the current figure at 160 dots per inch. |
| 25 | <code>        plt.close()</code> | Closes it to release plotting resources. |
| 26 | <code>        paths.append(str(path))</code> | Records its path in the return list. |
| 27 | <code>    s = run(Config(duration_s=.02, noise_std_v=.2, hum_peak_v=.1))</code> | Creates a short +2 mm demonstration with Gaussian noise and hum. |
| 28 | <code>    short = slice(0, 100)</code> | Selects the first 100 samples (5 ms). |
| 29 | <code>    ms = s.time_s[short]*1000</code> | Converts those sample times from seconds to milliseconds. |
| 30 | <code>    plt.figure(figsize=(9, 4))</code> | Creates the winding-voltage figure, nine by four inches. |
| 31 | <code>    for name, values in ((&quot;Primary&quot;, s.sensor.primary_v), (&quot;Secondary 1&quot;, s.sensor.secondary_1_v), (&quot;Secondary 2&quot;, s.sensor.secondary_2_v)):</code> | Iterates over primary, secondary 1, and secondary 2 voltage traces. |
| 32 | <code>        plt.plot(ms, values[short], label=name)</code> | Plots each selected trace versus time with its legend label. |
| 33 | <code>    save(&quot;01_windings&quot;, &quot;LVDT winding voltages at +2 mm&quot;, &quot;Time (ms)&quot;, &quot;Voltage (V)&quot;)</code> | Saves winding voltages with explicit units. |
| 34 | <code>    plt.figure(figsize=(9, 4))</code> | Creates the differential-voltage figure. |
| 35 | <code>    plt.plot(ms, s.sensor.differential_v[short], label=&quot;V1 - V2&quot;)</code> | Plots the clean V1-V2 trace. |
| 36 | <code>    save(&quot;02_differential&quot;, &quot;Differential sensor output&quot;, &quot;Time (ms)&quot;, &quot;Voltage (V)&quot;)</code> | Saves the differential plot. |
| 37 | <code>    plt.figure(figsize=(9, 4))</code> | Creates the clean/noisy comparison figure. |
| 38 | <code>    plt.plot(ms, s.measured_v[short], label=&quot;Measured (noise + hum)&quot;, alpha=.8)</code> | Plots measured ADC-input voltage with slightly transparent color. |
| 39 | <code>    plt.plot(ms, s.sensor.differential_v[short], label=&quot;Clean&quot;)</code> | Overlays the ideal clean differential voltage. |
| 40 | <code>    save(&quot;03_clean_noisy&quot;, &quot;Additive measurement interference&quot;, &quot;Time (ms)&quot;, &quot;Voltage (V)&quot;)</code> | Saves the measurement-interference comparison. |
| 41 | <code>    plt.figure(figsize=(9, 4))</code> | Creates the quantization-error figure. |
| 42 | <code>    plt.plot(s.time_s*1000, (s.adc.reconstructed_v-s.measured_v)*1000, &quot;.&quot;, label=&quot;ADC reconstruction error&quot;, markersize=3)</code> | Plots reconstructed ADC volts minus input volts, converting time/error to ms/mV. |
| 43 | <code>    half_lsb = s.config.adc_full_scale_v/2048/2*1000</code> | Calculates the default ADC half-LSB in mV; this demonstration assumes the default 12-bit ADC. |
| 44 | <code>    plt.axhline(half_lsb, color=&quot;red&quot;, linestyle=&quot;--&quot;, label=&quot;+/- half LSB&quot;)</code> | Draws a labeled positive half-LSB error bound. |
| 45 | <code>    plt.axhline(-half_lsb, color=&quot;red&quot;, linestyle=&quot;--&quot;)</code> | Draws the corresponding negative bound without duplicating the legend label. |
| 46 | <code>    save(&quot;04_quantization&quot;, &quot;Quantization error (no saturation in this trace)&quot;, &quot;Time (ms)&quot;, &quot;Error (mV)&quot;)</code> | Saves the unsaturated quantization-error demonstration. |
| 47 | <code>    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)</code> | Creates stacked sinusoidal and step plots with a shared time axis. |
| 48 | <code>    configs = standard_scenarios()</code> | Gets the default standard-scenario configurations. |
| 49 | <code>    for ax, name in zip(axes, (&quot;sinusoidal&quot;, &quot;step&quot;)):</code> | Pairs the two axes with sinusoidal and step scenario names. |
| 50 | <code>        d = run(configs[name])</code> | Runs the selected dynamic case. |
| 51 | <code>        ax.plot(d.time_s, d.displacement_mm, label=&quot;True trajectory&quot;)</code> | Plots the true continuous-in-time sampled displacement. |
| 52 | <code>        ax.plot(d.fixed.center_time_s, d.fixed.displacement_mm, &quot;.&quot;, label=&quot;Fixed estimate at window center&quot;)</code> | Plots fixed estimates at their measurement-window center times. |
| 53 | <code>        ax.set_ylabel(&quot;Displacement (mm)&quot;)</code> | Labels position in millimeters. |
| 54 | <code>        ax.set_title(name.capitalize())</code> | Titles the subplot from its scenario name. |
| 55 | <code>        ax.grid(alpha=.3)</code> | Adds a light grid to the subplot. |
| 56 | <code>        ax.legend()</code> | Adds its trace legend. |
| 57 | <code>    axes[-1].set_xlabel(&quot;Time (s)&quot;)</code> | Labels the bottom shared x-axis in seconds. |
| 58 | <code>    fig.tight_layout()</code> | Adjusts both subplot margins. |
| 59 | <code>    path = root / &quot;05_displacement.png&quot;</code> | Builds the dynamic-plot path. |
| 60 | <code>    fig.savefig(path, dpi=160)</code> | Saves the two-panel dynamic figure. |
| 61 | <code>    plt.close(fig)</code> | Closes the two-panel figure. |
| 62 | <code>    paths.append(str(path))</code> | Adds its path to the output list. |
| 63 | <code>    cal = run(configs[&quot;calibration&quot;])</code> | Runs the calibration scenario. |
| 64 | <code>    plt.figure(figsize=(7, 5))</code> | Creates the calibration figure. |
| 65 | <code>    plt.plot(cal.true_window_mean_mm, cal.fixed.displacement_mm, &quot;o&quot;, label=&quot;Fixed-point estimates&quot;)</code> | Plots measured fixed estimates against corresponding true window means as markers. |
| 66 | <code>    plt.plot([-5, 5], [-5, 5], &quot;--&quot;, label=&quot;Ideal&quot;)</code> | Overlays the ideal y=x line across +/-5 mm. |
| 67 | <code>    save(&quot;06_calibration&quot;, &quot;Signed displacement calibration&quot;, &quot;True displacement (mm)&quot;, &quot;Estimated displacement (mm)&quot;)</code> | Saves the calibration curve with both axes in mm. |
| 68 | <code>    plt.figure(figsize=(7, 5))</code> | Creates the Monte Carlo accuracy figure. |
| 69 | <code>    levels = [r[&quot;sigma_v&quot;] for r in report[&quot;noise&quot;]]</code> | Collects sigma values from the numerical report. |
| 70 | <code>    plt.plot(levels, [r[&quot;rmse_mm&quot;] for r in report[&quot;noise&quot;]], &quot;o-&quot;, label=&quot;Monte Carlo fixed-point RMSE&quot;)</code> | Plots measured fixed-path RMSE against sigma. |
| 71 | <code>    plt.plot(levels, [r[&quot;theoretical_std_mm&quot;] for r in report[&quot;noise&quot;]], &quot;--&quot;, label=&quot;Unclipped white-noise theory&quot;)</code> | Overlays ideal unclipped white-noise theory. |
| 72 | <code>    save(&quot;07_noise_error&quot;, f&quot;Noise robustness ({report[&#x27;trials_per_noise_level&#x27;]} trials per level)&quot;, &quot;Gaussian sigma (V)&quot;, &quot;Displacement error (mm)&quot;)</code> | Saves the noise study plot, including its actual trial count in the title. |
| 73 | <code>    plt.figure(figsize=(7, 5))</code> | Creates the phase-response figure. |
| 74 | <code>    phases = [r[&quot;phase_deg&quot;] for r in report[&quot;phase&quot;]]</code> | Collects tested phase angles. |
| 75 | <code>    plt.plot(phases, [r[&quot;fixed_mm&quot;] for r in report[&quot;phase&quot;]], &quot;o&quot;, label=&quot;Fixed-point estimate&quot;)</code> | Plots measured fixed-reference phase responses. |
| 76 | <code>    angle = np.linspace(0, 90, 200)</code> | Creates a smooth 0..90-degree axis for the theoretical curve. |
| 77 | <code>    plt.plot(angle, 2*np.cos(np.deg2rad(angle)), &quot;--&quot;, label=&quot;2 cos(phase)&quot;)</code> | Draws the expected 2*cos(phi) response for a +2 mm position. |
| 78 | <code>    save(&quot;08_phase_error&quot;, &quot;Uncompensated phase sensitivity at +2 mm&quot;, &quot;Sensor phase (degrees)&quot;, &quot;Estimated displacement (mm)&quot;)</code> | Saves the phase-response plot. |
| 79 | <code>    return paths</code> | Returns the complete list of eight saved image paths. |

