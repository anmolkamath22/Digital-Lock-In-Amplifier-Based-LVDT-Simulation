const TRAJ = {
  static: ["value_mm|Position (mm)|-5|5|0.1|2"],
  step: ["before_mm|Before (mm)|-5|5|0.1|-3", "after_mm|After (mm)|-5|5|0.1|3", "step_s|Step time (s)|0|5|0.01|0.5"],
  sine: ["center_mm|Center (mm)|-2|2|0.1|0", "amplitude_mm|Amplitude (mm)|0|3|0.1|3", "frequency_hz|Frequency (Hz)|0|20|0.1|2", "phase_deg|Phase (°)|0|360|1|0"],
  ramp: ["start_mm|Start (mm)|-5|5|0.1|-5", "end_mm|End (mm)|-5|5|0.1|5"],
  calibration: ["hold_windows|Windows per level|1|20|1|5"],
};
const PRESETS = {
  "Clean +2 mm": { mode: "static", value_mm: 2 },
  "Noisy": { mode: "static", value_mm: 2, noise_std_v: 0.2, hum_peak_v: 0.1, dc_offset_v: 0.15, interference_peak_v: 0.1, interference_hz: 950 },
  "Heavy noise": { mode: "static", value_mm: 2, noise_std_v: 0.4, hum_peak_v: 0.1 },
  "Step −3→+3": { mode: "step" },
  "Sine 2 Hz": { mode: "sine" },
  "Calibration": { mode: "calibration" },
  "Phase 45°": { mode: "static", value_mm: 2, phase_deg: 45 },
  "Coherent 1 kHz": { mode: "static", value_mm: 2, interference_peak_v: 0.24, interference_hz: 1000 },
  "ADC overrange": { mode: "static", value_mm: 2, interference_peak_v: 3, interference_hz: 1000 },
};
const $ = (s) => document.querySelector(s);
const form = $("#form");
let run = null, gen = null;
const charts = {};

function slider(spec, prefix = "") {
  const [k, lab, min, max, step, def] = spec.split("|");
  const id = prefix + k;
  return `<label>${lab}<input type="number" name="${id}" id="n_${id}" value="${def}" step="${step}">
    <input type="range" id="r_${id}" min="${min}" max="${max}" step="${step}" value="${def}"></label>`;
}
function wire(root) {
  root.querySelectorAll("input[type=range]").forEach((r) => {
    const n = $("#n_" + r.id.slice(2));
    r.oninput = () => (n.value = r.value);
    n.oninput = () => (r.value = n.value);
  });
}
document.querySelectorAll("[data-p]").forEach((d) => (d.outerHTML = slider(d.dataset.p)));
function renderTraj() {
  $("#traj").innerHTML = TRAJ[$("#mode").value].map((s) => slider(s, "t_")).join("");
  wire($("#traj"));
}
$("#mode").onchange = renderTraj;
renderTraj(); wire(form);

function setVal(k, v) {
  for (const id of [k, "t_" + k]) {
    const n = $("#n_" + id), r = $("#r_" + id);
    if (n) { n.value = v; if (r) r.value = v; }
  }
}
function defaults() {
  form.querySelectorAll("[id^=r_]").forEach((r) => { setVal(r.id.slice(2), r.defaultValue); });
}
Object.entries(PRESETS).forEach(([name, p]) => {
  const b = document.createElement("button");
  b.textContent = name; b.type = "button";
  b.onclick = () => {
    defaults(); $("#mode").value = p.mode; renderTraj();
    Object.entries(p).forEach(([k, v]) => k !== "mode" && setVal(k, v));
    form.requestSubmit();
  };
  $("#presets").appendChild(b);
});

