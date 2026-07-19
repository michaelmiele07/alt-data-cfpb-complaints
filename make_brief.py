#!/usr/bin/env python3
"""Render the one-page investment brief PDF (plain-English companion to the
technical note): premise, mechanism, affected companies, use cases."""
import pathlib

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, HRFlowable,
                                Table, TableStyle)

OUT = pathlib.Path(__file__).parent / "out"
INK, INK2, MUTED, RULE = "#0b0b0b", "#3d3c39", "#6b6a66", "#c3c2b7"

S = dict(
    title=ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=14.5, leading=17,
                         textColor=HexColor(INK), spaceAfter=2),
    sub=ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11,
                       textColor=HexColor(MUTED), spaceAfter=7),
    h=ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10, leading=13,
                     textColor=HexColor(INK), spaceBefore=8, spaceAfter=3),
    body=ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12.1,
                        textColor=HexColor(INK2), spaceAfter=4),
    bull=ParagraphStyle("bl", fontName="Helvetica", fontSize=9, leading=11.8,
                        textColor=HexColor(INK2), spaceAfter=2.5,
                        leftIndent=12, bulletIndent=2),
    cell=ParagraphStyle("c", fontName="Helvetica", fontSize=8, leading=10,
                        textColor=HexColor(INK2)),
    cellb=ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8, leading=10,
                         textColor=HexColor(INK)),
    foot=ParagraphStyle("f", fontName="Helvetica-Oblique", fontSize=7.5,
                        leading=9.5, textColor=HexColor(MUTED)),
)

def bullets(items):
    return [Paragraph(x, S["bull"], bulletText="•") for x in items]

def row(seg, names):
    return [Paragraph(seg, S["cellb"]), Paragraph(names, S["cell"])]

table = Table(
    [row("Credit bureaus", "EFX, TRU, EXPGY — highest volume; diluted by credit-repair templates (segmented out)"),
     row("Money-center banks", "JPM, BAC, WFC, C, USB, PNC, TFC, GS (consumer arm)"),
     row("Cards &amp; consumer credit", "COF (now incl. Discover), SYF, AXP, BFH"),
     row("Fintech / payments", "XYZ (Block/Cash App), PYPL, AFRM, SOFI, CHYM, HOOD, COIN"),
     row("Subprime lenders", "OMF, CACC, ENVA, OPRT, WRLD, RM"),
     row("Debt collectors", "ECPG, PRAA — complaint flow is their core operating externality"),
     row("Servicers", "RKT (incl. Mr. Cooper), RITM (Shellpoint), NNI")],
    colWidths=[1.35 * inch, 5.25 * inch])
table.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, HexColor("#e2e1d8")),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))

doc = SimpleDocTemplate(str(OUT / "cfpb_investment_brief.pdf"),
                        pagesize=letter, leftMargin=0.85 * inch,
                        rightMargin=0.85 * inch, topMargin=0.7 * inch,
                        bottomMargin=0.65 * inch)
story = [
    Paragraph("Where There's Smoke: Consumer Complaint Velocity as an Early Warning in Financials", S["title"]),
    Paragraph("Investment brief &nbsp;·&nbsp; Michael Miele &nbsp;·&nbsp; July 18, 2026 &nbsp;·&nbsp; "
              "companion to the technical note &nbsp;·&nbsp; github.com/michaelmiele07/alt-data-cfpb-complaints", S["sub"]),
    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceAfter=7),

    Paragraph("The premise", S["h"]),
    Paragraph(
        "Every consumer complaint filed with the CFPB against a financial company is public, timestamped, and named. "
        "When a lender's operations break — a botched servicing migration, a fee scheme, a fraud-handling failure — "
        "customers complain <i>before</i> the damage reaches earnings, reserves, or an enforcement headline. Tracking "
        "each company's complaint velocity against its own history turns 17 million filings into a monthly "
        "operational-stress monitor that costs nothing.", S["body"]),

    Paragraph("The mechanism — and its measured limits", S["h"]),
    *bullets([
        "The CFPB mines this same database to choose enforcement targets, so complaint spikes and regulatory risk "
        "are mechanically linked.",
        "The record is tight: <b>Block and Capital One spiked to all-time records in the exact month the CFPB sued "
        "each</b> (Jan 2025); Navient in the month of its 2017 suit; Wells Fargo around the $3.7B settlement.",
        "Measured limit: the pre-committed return test is a <b>null</b> (p=0.82) — a naive monthly long-short does "
        "not pay, because the biggest spikes coincide with already-public news. The value is monitoring, not "
        "mechanical ranking.",
    ]),

    Paragraph("The investable universe", S["h"]),
    table,

    Paragraph("How an investor would use it", S["h"]),
    *bullets([
        "<b>Risk overlay / avoid-list:</b> a sustained multi-month complaint build (not a one-month January blip) "
        "raises the odds of enforcement, remediation costs, and reserve builds — check any consumer-finance long "
        "against it.",
        "<b>Event anticipation:</b> slower builds that <i>precede</i> publicity are the leading component. Current "
        "watchlist: <b>AFRM and COF, June 2026 (z≈2.4–2.5 on record volume)</b> — pre-registered check, Jan 2027.",
        "<b>Diligence artifact:</b> the per-company complaint mix (fees vs fraud vs servicing) reads like a free "
        "operational audit of any servicer or fintech position.",
        "<b>Know the artifacts:</b> Rocket's 2026 spike is Mr. Cooper migration mechanics, not organic decay.",
    ]),

    Paragraph("What could mislead you", S["h"]),
    *bullets([
        "Spikes are partly reactive to news — confirmation more often than prediction.",
        "January is seasonally heavy; company attribution shifts with M&amp;A.",
        "The CFPB's political fortunes could change intake behavior (volumes at records through June 2026, so "
        "intake is currently healthy).",
    ]),

    HRFlowable(width="100%", thickness=0.7, color=HexColor(RULE), spaceBefore=5, spaceAfter=4),
    Paragraph("Data: CFPB public complaint database (public domain), 2011–June 2026. Methodology, validation, and "
              "the null result: out/cfpb_complaint_velocity_note.pdf. Research, not investment advice.", S["foot"]),
]
doc.build(story)
print("wrote", OUT / "cfpb_investment_brief.pdf")
