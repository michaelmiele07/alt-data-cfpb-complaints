# CFPB Complaint Velocity → Financial-Sector Quality Signal

Monthly consumer-complaint velocity per public financial company, built from
the CFPB's full public complaint database (17M complaints, 2011–present).
The financial-sector analog of my
[NHTSA vehicle-quality signal](https://github.com/michaelmiele07/alt-data-vehicle-quality):
regulatory exhaust → company-level quality signal, validated honestly.

## Pipeline

| step | script | output |
|---|---|---|
| fetch | `fetch.py` | `data/complaints.csv` (8.5 GB, not committed) |
| aggregate | `aggregate.py` | monthly counts by company / product / total |
| map + segment | `aggregate_mapped.py` + `tickers.csv` | monthly counts for 47 ticker-mapped companies, credit-reporting product segmented out |
| signal | `build_signal.py` | z-score of monthly non-credit-reporting complaints vs company's own trailing 12 months |
| validate | `validate.py` | cross-sectional return test, permutation p-value |

## What the signal catches (case validation)

Every top-decile historical spike coincides with a documented, verifiable
event — the signal finds real blowups:

| spike | z | event |
|---|---|---|
| Block (XYZ) 2025-01 | 29.8 | CFPB sues Block over Cash App fraud handling (Jan 2025) |
| Capital One 2025-01 | 19.1 | CFPB sues COF over 360 Savings rates (Jan 2025) |
| Navient 2017-01 | 11.5 | CFPB sues Navient (Jan 2017) |
| Wells Fargo 2023-01 | 10.5 | $3.7B CFPB settlement (Dec 2022) |

Caveat reported honestly: several spikes are partly **reactive** — lawsuit
publicity drives complaint filing — so a spike is a coincident/confirming
indicator of stress, not always a leading one. January months also carry
strong seasonal intake (post-holiday billing disputes); the return test uses
YoY growth, which absorbs seasonality.

## Honest null on returns

Pre-committed cross-sectional test (2015–2026, 131 months, ~40 names):
top-minus-bottom tertile of complaint growth, forward 1-month return at M+2:
**+0.07%/month, permutation p = 0.82 — no return predictability at this
horizon.** Same result structure as my H-1B project: the alt-data measures
something real (see case table), but the naive monthly long-short doesn't
pay. Plausible reasons: complaints are public and fast-priced, and the
biggest spikes coincide with already-public enforcement news.

## Known artifacts (documented, not hidden)

- **Credit-reporting flood:** complaints against the three bureaus tripled
  2023–2026 on credit-repair-mill templates; the credit-reporting product is
  segmented out of the signal (kept in data).
- **M&A attribution:** Discover→COF (2025-05), Mr. Cooper→RKT (2025-10).
  RKT's 2026 spike (z=5.6) is likely servicing-migration complaints from the
  Mr. Cooper integration — structural, not organic deterioration.
- **Survivorship in the return test:** COOP lacks Yahoo history post-delisting.

## Pre-registered check (2026-Q4)

The 2026-H1 spike list (`out/spike_table.txt`) includes AFRM and COF
(2026-06, z≈2.4–2.5). Check by January 2027: do these escalate into
regulatory action, credit losses, or guidance cuts — or revert?

Data: CFPB complaint database is public domain. This is research, not
investment advice.

## Deliverables

- Technical research note: [`out/cfpb_complaint_velocity_note.pdf`](out/cfpb_complaint_velocity_note.pdf)
- One-page investment brief (idea, companies, angle): [`out/cfpb_investment_brief.pdf`](out/cfpb_investment_brief.pdf)
