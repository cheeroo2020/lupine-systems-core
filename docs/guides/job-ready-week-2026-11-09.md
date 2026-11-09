# Job-ready week: 9 to 16 November 2026

**Aim:** by Monday 16 November, be ready to apply for an office-based technical role at a network business
(asset management, connections or planning), with:
- AEMO's NEM Foundations course finished;
- TasNetworks' Annual Planning Report 2026 read;
- two one-pagers in your own words;
- a CV;
- answers you can give aloud;
- a live portfolio.

**How to use this guide:** open only today's section. Each weekday has three parts:
- **Read:** the course modules and report pages for the day.
- **Understand:** five ideas, explained more fully than the sources do.
- **Check:** three questions. Answer them in your notebook and send them to Claude. The answers aren't here on purpose.

**References:**
- "NEM p." is a page of your copy of AEMO's course.
- "APR p." is the report's printed page number (the PDF page is 2 higher).
- Figures are **[ASSUMED]**: as stated by AEMO or TasNetworks, not checked by us.
- Fuller notes: `research/2026-11-09-R-aemo-nem-foundations.md` and `research/2026-11-09-R-tasnetworks-apr-2026.md`.

**If a day is too much,** do the course modules only. Friday and Saturday's one-pagers matter most.

---

## Monday 9: what the NEM is, and who does what

**Read (about 2 hours):**
- NEM course modules 1, 2 and 3 (NEM pp. 1–96).
- The planning report's executive summary (APR pp. 2–8).

**Understand:**
1. **One machine and one market.** The NEM is a single connected power system, about 5,000 km long, reaching
   Hobart (NEM p. 4). Generators sell into a pool, because electricity can't be stored in the system and you
   can't trace which generator your power came from (NEM p. 26).
2. **The path of electricity.** The generator's voltage is stepped up for transmission (up to 500 kV),
   stepped down at substations, then carried by the distribution network to customers at about 230 V
   (NEM pp. 11–13). Tasmania's backbone is 220 kV, with 110 kV around it (APR p. 35).
3. **Five bodies, five jobs** (NEM p. 46):
   - the **AEMC** makes the rules;
   - the **AER** regulates and enforces, including how much network businesses may earn;
   - **AEMO** runs the system and the market;
   - the ECMC sets policy;
   - the EAP advises.
4. **Why networks are regulated.** A second set of poles and wires down every street makes no sense, so a
   network is a natural monopoly. Instead of competition, the AER caps its revenue, usually every five years
   (NEM p. 86). Network businesses can't own generation or sell energy ("ring-fencing", NEM p. 79).
   TasNetworks is Tasmania's transmission *and* distribution business (NEM p. 84).
5. **What's new in Tasmania** (APR pp. 2–4):
   - Basslink became a regulated transmission service on 1 July 2026 (NEM p. 84; APR p. 18).
   - Firmus's AI factories have contracted 104 MW at St Leonards, 288 MW at Bell Bay and 52 MW at Wesley Vale (APR p. 4).
   - The Tasmanian Renewable Energy Target adds 3,000 MW of new renewable capacity (APR p. 2).

**Notebook:** three lines per module, in your own words.

**Check (send to Claude):**
1. In two sentences: what does the AER do that AEMO doesn't?
2. Why is TasNetworks regulated, rather than competing in a market?
3. The course says network losses are about 10% of electricity transported (NEM p. 88). TasNetworks reports
   losses of about 3.1% of the State's energy (APR p. 29). Read both sentences carefully. Why might the two numbers differ?

---

## Tuesday 10: keeping the system balanced

**Read (about 2 hours):**
- NEM course modules 4, 5 and 6 (NEM pp. 97–167).
- Report chapter 2, the Tasmanian power system (APR pp. 25–40).

**Understand:**
1. **Balance every second.** Supply must equal demand every second (NEM p. 100). Frequency is the signal:
   if demand exceeds supply, frequency falls (NEM p. 104). The normal band is 49.85–50.15 Hz (NEM p. 114).
   Textbook 03-19 explains why.
