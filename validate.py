#!/usr/bin/env python3
"""Validation: does complaint-velocity growth predict stock returns?

Design (pre-committed):
- Signal month M: YoY growth of trailing-3-month non-credit-reporting
  complaint counts per ticker (min 30 complaints in the trailing window).
- Return: month M+2 total return (one-month skip: complaints for month M
  are fully public by mid M+1 once companies respond).
- Cross-section: top-minus-bottom tertile mean return each month,
  2015-01..2026-05; two-sided permutation test, 2000 shuffles.

Foreign-listed ADRs and short-history names drop out where Yahoo lacks
data; the list is printed, not hidden.
"""
import numpy as np
import pandas as pd
import pathlib

import yfinance as yf

ROOT = pathlib.Path(__file__).parent
sig = pd.read_csv(ROOT / "out" / "monthly_signal.csv")
sig["month"] = pd.PeriodIndex(sig["month"], freq="M")
sig = sig.sort_values(["ticker", "month"])

sig["n3"] = sig.groupby("ticker")["n"].transform(lambda s: s.rolling(3).sum())
sig["growth"] = sig.groupby("ticker")["n3"].pct_change(12)
sig = sig.dropna(subset=["growth"])
sig = sig[(sig["n3"] >= 30) & (sig["month"] >= "2015-01") & (sig["month"] <= "2026-04")]

tickers = sorted(sig["ticker"].unique())
px = yf.download(tickers, start="2014-01-01", end="2026-07-17",
                 progress=False, auto_adjust=True)["Close"]
got = [t for t in tickers if t in px.columns and px[t].notna().sum() > 100]
print(f"prices for {len(got)}/{len(tickers)}; missing: {sorted(set(tickers)-set(got))}")
monthly = px[got].resample("ME").last()
rets = monthly.pct_change()
rets.index = rets.index.to_period("M")

def fwd(t, m):
    try:
        return rets.at[m + 2, t]
    except KeyError:
        return np.nan

sig = sig[sig["ticker"].isin(got)].copy()
sig["fwd_ret"] = [fwd(t, m) for t, m in zip(sig["ticker"], sig["month"])]
sig = sig.dropna(subset=["fwd_ret"])

spreads = []
for m, g in sig.groupby("month"):
    if len(g) < 9:
        continue
    g = g.sort_values("growth")
    k = len(g) // 3
    spreads.append(g.tail(k)["fwd_ret"].mean() - g.head(k)["fwd_ret"].mean())

obs = float(np.mean(spreads))
rng = np.random.default_rng(42)
perm = []
for _ in range(2000):
    ps = []
    for m, g in sig.groupby("month"):
        if len(g) < 9:
            continue
        r = g["fwd_ret"].to_numpy(copy=True)
        rng.shuffle(r)
        k = len(g) // 3
        ps.append(r[-k:].mean() - r[:k].mean())
    perm.append(np.mean(ps))
p = float((np.abs(np.asarray(perm)) >= abs(obs)).mean())

report = [
    f"months tested: {len(spreads)} (>=9 names each)",
    f"mean top-minus-bottom tertile fwd 1-mo return (M+2): {obs:+.2%}",
    f"two-sided permutation p (2000 shuffles): {p:.3f}",
    "sign convention: positive = rising complaints -> HIGHER returns",
]
print("\n".join(report))
(ROOT / "out" / "validation_result.txt").write_text("\n".join(report) + "\n")
