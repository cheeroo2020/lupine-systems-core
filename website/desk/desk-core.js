/*
 * Grid Desk: connection screening from published figures.
 * Used by website/desk/connections/ and tested by tests/test_desk_core.mjs.
 *
 * What it does: checks a proposed load against figures TasNetworks has published in its
 * Annual Planning Report 2026 (website/desk/data/apr-2026.json), and says which page each
 * result comes from.
 * What it does not do: any power system study (load flow, fault level, stability). It is a
 * learning screen, not an assessment by TasNetworks.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.DeskCore = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const round = (v, d = 1) => Math.round(v * 10 ** d) / 10 ** d;

  // Apparent power: MVA = MW / power factor (textbook 03-08, 03-09).
  function toMVA(mw, pf) { return mw / pf; }

  function validate(input) {
    const problems = [];
    if (!(Number.isFinite(input.mw) && input.mw > 0)) problems.push("Enter the load in MW, greater than zero.");
    if (!(Number.isFinite(input.pf) && input.pf >= 0.5 && input.pf <= 1)) problems.push("Power factor must be between 0.5 and 1.");
    if (!input.area) problems.push("Choose a planning area.");
    return problems;
  }

  function screen(input, data) {
    const problems = validate(input);
    if (problems.length) return { ok: false, problems };
    const rows = data.table_4_1.rows, rules = data.rules, mva = toMVA(input.mw, input.pf);
    const row = input.substation ? rows.find(r => r.name === input.substation && r.area === input.area) : null;
    const checks = [];
    const add = (id, title, status, detail, pages) => checks.push({ id, title, status, detail, pages });
    const maxRow = rows.reduce((a, b) => (b.firm_headroom_mva > a.firm_headroom_mva ? b : a));

    // 1. Spare capacity at a zone substation (distribution connection).
    if (input.substation && !row) {
      add("headroom", "Spare capacity at the substation", "study", `${input.substation} isn't in Table 4-1 for this planning area.`, [62, 63]);
    } else if (row) {
      const head = row.firm_headroom_mva, f = row.flags;
      const notes = [];
      if (f.includes("non_firm")) notes.push("its connection is non-firm, so supply may be interrupted after a single contingency");
      if (f.includes("subtransmission_constraint")) notes.push("its headroom is limited by a sub-transmission constraint");
      let status, detail;
      if (f.includes("unavailable_until_2028")) {
        status = "flag"; detail = `${row.name} shows ${head} MVA of firm headroom, but it is not available until 2028 because of an interim load connection.`;
      } else if (mva <= head) {
        status = notes.length ? "flag" : "ok";
        detail = `${round(mva)} MVA fits within ${row.name}'s published firm headroom of ${head} MVA.`;
      } else {
        status = "flag";
        detail = `${round(mva)} MVA exceeds ${row.name}'s published firm headroom of ${head} MVA. Options: network augmentation, a non-firm arrangement, or a connection at a higher voltage.`;
      }
      if (notes.length) detail += ` Note: ${notes.join("; ")}.`;
      add("headroom", "Spare capacity at the substation", status, detail, [row.page]);
    } else {
      add("headroom", "Spare capacity at the substation", "info",
          "No zone substation chosen: Table 4-1 covers distribution connections only, so a transmission connection needs its own study.", [62, 63]);
    }

    // 2. Is this a distribution-sized load at all?
    if (mva > maxRow.firm_headroom_mva) {
      add("size", "Distribution or transmission?", "study",
          `${round(mva)} MVA is more than any zone substation's published firm headroom (the largest is ${maxRow.firm_headroom_mva} MVA at ${maxRow.name}). Treat it as a transmission connection, which needs power system studies.`,
          [maxRow.page]);
    } else {
      add("size", "Distribution or transmission?", "ok",
          `${round(mva)} MVA is within the range of published zone-substation headroom (largest ${maxRow.firm_headroom_mva} MVA).`, [maxRow.page]);
    }

    // 3. Limits on how much load one failure may interrupt.
    const gt = rules.george_town_trigger, south = rules.southern_forecast;
    if (input.area === "Northern" && input.substation === "George Town") {
      if (input.mw >= gt.new_load_mw) {
        add("single_asset", "Single-failure limit", "flag",
            `${input.mw} MW is at or above the ${gt.new_load_mw} MW George Town trigger: new load at George Town of that size could at times be ${gt.share_of_state_load * 100}% or more of the State's load, so losing one transformer or the 220 kV bus there could black out the State. ${gt.response}`,
            gt.pages);
      } else {
        add("single_asset", "Single-failure limit", "study",
            `${input.mw} MW is below the ${gt.new_load_mw} MW George Town trigger on its own, but other new loads at George Town count towards it too.`, gt.pages);
      }
    } else if (input.area === "Southern") {
      const total = south.southern_max_demand_2034_mw + input.mw;
      add("single_asset", "Single-failure limit", input.mw > 850 - south.southern_max_demand_2034_mw ? "flag" : "study",
          `No more than 850 MW of load may be interrupted by a single asset failure. Southern maximum demand is forecast at ${south.southern_max_demand_2034_mw} MW by 2034 (${south.scenario}); adding ${input.mw} MW gives about ${total} MW. The report also says southern demand will exceed 850 MW in 2030 if the proposed ${south.boyer_boiler_mw} MW Boyer boiler proceeds.`,
          south.pages);
    } else {
      add("single_asset", "Single-failure limit", "info",
          "The planning rules allow no more than 850 MW of load to be interrupted by a single asset failure. The report publishes no area-specific trigger here; a planning study would check it.",
          rules.single_asset_850.pages);
    }

    // 4–5. Inverter-based loads: system strength and the new access standards.
    if (input.inverterBased) {
      const node = data.system_strength_nodes.area_to_node[input.area], o = data.system_strength_nodes.outlook[node];
      add("system_strength", `System strength near ${node}`, o.status === "ok" ? "info" : "study",
          `${o.text} (Matching this area to ${node} is a simplification.)`, o.pages);
      add("access_standards", "Access standards for large inverter-based loads", "info",
          "New access standards for large inverter-based loads, such as AI factories, were finalised in 2026 (Package 2). Check whether this load is large enough to be covered: the report doesn't give the threshold.",
          rules.access_standards_package_2.pages);
    }

    // 6. Responsive loads.
    add("responsive", "Can the load respond after a fault?", input.responsive ? "ok" : "info",
        input.responsive
          ? "The developer says the load can rapidly reduce its demand after a contingency. The report says this means less need for new transmission infrastructure."
          : "Ask the developer whether the load can rapidly reduce its demand after a contingency. The report says responsive loads need less new transmission infrastructure.",
        rules.responsive_load.pages);

    const count = s => checks.filter(c => c.status === s).length;
    return { ok: true, input: { ...input }, mva: round(mva), row: row || null, checks,
             summary: { flag: count("flag"), study: count("study"), ok: count("ok"), info: count("info") } };
  }

  // The memo Chris completes. Facts are filled in; the judgement sections are left for Chris.
  function memo(result, data, today) {
    const i = result.input, label = { ok: "No issue in published figures", flag: "Flag", study: "Needs a study", info: "Context" };
    const lines = [
      `# Connection enquiry: preliminary screening note`,
      ``,
      `*Practice note by Chris Gogoi, ${today}. A learning exercise using TasNetworks' published figures; not an assessment by TasNetworks.*`,
      ``,
      `## The enquiry`,
      `- Load: ${i.mw} MW at power factor ${i.pf} (about ${result.mva} MVA)`,
      `- Location: ${i.substation ? `${i.substation} zone substation, ` : ""}${i.area} planning area`,
      `- Inverter-based (e.g. an AI factory): ${i.inverterBased ? "yes" : "no"}; can reduce demand after a fault: ${i.responsive ? "yes" : "not stated"}`,
      ``,
      `## Screening against published figures`,
      ``,
      `| Check | Result | Why | Source |`,
      `|---|---|---|---|`,
      ...result.checks.map(c => `| ${c.title} | ${label[c.status]} | ${c.detail.replace(/\|/g, "/")} | APR 2026 p. ${c.pages.join(", ")} |`),
      ``,
      `## My summary for the connections lead`,
      `_In two or three sentences, in my own words: can this connect as asked, and what is the main issue?_`,
      ``,
      `## Main risks`,
      `_The two or three risks that matter most, and why._`,
      ``,
      `## Questions I'd ask the developer`,
      `_At least two._`,
      ``,
      `## What a proper assessment would add`,
      `_Which power system studies would be needed (for example load flow, fault level, stability), and why._`,
      ``,
      `---`,
      `Source: ${data.source.title}, ${data.source.publisher}. Page numbers are the report's printed pages. Figures are [ASSUMED]: as stated by TasNetworks, not checked by me against a second source.`,
    ];
    return lines.join("\n") + "\n";
  }

  return { toMVA, validate, screen, memo };
});