2. **Security is not reliability.**
   - *Security* means staying within safe limits if one element, such as a line or a generator, is suddenly
     lost. That loss is a "credible contingency" (NEM pp. 91, 102).
   - *Reliability* means there's enough supply to meet demand (NEM p. 103).
   - Network planners design for "N-1": the system must survive losing any one element.
3. **Dispatch every five minutes.** AEMO stacks generators' offers from cheapest up and runs the cheapest set
   that meets demand within the network's limits (NEM pp. 129–130). Prices run between −$1,000 and $20,300 per
   MWh in 2025–26 (NEM p. 132). When an interconnector is full, the regions' prices split (NEM p. 137).
4. **Frequency control (FCAS).** These services, bought by AEMO, push frequency back towards 50 Hz. They act at
   four speeds, from 1 second to 5 minutes (NEM pp. 156–157). When a region is cut off ("islanded"), its
   frequency control has to come from inside it (NEM p. 159). For Tasmania, that happens whenever Basslink trips.
5. **Tasmania's system** (APR ch. 2):
   - Hydro provides 2,125 MW of capacity and 62.9% of energy; wind 568 MW and 18.2% (APR p. 29).
   - In 2025, demand ran from 728 to 1,645 MW, peaking in winter (APR p. 26).
   - Four major industrial sites dominate (APR p. 7).
   - Demand fell after the Liberty Bell Bay smelter closed (APR p. 26), and energy use was down 5% in 2025 (APR p. 30).

**Notebook:** three lines per module, plus one line on Tasmania's generation mix.

**Check (send to Claude):**
1. A large generator suddenly trips. What happens to frequency in the first second, and what stops it falling further?
2. Why does Tasmania need some of its frequency control to come from inside Tasmania?
3. Tasmania's demand peaks in winter (APR p. 26). Suggest one reason, and one consequence for network planning.

---

## Wednesday 11: planning the network

**Read (about 2 hours):**
- NEM course modules 7 and 10 (NEM pp. 168–202 and 271–298).
- Report chapters 3 and 4, projects and constraints (APR pp. 41–76).

**Understand:**
1. **Metering is the NEM's cash register** (NEM p. 170). Every connection point has a 10-character identifier,
   the NMI, issued by the network business (NEM p. 175). The lab's rule that "a missing reading is not zero"
   is the same discipline metering data needs.
2. **The planning documents** (NEM pp. 274–277):
   - AEMO's Integrated System Plan: 20 years ahead, every two years.
   - Its Electricity Statement of Opportunities: 10 years.
   - TasNetworks' Annual Planning Report: its own 10-year look ahead, every year.
3. **The regulatory investment test (RIT-T).** Before a transmission upgrade over $8 million, a business must
   show the benefit outweighs the cost, and must consider non-network options such as demand response
   (NEM pp. 93–94; APR p. 21).
4. **George Town, the case to know** (APR pp. 52–53):
   - New load of 300 MW or more at George Town would at times be 60% or more of the whole State's load.
   - The planning rules say one equipment failure must not black out the State. If George Town carried that
     much, losing one transformer or the 220 kV busbar there could.
   - The option is a new substation with 550 Mvar of reactive support, costed at $370.6 million.
5. **The big projects:**
   - North West Transmission Developments stage 1: $1.317 billion, 129 km of double-circuit line (APR pp. 17, 22, 44).
   - Marinus Link: 1,500 MW, in two 750 MW stages (APR p. 17).
   - A known limit: Farrell–Sheffield carries up to 760 MW of West Coast generation over about 85 km (APR p. 55).
   - Spare capacity at each substation is listed in Table 4-1 (APR pp. 62–63).

**Notebook:** draw George Town in four boxes: the new load, the substation, the single failure, the State black.

**Check (send to Claude):**
1. Explain the George Town problem to a non-engineer in three sentences.
2. Besides building new lines, what must a regulatory investment test consider?
3. Why would a connections team care about the spare capacity in Table 4-1?

