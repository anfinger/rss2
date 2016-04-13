# -*- coding: utf-8 -*-

from django.db.models.expressions import RawSQL

# for use in 'RawSQL()'
#
_raw_str = ("`reisen_reisetermine`.`", "`")

# Format fields as YYYY-MM using 'RawSQL()'
#
_dt_str = "'%%d. %%m. %%Y'"
_nl_str = "' ... '"

_reference_date_fields = ('datum_beginn', 'datum_ende')
# wrapped as 'RawSQL(...)' call, see the note for the 'extra()' method here:
# >> https://docs.djangoproject.com/en/1.8/ref/models/querysets/#extra
#
reisetermine_rawsql = RawSQL(
    "GROUP_CONCAT(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(%s, %s), DATE_FORMAT(%s, %s)) ORDER BY %s ASC SEPARATOR ' \n ')" %
    # 'datum_beginn', '%%d. %%m. %%Y' ...
    #
    # (_reference_date_fields[0], _dt_str,
    #  _reference_date_fields[1], _dt_str,
    #  _reference_date_fields[0], _nl_str, ))
    (_reference_date_fields[0].join(_raw_str), _dt_str,
     _reference_date_fields[1].join(_raw_str), _dt_str,
     _reference_date_fields[0].join(_raw_str)), ())

dt_raw0 = RawSQL("DATE_FORMAT(`reisen_reisetermine`.`datum_beginn`, '%%d. %%m. %%Y')", ())
dt_raw1 = RawSQL("DATE_FORMAT(`reisen_reisetermine`.`datum_ende`, '%%d. %%m. %%Y')", ())
# REFERENCE_DATE_FIELDS_FORMATTED = [
#     RawSQL("DATE_FORMAT(%s, %s)" % (rdf.join(_raw_str), _dt_str), ()) for rdf in _reference_date_fields
#     ]

# SELECT
# 	reise_id_id,
# 	MIN(datum_beginn) AS min_datum,
#     group_concat(
# 		DISTINCT CONCAT_WS(
# 			' - ',
#             DATE_FORMAT(datum_beginn,'%d. %m. %Y'),
# 			DATE_FORMAT(datum_ende,'%d. %m. %Y'))
# 		ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine,
# 	reiseID,
#     titel,
#     untertitel,
#     einleitung,
#     reisetyp,
#     katalogseite
# FROM
# 	reisen_reisetermine INNER JOIN
#     reisen_reise ON (reise_id_id = reiseID)
# GROUP BY
# 	reise_id_id
# ORDER BY min_datum;
