"""Génère les passages du tram 28 de Lisbonne, lundi 16 novembre 2026 (graine 1616)."""
import csv, math, random, datetime as dt
from pathlib import Path
random.seed(1616)
STOPS = ["Martim Moniz", "Graça", "Portas do Sol", "Sé", "Baixa", "Chiado", "Estrela", "Prazeres"]
PULL = [0.45, 0.85, 1.0, 0.95, 0.8, 0.7, 0.45, 0.2]   # attractivité touristique le long de la ligne
rows, trip = [], 2800
t = dt.datetime(2026, 11, 16, 7, 0)
end = dt.datetime(2026, 11, 16, 22, 0)
while t <= end:
    trip += 1
    h = t.hour + t.minute / 60
    tour = math.exp(-((h - 13.5) ** 2) / (2 * 2.6 ** 2))          # vague touristique, pic vers 13 h 30
    work = 0.55 * math.exp(-((h - 8.3) ** 2) / 0.9) + 0.45 * math.exp(-((h - 18.2) ** 2) / 1.1)
    for i, (s, p) in enumerate(zip(STOPS, PULL)):
        base = 14 + 52 * tour * p + 26 * work * (0.6 + 0.4 * (i in (0, 4, 5)))
        load = max(2, int(random.gauss(base, 5)))
        rows.append([trip, t.strftime("%Y-%m-%d %H:%M:%S"), i + 1, s, load])
    t += dt.timedelta(minutes=random.choice([6, 7, 7, 8]))
out = Path(__file__).resolve().parent.parent / "data" / "rides" / "rides_2026-11-16.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["trip_id", "departed_at", "stop_seq", "stop", "on_board"]); w.writerows(rows)