---

## Thursday 12: security and reliability

**Read (about 2 hours):**
- NEM course modules 8 and 9 (NEM pp. 203–270). Read these for understanding only.
- Report chapters 5 and 6 (APR pp. 77–106).

**Understand:**
1. **Settlements and hedging, in one line each:**
   - Settlement is weekly: energy × loss factor × the regional price (NEM pp. 215, 222).
   - Retailers and generators hedge the volatile spot price with contracts (NEM pp. 252–263).
   
   Know them; don't specialise in them.
2. **Inertia** (not in the course). Spinning generators store energy in their rotating mass. In the first
   instant after a failure, that stored energy slows the fall in frequency. Hydro machines provide plenty;
   wind, solar and HVDC links provide little on their own.
   - Tasmania's secure level is 3,800 MW.s (APR p. 82).
   - A deficit of 3,620 MW.s is forecast from 2029–30 (APR p. 83).
3. **System strength.** The grid's ability to hold its voltage steady during a fault, measured as fault level
   in MVA. Inverter-based generation needs a strong grid to stay connected and controllable.
   - Since 2 December 2025, TasNetworks must procure the *entire* amount of system strength (APR p. 80).
   - It contracts with existing synchronous machines until June 2029 (APR p. 83).
   - George Town is "a vulnerable location" (APR p. 87).
4. **Reliability is measured from the customer's side.**
   - SAIDI is average minutes without supply per customer per year; SAIFI is the number of interruptions.
   - In 2025–26, Urban and Regional Centres averaged 210.43 minutes against a standard of 120 (APR p. 100).
   - Transmission faults came mostly from vegetation, lightning and equipment (APR p. 99).
5. **Last lines of defence.**
   - Under-frequency load shedding trips at least 60% of each market customer's load in a severe event (APR p. 95).
   - Protection schemes keep any single loss within a 144 MW limit, including when Basslink trips (APR p. 96).

**Notebook:** one line each for inertia, system strength, SAIDI and SAIFI.

**Check (send to Claude):**
1. In your own words: what's the difference between inertia and system strength?
2. Urban SAIDI was 210 minutes against a standard of 120. Name two things an asset team might look at first.
3. Why does more wind and solar raise the need for system strength services?

**The course is complete today.** Tell Claude, and it moves to "complete" in your portfolio.

---

## Friday 13: write the one-page brief of the planning report

**Rules:**
- No more than 450 words.
- Your own words.
- Every number has its page.
- One optional sketch.
- Send the draft to Claude, who checks every figure against the report before it's published.

**Template:**

> **TasNetworks Annual Planning Report 2026: one-page brief** · *Chris Gogoi, November 2026*
>
> **What the report is** (1–2 sentences): who publishes it, why, and over what period.
>
> **The network today** (3 facts with pages): size, generation mix, demand.
>
> **What's changing** (3 points): AI factories, new renewables, Marinus Link and Basslink.
>
> **The hard problems** (3 points): George Town; system strength and inertia; one constraint.
>
> **How TasNetworks is responding** (3 points): North West Transmission Developments; contracts for system
> strength; risk-based asset replacement.
>
> **Two questions I'd ask an engineer there.**
>
> *Source: TasNetworks Annual Planning Report 2026, printed page numbers cited. Figures as stated by TasNetworks.*

---

## Saturday 14: write the asset-risk one-pager

**Topic:** *How a network business decides to replace a transformer.* This is where industrial and production
engineering is strongest: failure modes, risk, condition data and maintenance strategy.

**Understand first:**
- **Risk = likelihood of failure × consequence of failure.** A badly worn transformer feeding a few
  customers can matter less than a fair one feeding a city with no backup.
