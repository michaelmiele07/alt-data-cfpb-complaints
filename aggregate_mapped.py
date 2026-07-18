#!/usr/bin/env python3
"""Second aggregation pass: monthly counts for ticker-mapped companies,
split into credit-reporting product vs everything else.

Credit-reporting complaints are dominated by credit-repair-mill templates
(they tripled 2023-2026 across ALL bureaus simultaneously), so they are a
poor company-quality signal and are segmented out rather than mixed in.

Output: data/monthly_mapped.csv (month, ticker, company, credit_reporting, n)
"""
import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"

tickers = pd.read_csv(ROOT / "tickers.csv")
patterns = list(tickers.itertuples(index=False))

agg = {}
reader = pd.read_csv(DATA / "complaints.csv",
                     usecols=["Date received", "Company", "Product"],
                     chunksize=1_000_000, dtype=str)
for i, chunk in enumerate(reader):
    chunk["month"] = pd.to_datetime(chunk["Date received"],
                                    errors="coerce").dt.to_period("M")
    chunk = chunk.dropna(subset=["month", "Company"])
    chunk["credit_reporting"] = chunk["Product"].str.contains(
        "Credit reporting", case=False, na=False)
    for t in patterns:
        m = chunk[chunk["Company"].str.contains(t.company_pattern,
                                                case=False, regex=False)]
        if m.empty:
            continue
        for key, count in m.groupby(["month", "credit_reporting"]).size().items():
            k = (key[0], t.ticker, t.company_pattern, key[1])
            agg[k] = agg.get(k, 0) + count
    print(f"chunk {i}", flush=True)

out = (pd.Series(agg).rename("n")
         .rename_axis(["month", "ticker", "company", "credit_reporting"])
         .reset_index())
out.to_csv(DATA / "monthly_mapped.csv", index=False)
print("done:", len(out), "rows,", out["ticker"].nunique(), "tickers")
