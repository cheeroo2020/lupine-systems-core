// Tests for website/lab/lab-core.js. Run: node --test tests/test_lab_core.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";

const require = createRequire(import.meta.url);
const Lab = require("../website/lab/lab-core.js");
const demo = JSON.parse(readFileSync(new URL("../website/lab/demo-data.json", import.meta.url)));

const sample = (t, lines) => [t, ...lines.map(l => `      ${l}`)].join("\n");
const unplugged = (t, mV, mA, extra = []) =>
  sample(t, [`"Voltage" = ${mV}`, `"Amperage" = ${mA}`, `"ExternalConnected" = No`, ...extra]);

test("a negative current printed as an unsigned 64-bit number keeps its exact value", () => {
  assert.equal(Lab.signed64("18446744073709551136"), -480);   // 2^64 - 480
  assert.equal(Lab.signed64("480"), 480);
  assert.equal(Lab.signed64("-480"), -480);
  assert.equal(Lab.signed64("No"), null);
});

test("power is V x I from the battery's own readings, unplugged", () => {
  const [s] = Lab.parseIoreg(unplugged("2026-10-21T00:00:00Z", 12600, "18446744073709551136")).samples;
  assert.equal(s.voltage_V, 12.6);
  assert.equal(s.current_A, -0.48);
  assert.equal(s.power_W, 6.048);
  assert.equal(s.power_status, "ok");
});

test("a missing current is missing, never zero", () => {
  const [s] = Lab.parseIoreg(sample("2026-10-21T00:00:00Z", [`"Voltage" = 12600`, `"ExternalConnected" = No`])).samples;
  assert.equal(s.current_A, null);
  assert.equal(s.power_W, null);
  assert.equal(s.power_status, "missing");
});

test("a real zero stays zero and is counted in the average", () => {
  const run = Lab.makeRun({ text: [unplugged("2026-10-21T00:00:00Z", 12000, 0), unplugged("2026-10-21T00:01:00Z", 12000, -1000)].join("\n") });
  assert.equal(run.samples[0].power_W, 0);
  assert.equal(run.samples[0].power_status, "zero");
  assert.equal(run.power.n_zero, 1);
  assert.equal(run.power.mean, 6);   // (0 + 12) / 2: the zero is included
});

test("missing values are left out of averages, not averaged in as zero", () => {
  const run = Lab.makeRun({ text: [unplugged("2026-10-21T00:00:00Z", 12000, -1000),
    sample("2026-10-21T00:01:00Z", [`"Voltage" = 12000`, `"ExternalConnected" = No`]),
    unplugged("2026-10-21T00:02:00Z", 12000, -1000)].join("\n") });
  assert.equal(run.power.n_missing, 1);
  assert.equal(run.power.mean, 12);
  assert.equal(run.energy.coverage, 0);   // no interval has both ends usable
});

test("on the charger, battery current is not taken as the Mac's power", () => {
  const [s] = Lab.parseIoreg(sample("2026-10-21T00:00:00Z", [`"Voltage" = 12600`, `"Amperage" = 900`, `"ExternalConnected" = Yes`])).samples;
  assert.equal(s.current_A, 0.9);
  assert.equal(s.power_W, null);
  assert.match(s.note, /charger/);
});

test("a missing minute is reported as a gap", () => {
  const p = Lab.parseIoreg([unplugged("2026-10-21T00:00:00Z", 12000, -500), unplugged("2026-10-21T00:01:00Z", 12000, -500),
    unplugged("2026-10-21T00:03:00Z", 12000, -500)].join("\n"));
  assert.ok(p.warnings.some(w => /Gap of 120 s/.test(w)));
});

test("energy is the area under the power curve, in watt-hours", () => {
  const run = Lab.makeRun({ text: [unplugged("2026-10-21T00:00:00Z", 10000, -1000), unplugged("2026-10-21T01:00:00Z", 10000, -1000)].join("\n") });
  assert.equal(run.energy.energy_Wh, 10);   // 10 W for one hour
  assert.equal(run.energy.coverage, 1);
});

