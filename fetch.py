#!/usr/bin/env python3
"""Download the full CFPB consumer-complaint database (public domain).

Primary source: Consumer Financial Protection Bureau complaint database
bulk export. ~1.3 GB zipped / ~8.5 GB CSV; not committed to git.
"""
import pathlib
import subprocess

URL = "https://files.consumerfinance.gov/ccdb/complaints.csv.zip"
DATA = pathlib.Path(__file__).parent / "data"
DATA.mkdir(exist_ok=True)
dest = DATA / "complaints.csv.zip"
subprocess.run(["curl", "-s", "-o", str(dest), URL], check=True)
subprocess.run(["unzip", "-o", "-q", str(dest), "-d", str(DATA)], check=True)
print("done:", dest)
