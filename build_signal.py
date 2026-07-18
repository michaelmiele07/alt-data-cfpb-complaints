#!/usr/bin/env python3
"""Complaint-velocity signal: monthly z-score of non-credit-reporting
complaint counts per ticker vs the company's own trailing 12 months.

Credit-reporting-product complaints are excluded from the signal (see
aggregate_mapped.py docstring) but kept in the data for transparency.

Output: out/monthly_signal.csv  (ticker, month, n, z)
        out/spike_table.txt     (recent spikes + all-time top spikes)
"""
import numpy as np
import pandas as pd
import pathlib

ROOT = pathlib.Path(__file__).parent
m = pd.read_csv(ROOT / "data" / "monthly_mapped.csv")
m["month"] = pd.PeriodIndex(m["month"], freq="M")

sig = (m[~m["credit_reporting"]]
       .groupby(["ticker", "month"])["n"].sum().rename("n").reset_index()
       .sort_values(["ticker", "month"]))

# fill missing months with zero within each ticker's active range
filled = []
for t, g in sig.groupby("ticker"):
    idx = pd.period_range(g["month"].min(), "2026-06", freq="M")
    s = g.set_index("month")["n"].reindex(idx, fill_value=0).rename("n")
    s.index.name = "month"
    filled.append(s.reset_index().assign(ticker=t))
sig = pd.concat(filled)

sig["logn"] = np.log1p(sig["n"])
grp = sig.groupby("ticker")["logn"]
sig["mu"] = grp.transform(lambda s: s.shift(1).rolling(12).mean())
sig["sd"] = grp.transform(lambda s: s.shift(1).rolling(12).std())
sig["z"] = (sig["logn"] - sig["mu"]) / sig["sd"].clip(lower=0.05)

# require real complaint flow for a z to be meaningful
active = sig.groupby("ticker")["n"].transform(
    lambda s: s.rolling(12, min_periods=12).median())
sig.loc[(active < 10) | sig["mu"].isna(), "z"] = np.nan

out = ROOT / "out"
out.mkdir(exist_ok=True)
sig[["ticker", "month", "n", "z"]].to_csv(out / "monthly_signal.csv", index=False)

recent = sig[(sig["month"] >= "2026-01") & (sig["z"] >= 2)]
top = sig.dropna(subset=["z"]).nlargest(15, "z")
lines = ["Recent spikes (z>=2, 2026 H1, non-credit-reporting complaints):", ""]
for _, r in recent.sort_values("z", ascending=False).iterrows():
    lines.append(f"  {r['ticker']:>5} {r['month']}  n={r['n']:>5.0f}  z={r['z']:.1f}")
lines += ["", "All-time top complaint-velocity spikes:", ""]
for _, r in top.iterrows():
    lines.append(f"  {r['ticker']:>5} {r['month']}  n={r['n']:>5.0f}  z={r['z']:.1f}")
(out / "spike_table.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