test("a gap is not covered time: energy across it is a separate, labelled estimate", () => {
  // Regression: samples at minutes 0, 1 and 3 used to report 100% coverage.
  const run = Lab.makeRun({ text: [unplugged("2026-10-21T00:00:00Z", 12000, -1000), unplugged("2026-10-21T00:01:00Z", 12000, -1000),
    unplugged("2026-10-21T00:03:00Z", 12000, -1000)].join("\n") });
  assert.equal(run.energy.span_s, 180);
  assert.equal(run.energy.covered_s, 60);
  assert.equal(run.energy.gap_s, 120);
  assert.equal(run.energy.coverage, 0.333);
  assert.equal(run.energy.energy_Wh, 0.2);              // 12 W for the one covered minute
  assert.equal(run.energy.interpolated_Wh, 0.4);        // 12 W across the 2-minute gap, an estimate
  const other = Lab.makeRun({ text: [unplugged("2026-10-21T00:00:00Z", 12000, -1000), unplugged("2026-10-21T00:01:00Z", 12000, -1000)].join("\n") });
  assert.ok(Lab.compareRuns(run, other).warnings.some(w => /interpolated/.test(w)));
});

test("the raw text is kept, and CSV leaves missing cells empty", () => {
  const text = [unplugged("2026-10-21T00:00:00Z", 12000, -1000), sample("2026-10-21T00:01:00Z", [`"Voltage" = 12000`, `"ExternalConnected" = No`])].join("\n");
  const run = Lab.makeRun({ text });
  assert.equal(run.raw, text);
  const rows = Lab.toCSV(run).trim().split("\n");
  assert.equal(rows.length, 3);
  const cols = rows[0].split(","), second = rows[2].split(",");
  assert.equal(second[cols.indexOf("current_A")], "");
  assert.equal(second[cols.indexOf("power_W")], "");
  assert.equal(second[cols.indexOf("data")], "real");
});

test("real readings are never compared with synthetic ones", () => {
  const real = Lab.makeRun({ text: unplugged("2026-10-21T00:00:00Z", 12000, -1000) });
  const fake = Lab.makeRun({ text: unplugged("2026-10-21T00:00:00Z", 12000, -1000), synthetic: true });
  const c = Lab.compareRuns(real, fake);
  assert.equal(c.comparable, false);
  assert.equal(c.power, undefined);
});

test("a metric or unit mismatch blocks the comparison", () => {
  const a = Lab.makeRun({ text: unplugged("2026-10-21T00:00:00Z", 12000, -1000) });
  const b = { ...a, unit: "mW" };
  assert.equal(Lab.compareRuns(a, b).comparable, false);
});

test("the demo comparison warns about ambient, gaps and missing samples, and uses no Celsius percentages", () => {
  const [A, B] = demo.runs.map(Lab.makeRun);
  assert.ok(A.synthetic && B.synthetic);
  const c = Lab.compareRuns(A, B);
  assert.equal(c.comparable, true);
  assert.equal(c.synthetic, true);
  assert.ok(c.warnings.some(w => /Ambient differs by 1.5 K/.test(w)));
  assert.ok(c.warnings.some(w => /Gap of 120 s/.test(w)));
  assert.ok(c.warnings.some(w => /not counted as zero/.test(w)));
  assert.ok(c.power.b > c.power.a);
  assert.equal(c.temperature.end_difference_K, round2(B.battery.end_C - A.battery.end_C));
  assert.ok(!/percent|%/.test(JSON.stringify(c.temperature)));
  assert.equal(B.samples.at(-1).current_A, 0);          // a valid zero current, on the charger
  assert.equal(B.samples.at(-1).power_W, null);         // but no power can be derived from it
});

test("ambient differences under 1 K don't raise a warning", () => {
  const t = unplugged("2026-10-21T00:00:00Z", 12000, -1000) + "\n" + unplugged("2026-10-21T00:01:00Z", 12000, -1000);
  const a = Lab.makeRun({ text: t, ambient_C: 19.0 }), b = Lab.makeRun({ text: t, ambient_C: 19.4 });
  const c = Lab.compareRuns(a, b);
  assert.ok(!c.warnings.some(w => /Ambient/.test(w)));
  assert.equal(c.checks.find(x => x.name === "Ambient (°C)").severity, "ok");
});

function round2(v) { return Math.round(v * 100) / 100; }
