-- [Read tram] Script sur WH_Lisboa, type Requête : départs saturés, point noir, heure critique, record et la phrase msg pour Teams
WITH r AS (
  SELECT CAST(trip_id AS int) AS trip, CAST(departed_at AS datetime2(0)) AS t,
         stop, CAST(on_board AS int) AS ob
  FROM LH_Lisboa.dbo.rides
),
tr AS (SELECT trip, MIN(t) AS t, MAX(ob) AS peak FROM r GROUP BY trip),
s AS (
  SELECT stop, SUM(CASE WHEN ob > 58 THEN 1 ELSE 0 END) AS sat,
         AVG(CAST(ob AS decimal(6,1))) AS avg_ob
  FROM r GROUP BY stop
),
h AS (
  SELECT DATEPART(hour, t) AS hr, COUNT(*) AS n,
         SUM(CASE WHEN peak > 58 THEN 1 ELSE 0 END) AS sat,
         AVG(CAST(peak AS decimal(6,1))) AS avg_peak
  FROM tr GROUP BY DATEPART(hour, t)
),
k AS (
  SELECT
    (SELECT COUNT(*) FROM tr) AS trips,
    (SELECT COUNT(*) FROM tr WHERE peak > 58) AS full_trips,
    (SELECT MAX(ob) FROM r) AS max_on_board,
    (SELECT TOP 1 stop FROM s ORDER BY sat DESC, avg_ob DESC) AS worst_stop,
    (SELECT TOP 1 sat FROM s ORDER BY sat DESC, avg_ob DESC) AS worst_stop_sat,
    (SELECT TOP 1 hr FROM h ORDER BY avg_peak DESC) AS peak_hour,
    (SELECT TOP 1 CONCAT(sat, ' sur ', n) FROM h ORDER BY avg_peak DESC) AS peak_hour_sat
)
SELECT *,
  CONCAT('Tram 28, Lisbonne, 16 novembre 2026 : ', trips, ' départs, ',
    full_trips, ' saturés (plus de 58 à bord). ',
    'Point noir : ', worst_stop, ', ', worst_stop_sat, ' passages saturés. ',
    'Heure critique : ', peak_hour, ' h, ', peak_hour_sat, ' départs saturés. ',
    'Record : ', max_on_board, ' passagers.') AS msg
FROM k;
