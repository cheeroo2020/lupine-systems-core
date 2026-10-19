/*
 * Lupine lab: reading and comparing measurements.
 * Used by website/lab/index.html and tested by tests/test_lab_core.mjs.
 *
 * Rules this file keeps:
 *  - A reading that did not arrive is null ("missing"), never 0. A real 0 stays 0.
 *  - Raw text is kept beside every derived number.
 *  - Two runs are compared only when the metric and unit match, and real data is
 *    never compared with synthetic data.
 *  - Temperatures are compared as differences in kelvin, never as percentages.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.LabCore = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const STAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/;
  const KEYLINE = /"(\w+)"\s=\s(.+?)\s*$/;
  const KEYS = ["Voltage", "Amperage", "Temperature", "ExternalConnected", "CurrentCapacity"];
  const round = (v, d) => (v === null ? null : Math.round(v * 10 ** d) / 10 ** d);

  // ioreg prints a negative current as an unsigned 64-bit number (2^64 - n).
  // Number() would lose the low digits, so the sign is fixed with BigInt first.
  function signed64(text) {
    if (!/^-?\d+$/.test(String(text))) return null;
    let v = BigInt(text);
    if (v >= 2n ** 63n) v -= 2n ** 64n;
    return Number(v);
  }

  // Output of the lab's baseline command: a UTC timestamp line, then key lines.
  function parseIoreg(text) {
    const samples = [], warnings = [];
    let cur = null;
    const start = t => { cur = { t, raw: {} }; samples.push(cur); };
    String(text || "").split(/\r?\n/).forEach((line, n) => {
      const s = line.trim();
      if (!s) return;
      if (STAMP.test(s)) return start(s);
      const m = s.match(KEYLINE);
      if (!m || !KEYS.includes(m[1])) return;
      if (!cur) { start(null); warnings.push("Readings before the first timestamp have no acquisition time, so their freshness can't be checked."); }
      if (m[1] in cur.raw) warnings.push(`Line ${n + 1}: ${m[1]} appears twice in one sample; the first value was kept.`);
      else cur.raw[m[1]] = m[2];
    });
    samples.forEach(derive);
    return { samples, warnings: warnings.concat(gapWarnings(samples)), raw: String(text || "") };
  }

  function derive(s) {
    const r = s.raw, num = (k, d) => (k in r && signed64(r[k]) !== null ? signed64(r[k]) / d : null);
    s.voltage_V = num("Voltage", 1000);            // millivolts
    s.current_A = num("Amperage", 1000);           // milliamps; negative = leaving the battery [ASSUMED]
    s.battery_C = num("Temperature", 100);         // hundredths of a degree [ASSUMED]
    s.capacity_raw = num("CurrentCapacity", 1);    // percent on some Macs, mAh on others: kept raw
    s.on_charger = r.ExternalConnected === "Yes" ? true : r.ExternalConnected === "No" ? false : null;
    s.power_W = null;
    if (s.voltage_V === null || s.current_A === null) s.note = "missing voltage or current";
    else if (s.on_charger === null) s.note = "power source unknown (no ExternalConnected line)";
    else if (s.on_charger) s.note = "on the charger: battery current is not the Mac's consumption";
    else if (s.current_A > 0) s.note = "positive current while unplugged: check the sign convention";
    else { s.power_W = round(s.voltage_V * Math.abs(s.current_A), 3); s.note = ""; }
    s.power_status = s.power_W === null ? "missing" : s.power_W === 0 ? "zero" : "ok";
  }

  function seconds(s) { return s.t ? Date.parse(s.t) / 1000 : null; }

  function gapWarnings(samples) {
    const t = samples.map(seconds), steps = [];
    for (let i = 1; i < t.length; i++) if (t[i] !== null && t[i - 1] !== null) steps.push(t[i] - t[i - 1]);
    if (!steps.length) return [];
    const typical = [...steps].sort((a, b) => a - b)[Math.floor((steps.length - 1) / 2)], out = [];   // lower median
    for (let i = 1; i < t.length; i++) {
      if (t[i] === null || t[i - 1] === null) continue;
      if (t[i] - t[i - 1] <= 0) out.push(`Samples ${i} and ${i + 1} are out of time order.`);
      else if (t[i] - t[i - 1] > 1.5 * typical)
        out.push(`Gap of ${t[i] - t[i - 1]} s before sample ${i + 1}: readings in it are missing, not zero.`);
    }
    return out;
  }

  // Averages leave missing values out; zeros stay in.
  function stats(values) {
    const valid = values.filter(v => v !== null && Number.isFinite(v)), n = valid.length;
    return {
      n_total: values.length, n_valid: n, n_missing: values.length - n, n_zero: valid.filter(v => v === 0).length,
      mean: n ? round(valid.reduce((a, b) => a + b, 0) / n, 3) : null,
      min: n ? Math.min(...valid) : null, max: n ? Math.max(...valid) : null,
    };
  }

  // Energy = area under the power curve (01-15), over intervals where both ends are usable.
  function energy(samples) {
    let wh = 0, covered = 0, span = 0;
    for (let i = 1; i < samples.length; i++) {
      const t0 = seconds(samples[i - 1]), t1 = seconds(samples[i]);
      if (t0 === null || t1 === null || t1 <= t0) continue;
      span += t1 - t0;
      const a = samples[i - 1].power_W, b = samples[i].power_W;
      if (a !== null && b !== null) { wh += ((a + b) / 2) * (t1 - t0) / 3600; covered += t1 - t0; }
    }
    return { energy_Wh: covered ? round(wh, 4) : null, covered_s: covered, span_s: span, coverage: span ? round(covered / span, 3) : null };
  }

  function makeRun(meta) {
    const parsed = parseIoreg(meta.text), s = parsed.samples;
    const temps = s.map(x => x.battery_C).filter(v => v !== null);
    const ambient = typeof meta.ambient_C === "number" && Number.isFinite(meta.ambient_C) ? meta.ambient_C : null;
    const start = temps.length ? temps[0] : null, end = temps.length ? temps[temps.length - 1] : null;
    const e = energy(s);
    return {
      id: meta.id, label: meta.label || "", synthetic: meta.synthetic === true,
      device: meta.device || "", method: meta.method || "", workload: meta.workload || "", ambient_C: ambient,
      metric: "battery discharge power", unit: "W",
      samples: s, warnings: parsed.warnings, raw: parsed.raw,
      duration_s: e.span_s || null, power: stats(s.map(x => x.power_W)), energy: e,
      battery: {
        start_C: start, end_C: end,
        rise_K: start !== null && end !== null ? round(end - start, 2) : null,
        above_ambient_K: end !== null && ambient !== null ? round(end - ambient, 2) : null,
      },
    };
  }

  function compareRuns(a, b) {
    const checks = [], warnings = [];
    const check = (name, va, vb, severity) =>
      checks.push({ name, a: va, b: vb, same: va === vb, severity: va === vb ? "ok" : severity });
    check("Metric", a.metric, b.metric, "block");
    check("Unit", a.unit, b.unit, "block");
    check("Data", a.synthetic ? "synthetic" : "real", b.synthetic ? "synthetic" : "real", "block");
    if (checks.some(c => c.severity === "block"))
      return { comparable: false, synthetic: a.synthetic || b.synthetic, checks,
               warnings: ["Different metric, unit, or real against synthetic data: no comparison made."] };

    const durationsClose = a.duration_s && b.duration_s &&
      Math.abs(a.duration_s - b.duration_s) / Math.max(a.duration_s, b.duration_s) <= 0.1;
    const ambientClose = a.ambient_C !== null && b.ambient_C !== null && Math.abs(a.ambient_C - b.ambient_C) < 1;
    check("Device", a.device, b.device, "warn");
    check("Method", a.method, b.method, "warn");
    check("Workload", a.workload, b.workload, "info");       // usually the thing being compared
    check("Duration (s)", a.duration_s, b.duration_s, durationsClose ? "ok" : "warn");
    check("Ambient (°C)", a.ambient_C, b.ambient_C, ambientClose ? "ok" : "warn");

    if (a.device !== b.device) warnings.push("Different devices: a difference may come from the hardware, not the workload.");
    if (a.method !== b.method) warnings.push("Different methods: a difference may come from how it was measured.");
    if (!a.duration_s || !b.duration_s) warnings.push("A run has no usable timestamps, so its duration is unknown.");
    else if (Math.abs(a.duration_s - b.duration_s) / Math.max(a.duration_s, b.duration_s) > 0.1)
      warnings.push("Durations differ by more than 10%: compare average power, not total energy.");
    for (const r of [a, b]) {
      if (r.ambient_C === null) warnings.push(`${r.label || r.id}: ambient not recorded, so a temperature rise can't be separated from a change in the room.`);
      if (r.power.n_missing) warnings.push(`${r.label || r.id}: ${r.power.n_missing} of ${r.power.n_total} samples have no usable power. They are left out of the average, not counted as zero.`);
      if (r.energy.coverage !== null && r.energy.coverage < 1) warnings.push(`${r.label || r.id}: energy covers only ${Math.round(r.energy.coverage * 100)}% of the run's time.`);
      r.warnings.forEach(w => warnings.push(`${r.label || r.id}: ${w}`));
    }
    if (a.ambient_C !== null && b.ambient_C !== null && Math.abs(a.ambient_C - b.ambient_C) >= 1)
      warnings.push(`Ambient differs by ${round(Math.abs(a.ambient_C - b.ambient_C), 1)} K: part of any temperature difference may be the room.`);

    const pa = a.power.mean, pb = b.power.mean;
    const both = (x, y) => x !== null && y !== null;
    return {
      comparable: true, synthetic: a.synthetic || b.synthetic, checks, warnings,
      power: {
        a: pa, b: pb, unit: "W",
        difference_W: both(pa, pb) ? round(pb - pa, 3) : null,
        ratio: both(pa, pb) && pa !== 0 ? round(pb / pa, 2) : null,   // power is a ratio-scale quantity
      },
      energy_Wh: { a: a.energy.energy_Wh, b: b.energy.energy_Wh },
      temperature: {            // differences in kelvin only: no percentages of Celsius values
        rise_K: { a: a.battery.rise_K, b: b.battery.rise_K },
        above_ambient_K: { a: a.battery.above_ambient_K, b: b.battery.above_ambient_K },
        end_difference_K: both(a.battery.end_C, b.battery.end_C) ? round(b.battery.end_C - a.battery.end_C, 2) : null,
      },
    };
  }

  // One row per sample; a missing value is an empty cell, never 0; raw text kept.
  function toCSV(run) {
    const head = ["data", "sample", "time_utc", "voltage_V", "current_A", "battery_temp_C", "on_charger", "capacity_raw",
                  "power_W", "power_status", "note", ...KEYS.map(k => "raw_" + k)];
    const cell = v => {
      if (v === null || v === undefined) return "";
      const s = String(v);
      return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
    };
    const rows = run.samples.map((s, i) => [run.synthetic ? "SYNTHETIC" : "real", i + 1, s.t, s.voltage_V, s.current_A, s.battery_C,
      s.on_charger, s.capacity_raw, s.power_W, s.power_status, s.note, ...KEYS.map(k => s.raw[k])].map(cell).join(","));
    return [head.join(","), ...rows].join("\n") + "\n";
  }

  return { signed64, parseIoreg, stats, energy, makeRun, compareRuns, toCSV };
});
