"""Recalcule ce que doit renvoyer Read tram, à partir du CSV brut (capacité 58)."""
import csv
from collections import defaultdict
from pathlib import Path

CAP = 58
CSV = Path(__file__).resolve().parent.parent / "data" / "rides" / "rides_2026-11-16.csv"
rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
trips = defaultdict(list)
for r in rows:
    trips[r["trip_id"]].append(r)
peak = {k: max(int(x["on_board"]) for x in v) for k, v in trips.items()}
full = sum(p > CAP for p in peak.values())
print(f"{len(rows)} passages, {len(trips)} départs, {full} saturés ({100 * full / len(trips):.1f} %)")
print(f"record : {max(int(r['on_board']) for r in rows)} passagers\n")
stops = defaultdict(list)
for r in rows:
    stops[(int(r["stop_seq"]), r["stop"])].append(int(r["on_board"]))
print("arrêt                 saturés  moyenne")
for (n, s), v in sorted(stops.items()):
    print(f"{n} {s:<20} {sum(x > CAP for x in v):>6}  {sum(v) / len(v):>7.1f}")
hours = defaultdict(list)
for k, v in trips.items():
    hours[int(v[0]["departed_at"][11:13])].append(peak[k])
print("\nheure  départs  saturés  pic moyen")
for h, v in sorted(hours.items()):
    print(f"{h:>4} h {len(v):>7} {sum(x > CAP for x in v):>8} {sum(v) / len(v):>10.1f}")
