SELECT 
 DATETIME_ADD(DATETIME(datetime, 'UTC'), INTERVAL 2000 YEAR) as datetime,
 `MzPlocKroJad-C6H6-1g` as Plock_KJ,
 `MzPlocMiReja-C6H6-1g` as Plock_MR,
FROM `plock-air.2024_plock_air.2024_c6h6_raw`
WHERE
  datetime IS NOT NULL
  AND `MzPlocKroJad-C6H6-1g` IS NOT NULL
  AND `MzPlocMiReja-C6H6-1g` IS NOT NULL