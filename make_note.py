#!/usr/bin/env python3
"""Render the ~1.5 page research note PDF (house style of prior notes)."""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Image,
                                HRFlowable)

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"
INK, INK2, MUTED, RULE = "#0b0b0b", "#3d3c39", "#6b6a66", "#c3c2b7"

# ---- figure: Block & Capital One complaint velocity with lawsuit markers
sig = pd.read_csv(OUT / "monthly_signal.csv")
sig["month"] = pd.PeriodIndex(sig["month"], freq="M").to_timestamp()
fig, ax = plt.subplots(figsize=(6.6, 2.3), dpi=200)
for t, color in [("XYZ", "#0b0b0b"), ("COF", "#a03828")]:
    g = sig[(sig["ticker"] == t) & (sig["month"] >= "2022-01")]
    ax.plot(g["month"], g["n"], lw=1.4, color=color,
            label={"XYZ": "Block (Cash App)", "COF": "Capital One"}[t])
ax.axvline(pd.Timestamp("2025-01-15"), color="#6b6a66", lw=0.8, ls="--")
ax.text(pd.Timestamp("2025-02-01"), ax.get_ylim()[1] * 0.92,
        "CFPB sues both,\nJan 2025", fontsize=6.5, color="#6b6a66")
ax.set_ylabel("complaints/mo (ex credit-reporting)", fontsize=7)
ax.legend(fontsize=7, frameon=False)
ax.tick_params(labelsize=7)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "figure1.png", bbox_inches="tight")

S = dict(
    title=ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=15, leading=18,
                         textColor=HexColor(INK), spaceAfter=2),
    sub=ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11,
                       textColor=HexColor(MUTED), spaceAfter=8),
    h=ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13,
                     textColor=HexColor(INK), spaceBefore=9, spaceAfter=3),
    body=ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12.3,
                        textColor=HexColor(INK2), spaceAfter=5),
    foot=ParagraphStyle("f", fontName="Helvetica-Oblique", fontSize=7.5,
                        leading=9.5, textColor=HexColor(MUTED)),
)

doc = SimpleDocTemplate(str(OUT / "cfpb_complaint_velocity_note.pdf"),
                        pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.65 * inch)
story = [
    Paragraph("Complaint Velocity II: CFPB Consumer Complaints as a "
              "Quality Signal for Financial Stocks", S["title"]),
    Paragraph("Alt-data research note &nbsp;·&nbsp; Michael Miele &nbsp;·&nbsp; "
              "July 18, 2026 &nbsp;·&nbsp; CFPB complaint database through "
              "June 2026 (17.0M complaints)", S["sub"]),
    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceAfter=8),

    Paragraph("Data and signal construction", S["h"]),
    Paragraph(
        "I aggregated the CFPB's full public complaint database — <b>17.0M complaints, 2011–June 2026</b> — to "
        "monthly counts per company and mapped 47 companies to listed tickers (banks, card issuers, servicers, "
        "collectors, fintechs). Credit-reporting-product complaints are segmented out of the signal: they tripled "
        "2023–2026 across all three bureaus simultaneously on credit-repair-mill templates and measure filing "
        "industrialization, not issuer quality. The signal is each company's monthly non-credit-reporting complaint "
        "count z-scored against its own trailing 12 months (log scale, minimum flow filters). Intake is alive and "
        "growing post-2025 CFPB turmoil: the bureau logged a record 784K complaints in June 2026.", S["body"]),

    Paragraph("The signal finds real blowups", S["h"]),
    Paragraph(
        "Every all-time top spike lines up with a documented event: <b>Block z=29.8 in Jan 2025</b> (CFPB Cash App "
        "lawsuit), <b>Capital One z=19.1</b> the same month (360 Savings suit), <b>Navient z=11.5 in Jan 2017</b> "
        "(CFPB suit), <b>Wells Fargo z=10.5 in Jan 2023</b> (the $3.7B settlement window). Honest caveat: part of "
        "each spike is <i>reactive</i> — enforcement publicity drives filings — so the z-score is best read as a "
        "coincident stress-confirmation layer, with the leading content in slower complaint builds. January also "
        "carries seasonal intake; the return test below uses YoY growth, which absorbs it.", S["body"]),
    Image(str(OUT / "figure1.png"), width=6.4 * inch, height=2.23 * inch),

    Paragraph("Pre-committed return test: an honest null", S["h"]),
    Paragraph(
        "Cross-sectional tertile test, 131 months 2015–2026, ~40 names: rank by YoY growth of trailing-3-month "
        "complaints, hold the forward month at M+2 (complaints fully public by then). Result: <b>+0.07%/month "
        "top-minus-bottom, permutation p = 0.82</b> — no return predictability at this horizon, consistent with "
        "complaints being public, fast-priced information. The same honest-null structure as my H-1B study: the "
        "data measures something real (see spike table), but the naive monthly long-short does not pay.", S["body"]),

    Paragraph("Current watchlist and pre-registered check", S["h"]),
    Paragraph(
        "2026-H1 spikes (z≥2, ex-January): <b>Affirm and Capital One in June 2026</b> (z≈2.4–2.5, the COF print on "
        "record volume of 2,583/month), Rithm/Shellpoint in June, Rocket in Q1 (z=5.6 — flagged as a likely "
        "structural artifact of the Mr. Cooper servicing migration, not organic deterioration). <b>Check by "
        "January 2027:</b> do the AFRM/COF June builds escalate into regulatory action, credit losses, or guidance "
        "cuts — or revert to baseline? Logged here before the outcome is knowable.", S["body"]),

    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE),
               spaceBefore=6, spaceAfter=4),
    Paragraph("Pipeline: github.com/michaelmiele07/alt-data-cfpb-complaints — fetch → aggregate → ticker map → "
              "z-score signal → permutation validation. CFPB data is public domain. Research, not investment "
              "advice. Companion to my NHTSA vehicle-quality note (same method, different regulator).", S["foot"]),
]
doc.build(story)
print("wrote", OUT / "cfpb_complaint_velocity_note.pdf")
