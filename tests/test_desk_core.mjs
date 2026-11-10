// Tests for website/desk/desk-core.js. Run: node --test tests/test_desk_core.mjs
import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";

const require = createRequire(import.meta.url);
const Desk = require("../website/desk/desk-core.js");
const data = JSON.parse(readFileSync(new URL("../website/desk/data/apr-2026.json", import.meta.url)));
const base = { mw: 10, pf: 0.95, area: "Southern", substation: "Kingston (33 kV)", inverterBased: false, responsive: false };
const check = (r, id) => r.checks.find(c => c.id === id);

test("apparent power is MW divided by power factor", () => {
  assert.equal(Desk.toMVA(95, 0.95), 100);
});

test("bad input is refused, not guessed", () => {
  assert.equal(Desk.screen({ ...base, mw: 0 }, data).ok, false);
  assert.equal(Desk.screen({ ...base, pf: 1.2 }, data).ok, false);
  assert.equal(Desk.screen({ ...base, area: "" }, data).ok, false);
});

test("a small load within published firm headroom passes the headroom check", () => {
  const r = Desk.screen(base, data);             // 10.5 MVA at Kingston 33 kV (47 MVA headroom)
  assert.equal(check(r, "headroom").status, "ok");
  assert.deepEqual(check(r, "headroom").pages, [63]);
  assert.equal(check(r, "size").status, "ok");
});

test("a load above the substation's headroom is flagged, with options", () => {
  const r = Desk.screen({ ...base, mw: 60 }, data);
  assert.equal(check(r, "headroom").status, "flag");
  assert.match(check(r, "headroom").detail, /exceeds/);
});

test("a 100 MW AI factory is a transmission question: larger than any zone substation's headroom", () => {
  const r = Desk.screen({ ...base, mw: 100, area: "Northern", substation: null, inverterBased: true }, data);
  assert.equal(check(r, "size").status, "study");
  assert.match(check(r, "size").detail, /47 MVA at Kingston \(33 kV\)/);
  assert.equal(check(r, "headroom").status, "info");
});

test("headroom held for an interim load connection is flagged until 2028", () => {
  const r = Desk.screen({ ...base, mw: 5, area: "Northern", substation: "St Leonards" }, data);
  assert.equal(check(r, "headroom").status, "flag");
  assert.match(check(r, "headroom").detail, /not available until 2028/);
});

test("a non-firm connection is flagged even when the load fits", () => {
  const r = Desk.screen({ ...base, mw: 5, area: "North West and West Coast", substation: "Queenstown (22 kV)" }, data);
  assert.equal(check(r, "headroom").status, "flag");
  assert.match(check(r, "headroom").detail, /non-firm/);
});

test("300 MW or more at George Town hits the system-black trigger", () => {
  const big = Desk.screen({ ...base, mw: 300, area: "Northern", substation: "George Town" }, data);
  assert.equal(check(big, "single_asset").status, "flag");
  assert.deepEqual(check(big, "single_asset").pages, [52]);
  const small = Desk.screen({ ...base, mw: 50, area: "Northern", substation: "George Town" }, data);
  assert.equal(check(small, "single_asset").status, "study");
});

test("southern loads are checked against the 850 MW limit and the 830 MW forecast", () => {
  const r = Desk.screen({ ...base, mw: 40 }, data);
  assert.equal(check(r, "single_asset").status, "flag");       // 830 + 40 > 850
  assert.match(check(r, "single_asset").detail, /about 870 MW/);
  const tiny = Desk.screen({ ...base, mw: 5 }, data);
  assert.equal(check(tiny, "single_asset").status, "study");    // within margin, but Boyer would breach in 2030
});

test("inverter-based loads get the system strength outlook for their area, labelled as a simplification", () => {
  const r = Desk.screen({ ...base, mw: 20, area: "Northern", substation: "George Town", inverterBased: true }, data);
  const ss = check(r, "system_strength");
  assert.equal(ss.status, "study");
  assert.match(ss.detail, /vulnerable/);
  assert.match(ss.detail, /simplification/);
  assert.ok(check(r, "access_standards"));
  const plain = Desk.screen(base, data);
  assert.equal(check(plain, "system_strength"), undefined);
});

test("every check cites a page, and the memo leaves the judgement to Chris", () => {
  const r = Desk.screen({ ...base, mw: 100, area: "Northern", substation: "George Town", inverterBased: true }, data);
  assert.ok(r.checks.every(c => c.pages.length && c.pages.every(Number.isInteger)));
  const m = Desk.memo(r, data, "13 November 2026");
  assert.match(m, /not an assessment by TasNetworks/);
  assert.match(m, /## My summary for the connections lead\n_In two or three sentences/);
  assert.match(m, /\[ASSUMED\]/);
  assert.equal((m.match(/^\| /gm) || []).length, r.checks.length + 1);   // header row + one per check
});
