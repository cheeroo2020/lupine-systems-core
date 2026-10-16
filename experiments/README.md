# Experiments

Every practical experiment is recorded here, from question to conclusion, so that anyone,
including you months later, can repeat it and check the result.

**No experiments yet.** Hardware is postponed until the fundamentals are in place (see the
timeline in `docs/handbook/handbook.md`, Part I).

---

## The rules

1. **One folder per experiment**, named by ID and a short name: `E001-ohms-law-resistor/`.
   IDs are never reused or renumbered.
2. **This folder holds the only authoritative copy of the raw measurements.** The handbook
   and the website summarise and link to them; they never copy them.
3. **Raw data is never edited.** If a value turns out to be wrong, it stays, and the
   correction goes in a separate, dated file or column with the reason.
4. **The prediction is written before measuring.** It doesn't get revised afterwards.
5. **Failed experiments are kept.** A failure, recorded honestly, is a result.
6. **Safety rules apply to every experiment:** 5 V USB power only, no mains work, no loose
   lithium cells, nothing left powered and unattended. These hold until we explicitly
   decide otherwise.

## What a folder contains

```
experiments/
└── E001-short-name/
    ├── README.md      the record, copied from TEMPLATE.md and filled in
    ├── data/          raw measurements as recorded (CSV preferred), with units in the header
    └── setup/         optional: wiring diagram, photos of the setup
```

Keep files small. A few MB per file is plenty for this kind of work, and GitHub rejects
files over 100 MB. The repository is public, so photos must not show anything private.

## Software tests are not physical validation

A passing test shows that the code does what the code says. It shows nothing about real
equipment. Every record states which of these it contains:

| Label | Means |
|---|---|
| **[SIMULATED]** | A result from software only |
| **[MEASURED]** | A value read from an instrument we used, with its uncertainty |
| **[VERIFIED]** | Checked by an independent instrument or method, with the scope stated |
| **[ASSUMED]** | Taken from a datasheet, rating plate or source without our own check |

## Index

| ID | Title | Date | Status | Handbook section |
|---|---|---|---|---|
| — | No experiments yet | — | — | — |
