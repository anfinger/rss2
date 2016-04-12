

SELECT
  `reisen_reise`.`titel`,
  (GROUP_CONCAT(
      DISTINCT CONCAT_WS(
          ' - ', DATE_FORMAT(`reisen_reisetermine`.`datum_beginn`, '%d. %m. %Y'),
          DATE_FORMAT(`reisen_reisetermine`.`datum_ende`, '%d. %m. %Y')) ORDER BY
          `reisen_reisetermine`.`datum_beginn` ASC SEPARATOR '\n')) AS `rt`,
  MIN(`reisen_reisetermine`.`datum_beginn`) AS `min_dt`
FROM `reisen_reisetermine`
  INNER JOIN `reisen_reise` ON (`reisen_reisetermine`.`reise_id_id` = `reisen_reise`.`reiseID`)
GROUP BY `reisen_reise`.`titel`, `reisen_reisetermine`.`datum_beginn`, `reisen_reisetermine`.`datum_ende`,
  (GROUP_CONCAT(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(`reisen_reisetermine`.`datum_beginn`, '%d. %m. %Y'),
                                   DATE_FORMAT(`reisen_reisetermine`.`datum_ende`, '%d. %m. %Y')) ORDER BY
                `reisen_reisetermine`.`datum_beginn` ASC SEPARATOR ' ... '))
ORDER BY NULL;



# zu 'get_index_queryset_v1()
#
SELECT
  `reisen_reise`.`titel`,
  (GROUP_CONCAT(
      DISTINCT CONCAT_WS(
          ' - ', DATE_FORMAT(`reisen_reisetermine`.`datum_beginn`, '%d. %m. %Y'),
          DATE_FORMAT(`reisen_reisetermine`.`datum_ende`, '%d. %m. %Y')) ORDER BY
          `reisen_reisetermine`.`datum_beginn` ASC SEPARATOR '\n')) AS `rt`
FROM `reisen_reisetermine`
  INNER JOIN `reisen_reise` ON (`reisen_reisetermine`.`reise_id_id` = `reisen_reise`.`reiseID`);
