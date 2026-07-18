#!/usr/bin/env python3
"""Aggregate the raw CFPB complaint CSV (~8.5 GB) to monthly counts.

Input : data/complaints.csv  (full public complaint database export)
Output: data/monthly_by_company.csv   (month, company, n)
        data/monthly_by_product.csv   (month, product, n)
        data/monthly_total.csv        (month, n)  -- intake-continuity check

Chunked single pass; only three columns are read.
"""
import pandas as pd
import pathlib

DATA = pathlib.Path(__file__).parent / "data"
USECOLS = ["Date received", "Company", "Product"]

by_company = {}
by_product = {}
total = {}

reader = pd.read_csv(DATA / "complaints.csv", usecols=USECOLS,
                     chunksize=1_000_000, dtype=str)
for i, chunk in enumerate(reader):
    month = pd.to_datetime(chunk["Date received"], errors="coerce").dt.to_period("M")
    chunk = chunk.assign(month=month).dropna(subset=["month"])
    for key, count in chunk.groupby(["month", "Company"]).size().items():
        by_company[key] = by_company.get(key, 0) + count
    for key, count in chunk.groupby(["month", "Product"]).size().items():
        by_product[key] = by_product.get(key, 0) + count
    for key, count in chunk.groupby("month").size().items():
        total[key] = total.get(key, 0) + count
    print(f"chunk {i}: {len(chunk)} rows", flush=True)

pd.Series(by_company).rename("n").rename_axis(["month", "company"]).reset_index() \
    .to_csv(DATA / "monthly_by_company.csv", index=False)
pd.Series(by_product).rename("n").rename_axis(["month", "product"]).reset_index() \
    .to_csv(DATA / "monthly_by_product.csv", index=False)
pd.Series(total).rename("n").rename_axis("month").reset_index() \
    .to_csv(DATA / "monthly_total.csv", index=False)
print("done")