function params() {
  const p = { mode: $("#mode").value };
  new FormData(form).forEach((v, k) => { if (k !== "mode") p[k.replace(/^t_/, "")] = Number(v); });
  // the sensor's phase_deg must not be overwritten by the sine trajectory's phase_deg
  if (p.mode === "sine") p.phase_deg = Number($("#n_phase_deg").value);
  const traj = {}; TRAJ[p.mode].forEach((s) => { const k = s.split("|")[0]; traj[k] = Number($("#n_t_" + k).value); });
  return { ...p, ...traj, phase_deg: Number($("#n_phase_deg").value), traj };
}

Chart.defaults.color = "#8b98a5"; Chart.defaults.borderColor = "#26303b"; Chart.defaults.font.size = 11;
function chart(id, datasets, opts = {}) {
  charts[id]?.destroy();
  charts[id] = new Chart($("#" + id), {
    type: "line", data: { datasets },
    options: { animation: false, maintainAspectRatio: false, parsing: false, normalized: true,
      elements: { point: { radius: 0 }, line: { borderWidth: 1.4 } },
      interaction: { mode: "nearest", intersect: false },
      scales: { x: { type: "linear", title: { display: !!opts.x, text: opts.x } }, y: { title: { display: !!opts.y, text: opts.y } } },
      plugins: { legend: { labels: { boxWidth: 10 } } }, ...opts.extra },
  });
}
const xy = (xs, ys) => xs.map((x, i) => ({ x, y: ys[i] }));
const C = { a: "#4cc2ff", b: "#f0883e", c: "#a371f7", d: "#3fb950", e: "#e6edf3" };

function stats(items) {
  $("#stats").innerHTML = items.map(([k, v]) => `<div class="stat"><small>${k}</small><b>${v}</b></div>`).join("");
}
function step(n) { for (let i = 1; i <= 4; i++) $("#f" + i).classList.toggle("on", i <= n); }