- **Condition** is how worn the asset actually is. Typical evidence for a power transformer includes:
  - gases dissolved in its oil (an early sign of internal faults);
  - oil quality and the state of its paper insulation;
  - loading and temperature history;
  - the tap changer and bushings.
  
  [ASSUMED: general industry practice, not stated in the report. Check TasNetworks' Strategic Asset
  Management Plan, which the report says is available on request (APR p. 117).]
- **Criticality** is how much a failure would hurt: customers affected, whether there's a backup (N-1),
  safety, and how long a replacement takes to arrive.
- **TasNetworks' approach:**
  - replacement "based on asset condition and risk, rather than age" (APR p. 111);
  - decisions by "overall risk (taking account of asset criticality and condition)" (APR p. 117).
- **Examples:** Sheffield T1, 2027, $10.7 million; Rosebery, 2028, $17.5 million (APR p. 71).

**Template (no more than 450 words):**
1. **The asset and its job:** what a network transformer does.
2. **How it fails:** three failure modes.
3. **What a failure costs:** customers, safety, repair time.
4. **How you'd know:** the condition evidence.
5. **How TasNetworks decides:** quote the approach and give the two examples, with pages.
6. **What an industrial engineer adds:** failure modes and effects analysis (FMEA), maintenance strategy, data quality.
7. **Limits:** written from public information only.

---

## Sunday 15: CV and interview practice

**Your CV, top section.** A three-line summary, filled in with your real details:

> Industrial and production engineer moving into electricity networks. Since October 2026: completed AEMO's NEM
> Foundations course, studied TasNetworks' 2026 Annual Planning Report, and built an evidence-based
> measurement and control project (Lupine). [N] years in [your real roles], bringing [two real strengths,
> such as process improvement and data analysis].

**Then three or four achievements from your past roles,** each as *action → result*. Prefer ones about:
- improving a process;
- working with data;
- managing risk;
- explaining technical things to non-specialists.

**Add the portfolio link.** Keep personal details on your CV only, never in the repository.

**Practise aloud.** For each question, give a 60 to 90 second answer and record it on your phone. Each question
lists what a strong answer covers; your answer must be your own.

1. **"Why the change into networks?"** Your story since 2017 in two sentences, then the evidence of what you've done since October.
2. **"What does TasNetworks do?"** Transmission and distribution; regulated by the AER; the system strength and inertia roles (APR p. 2).
3. **"What's the biggest challenge in our planning report?"** Pick one (George Town, system strength, or AI-factory load) and explain the trade-off.
4. **"Explain system strength."** Voltage holding steady through a fault; inverter-based generation; TasNetworks must procure all of it (APR p. 80).
5. **"How should we decide when to replace an asset?"** Risk = likelihood × consequence; condition and criticality, not age (APR pp. 111, 117).
6. **"What is a RIT-T?"** A cost-benefit test over $8 million; must consider non-network options (APR p. 21).
7. **"What does N-1 mean?"** Surviving the loss of any one element.
8. **"A data centre wants 100 MW. What happens?"** An enquiry, then a technical assessment: spare capacity, system strength, connection standards, then an agreement. Mention George Town's lesson.
9. **"Tell me about a time you used data to make a decision."** One real example from your work.
10. **"Tell me about a mistake."** Your 20 October mix-up of current and energy: what you got wrong, how you checked it, what you changed.

**The ten discussion points** in `research/2026-11-09-R-tasnetworks-apr-2026.md` are your revision list.

---

## Monday 16: apply

1. Check the careers page on TasNetworks' website, and set up job alerts.
2. Tailor your CV's top section to each role's own words.
3. Send one short, specific enquiry. TasNetworks invites them at careers@tasnetworks.com.au. Include:
   - who you are, in one line;
   - one insight from the planning report;
   - your portfolio link.
4. Also worth checking: Tasmanian energy employers with office-based technical roles, such as Hydro Tasmania
   and its consulting arm, and the Marinus Link project. [ASSUMED: check each employer's current openings.]
   Avoid billing, retail and general-operations roles: they aren't your direction.

**Then textbook Part 01 resumes,** at sitting 2.
