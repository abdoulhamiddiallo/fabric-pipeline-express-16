-- [Contrôle] point de terminaison SQL de LH_Lisboa, après l'exécution 2
SELECT stop_seq, stop,
       COUNT(*) AS passages,
       SUM(CASE WHEN CAST(on_board AS int) > 58 THEN 1 ELSE 0 END) AS satures,
       CAST(AVG(CAST(on_board AS decimal(6,1))) AS decimal(5,1)) AS moyenne_a_bord
FROM dbo.rides
GROUP BY stop_seq, stop
ORDER BY stop_seq;