form.onsubmit = async (e) => {
  e.preventDefault(); $("#err").textContent = ""; $("#genBtn").disabled = true; step(1);
  const p = params();
  const tr = p.traj; delete p.traj;
  // trajectory phase_deg uses its own key on the server
  const body = { ...p, ...tr };
  if (p.mode === "sine") { body.phase_deg = p.phase_deg; body.traj_phase = tr.phase_deg; }
  try {
    const r = await fetch("/api/generate", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
    const d = await r.json(); if (!r.ok) throw new Error(d.error);
    gen = d; run = d.run; step(2);
    $("#simBtn").disabled = false; $("#dlBtn").disabled = false;
    const z = d.zoom, tms = z.t.map((t) => t * 1000);
    chart("cWave", [
      { label: "Secondary 1", data: xy(tms, z.s1), borderColor: C.a },
      { label: "Secondary 2", data: xy(tms, z.s2), borderColor: C.b },
      { label: "Differential (clean)", data: xy(tms, z.diff), borderColor: C.d },
      { label: "Measured (+noise)", data: xy(tms, z.measured), borderColor: C.e, borderWidth: 0.8 },
    ], { x: "time (ms)", y: "V" });
    chart("cAdc", [{ label: "ADC code", data: xy(tms, z.adc), borderColor: C.c, stepped: true },
      { label: "+2047", data: [{ x: 0, y: 2047 }, { x: tms.at(-1), y: 2047 }], borderColor: "#f85149", borderDash: [4, 4] },
      { label: "−2048", data: [{ x: 0, y: -2048 }, { x: tms.at(-1), y: -2048 }], borderColor: "#f85149", borderDash: [4, 4] }],
      { x: "time (ms)", y: "code" });
    chart("cFft", [{ label: "|FFT| (dB, Hann)", data: xy(d.spectrum.f, d.spectrum.db), borderColor: C.a, borderWidth: 1 }],
      { x: "frequency (Hz)", y: "dB", extra: { scales: { x: { type: "linear", max: 3000, title: { display: true, text: "frequency (Hz)" } }, y: { min: -120 } } } });
    drawDisp(); $("#tbody").innerHTML = ""; $("#results").className = "muted"; $("#results").textContent = "Signal ready. Press ② Run Verilog lock-in."; $("#log").textContent = "Vectors ready. Press ② to run the Verilog lock-in.";
    const ex = d.expected, err = ex.x_fixed.map((x, i) => Math.abs(x - ex.truth[i]));
    stats([["Samples", d.samples.toLocaleString()], ["Windows", d.windows], ["ADC clipped", `${d.clipped} (${d.clipped_percent.toFixed(2)}%)`],
      ["Python time", d.python_ms + " ms"], ["Mean |error|", (err.reduce((a, b) => a + b, 0) / err.length).toFixed(4) + " mm"],
      ["Verilog", "not run"]]);
  } catch (ex) { $("#err").textContent = ex.message; }
  $("#genBtn").disabled = false;
};

function drawDisp(rtl) {
  const ex = gen.expected, t = ex.center_t.map((v) => v * 1000);
  const ds = [
    { label: "True displacement", data: xy(gen.traj.t.map((v) => v * 1000), gen.traj.x), borderColor: C.d },
    { label: "Python float lock-in", data: xy(t, ex.x_float), borderColor: C.b, pointRadius: 0, borderDash: [3, 3] },
    { label: "Python fixed (expected)", data: xy(t, ex.x_fixed), borderColor: C.a, pointRadius: 2, showLine: false },
  ];
  if (rtl) ds.push({ label: "Verilog output", data: xy(t, rtl.rtl_mm), borderColor: C.c, backgroundColor: C.c, pointRadius: 3, pointStyle: "crossRot", showLine: false });
  chart("cDisp", ds, { x: "time (ms)", y: "mm" });
  if (rtl) chart("cErr", [{ label: "error (mm)", data: xy(t, rtl.rtl_mm.map((x, i) => x - ex.truth[i])), borderColor: C.c, stepped: true }], { x: "window center (ms)", y: "mm" });
}

$("#simBtn").onclick = async () => {
  $("#simBtn").disabled = true; $("#err").textContent = ""; $("#log").textContent = "Simulating…";
  try {
    const r = await fetch("/api/simulate/" + run, { method: "POST" });
    const d = await r.json(); if (!r.ok) throw new Error(d.error);
    step(4); drawDisp(d);
    $("#engineBadge").textContent = d.engine === "python-model" ? "engine: Python RTL model (no simulator found)" : "engine: " + d.engine;
    $("#log").textContent = d.log;
    const ex = gen.expected;
    const n = d.rtl_acc.length;
    $("#tbody").innerHTML = ex.acc.map((a, i) => {
      const okI = d.rtl_acc[i] === a, okQ = d.rtl_q_acc[i] === d.expected_q[i];
      const tick = (ok) => `<td style="color:${ok ? "var(--ok)" : "var(--bad)"}">${ok ? "✓" : "✗"}</td>`;
      return `<tr><td>${i}</td><td>${(ex.center_t[i] * 1000).toFixed(2)}</td><td>${d.rtl_acc[i] ?? "–"}</td><td>${d.rtl_q_acc[i] ?? "–"}</td>
        <td>${d.mag_v[i].toFixed(5)}</td><td>${d.mag_mm[i].toFixed(4)}</td><td>${d.phase_deg[i].toFixed(2)}</td><td>${d.rtl_mm[i].toFixed(4)}</td>${tick(okI)}${tick(okQ)}</tr>`;
    }).join("");
    const mean = (a) => a.reduce((s, v) => s + v, 0) / a.length;
    const sd = (a) => { const m = mean(a); return Math.sqrt(mean(a.map((v) => (v - m) ** 2))); };
    // circular mean for phase
    const ph = d.phase_deg.map((p) => (p * Math.PI) / 180);
    const phMean = (Math.atan2(mean(ph.map(Math.sin)), mean(ph.map(Math.cos))) * 180) / Math.PI;
    const last = n - 1;
    const card = (k, v, sub, cls = "") => `<div class="stat ${cls}"><small>${k}</small><b>${v}</b><small>${sub}</small></div>`;
    $("#results").className = "";
    $("#results").innerHTML = `<div class="big">
      ${card("Magnitude (mean)", mean(d.mag_v).toFixed(4) + " V", `σ ${sd(d.mag_v).toFixed(4)} V · latest ${d.mag_v[last].toFixed(4)} V`)}
      ${card("Displacement magnitude", mean(d.mag_mm).toFixed(3) + " mm", `|V| / K, K = ${d.K} V/mm · latest ${d.mag_mm[last].toFixed(3)} mm`)}
      ${card("Phase angle (mean)", phMean.toFixed(2) + "°", `σ ${sd(d.phase_deg).toFixed(2)}° · latest ${d.phase_deg[last].toFixed(2)}°`, "ph")}
      ${card("Signed displacement (I/K)", mean(d.rtl_mm).toFixed(3) + " mm", `latest ${d.rtl_mm[last].toFixed(3)} mm · ${n} windows`)}
      ${card("In-phase I (mean)", mean(d.i_v).toFixed(4) + " V", "Verilog, sine LUT")}
      ${card("Quadrature Q (mean)", mean(d.q_v).toFixed(4) + " V", "Verilog, cosine LUT")}
      ${card("Verilog vs Python", `<span class="badge ${d.passed && d.passed_q ? "pass" : "fail"}">${d.passed && d.passed_q ? "BIT-EXACT" : "MISMATCH"}</span>`,
        `I ${d.rtl_count - d.mismatches}/${d.expected_count} · Q ${d.expected_q.length - d.mismatches_q}/${d.expected_q.length}`)}
    </div>`;
    const t = ex.center_t.map((v) => v * 1000);
    chart("cMag", [{ label: "|V| (V)", data: xy(t, d.mag_v), borderColor: C.a, stepped: true },
      { label: "|x| (mm)", data: xy(t, d.mag_mm), borderColor: C.d, stepped: true, yAxisID: "y2" }],
      { x: "window center (ms)", y: "V", extra: { scales: { x: { type: "linear", title: { display: true, text: "window center (ms)" } },
        y: { title: { display: true, text: "V" } }, y2: { position: "right", grid: { drawOnChartArea: false }, title: { display: true, text: "mm" } } } } });
    chart("cPhase", [{ label: "phase φ (°)", data: xy(t, d.phase_deg), borderColor: "#a371f7", stepped: true }],
      { x: "window center (ms)", y: "degrees", extra: { scales: { x: { type: "linear", title: { display: true, text: "window center (ms)" } }, y: { min: -180, max: 180, ticks: { stepSize: 45 }, title: { display: true, text: "degrees" } } } } });
    const errs = d.rtl_mm.map((x, i) => x - ex.truth[i]);
    const rmse = Math.sqrt(errs.reduce((a, b) => a + b * b, 0) / errs.length);
    const items = [...$("#stats").children].slice(0, 5).map((s) => [s.querySelector("small").textContent, s.querySelector("b").textContent]);
    items.push(["Verilog", `<span class="badge ${d.passed && d.passed_q ? "pass" : "fail"}">${d.passed && d.passed_q ? "PASS" : "FAIL"}</span>`],
      ["RMSE vs truth", rmse.toFixed(4) + " mm"], ["HDL time (I+Q)", d.hdl_ms + " ms"]);
    stats(items);
  } catch (ex) { $("#err").textContent = "Simulation failed"; $("#log").textContent = ex.message; }
  $("#simBtn").disabled = false;
};
$("#dlBtn").onclick = () => run && (location.href = "/api/download/" + run);

fetch("/api/info").then((r) => r.json()).then((d) => ($("#engineBadge").textContent = "engine: " + (d.engine === "python-model" ? "Python RTL model (no simulator found)" : d.engine)));
form.requestSubmit();
