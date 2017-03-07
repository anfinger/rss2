# -*- coding: utf8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import ReiseForm
from uuid import UUID
import re
from django.utils import timezone
from django import db
from collections import namedtuple, OrderedDict 
from django.db import connection
from itertools import chain
from django.core import serializers
from django.template.loader import render_to_string
#from django.utils.encoding import python_2_unicode_compatible

#from django.core.files.storage import DefaultStorage
#from filebrowser.sites import FileBrowserSite
#from filebrowser.sites import site

#from django.core.files.storage import FileSystemStorage

from .models import Reise, Reisetermine, Abfahrtszeiten, LeistungenReise, Reisebeschreibung, Reisetage, Reisepreise, Preis, ReisepreisZusatz, Zusatzleistung, Fruehbucherrabatt, Reisebilder, Reisekatalogzugehoerigkeit, Katalog

from .querysets import get_detail_hinweise_queryset, get_detail_angebote_queryset, get_detail_auftragsbestaetigungen_queryset

# Create your views here.

#site = FileBrowserSite(name='huhu', storage=DefaultStorage())
#site.directory = "/images/"
#site.storage.location = DefaultStorage().location

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

################################################################t.META.HTTP_REFERER }}
# Index Seite, Reisen Übersicht                                  #
##################################################################
def index(request):
    dibug = ''
    cursor = connection.cursor()
    cursor.execute("SELECT reiseID, reisen_reise.untertitel, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) ORDER BY RT.min_datum;")
    #cursor.execute("SELECT reiseID, reisen_reise.untertitel, einleitung, reisetyp, katalogseite, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reiseID) LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id);");
    termine = namedtuplefetchall(cursor)
    cursor.close()
    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)
    return render(request, 'reisen/index.html', {'termine': termine, 'dibug': dibug})

##################################################################
# Winterreisen 2016 2017                                         #
##################################################################
def winter2016_17(request):
    dibug = ''
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT reiseID, reisen_reise.untertitel, korrektur_bemerkung_intern, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = '5fcadf9947314b82ac79802e92585c39' ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()

    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)

    cursor = connection.cursor()
    cursor.execute("select DISTINCT reisen_reise.titel, korrektur_bemerkung_intern from reisen_reise left join reisen_reisekatalogzugehoerigkeit on (reiseID = reise_id_id) where katalog_id_id = '5fcadf9947314b82ac79802e92585c39';")
    korrekturen = namedtuplefetchall(cursor)
    cursor.close()

    return render(request, 'reisen/index.html', {'termine': termine, 'dibug': dibug, 'korrekturen': korrekturen })

##################################################################
# Winterreisen 2016 2017                                         #
##################################################################
def winter2017_18(request):
    dibug = ''
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT reiseID, neu, reisen_reise.untertitel, korrektur_bemerkung_intern, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = '21a8a8c913854f41865953f6f10f538f' ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()

    korrekturen = Reise.objects.select_related().filter(
        reisekatalogzugehoerigkeit__katalog_id='21a8a8c913854f41865953f6f10f538f'
      ).all()#.values(
#        'reiseID', 
 #       'titel',
  #      'korrektur_bemerkung_intern'
   #   ).distinct()

    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)

    #cursor = connection.cursor()
    #cursor.execute("select DISTINCT reisen_reise.titel, korrektur_bemerkung_intern from reisen_reise left join reisen_reisekatalogzugehoerigkeit on (reiseID = reise_id_id) where katalog_id_id = '21a8a8c913854f41865953f6f10f538f';")
    #korrekturen = namedtuplefetchall(cursor)
    #cursor.close()

    return render(request, 'reisen/index.html', {'termine': termine, 'dibug': dibug, 'korrekturen': korrekturen })


##################################################################
# XML Export Winterreisen 2016 2017                              #
##################################################################
def winter2016_17_export(request):

    #XMLSerializer = serializers.get_serializer("xml")
    #xml_serializer = XMLSerializer()
    #xml_serializer.serialize(Reise.objects.all())
    #data = xml_serializer.getvalue()

    #with open("/var/www/reiseservice-schwerin/rss2/media/termine.xml", "w") as out:
    #    xml_serializer.serialize(Reise.objects.all(), stream=out)

    #xml = render_to_string('xml_template.xml', {'query_set': query_set})

    cursor = connection.cursor()
    cursor.execute("SELECT reiseID, reisen_reise.untertitel, korrektur_bemerkung_intern, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = '5fcadf9947314b82ac79802e92585c39' ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()

    return render(request, 'reisen/export.xml', {'termine': termine })

##################################################################
# Winterreisen 2016 2017                                         #
##################################################################
#@python_2_unicode_compatible # For Python 3.4 and 2.7
def winter1617(request):
    dibug = ''
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT reiseID, RP.abpreis, reisen_kategorie.kategorie, reisen_reise.untertitel, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) left join reisen_reisekategorien on (reiseID = reisen_reisekategorien.reise_id_id) left join reisen_kategorie on (kategorieID = kategorie_id_id) left join (select reisen_reisepreise.reise_id_id, MIN(reisen_reisepreise.preis) AS abpreis from reisen_reisepreise GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reiseID = RP.reise_id_id) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = '5fcadf9947314b82ac79802e92585c39' AND reisen_kategorie.kategorie in ('Musicals & Shows','Weihnachts- & Silvesterreisen', 'Adventsreisen & Weihnachtsmärkte', 'Kuren, Gesundheits- und Wellnessreisen', 'Flusskreuzfahrten', 'Ostern', 'kombinierte Flug- und Busreisen', 'Frühlingsreisen', 'Herbstreisen', 'Winterreisen') ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()

    kategorien = ['Herbstreisen', u'Adventsreisen & Weihnachtsmärkte', u'Weihnachts- & Silvesterreisen', 'Winterreisen', u'Frühlingsreisen', 'Ostern', u'Kuren, Gesundheits- und Wellnessreisen', 'kombinierte Flug- und Busreisen', 'Flusskreuzfahrten', 'Musicals & Shows']

    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)

    return render(request, 'reisen/index_reisen_web_alt.html', {'termine': termine, 'dibug': dibug, 'kategorien': kategorien })

##################################################################
# Winterreisen 2016 2017                                         #
##################################################################
#@python_2_unicode_compatible # For Python 3.4 and 2.7
def winter1718(request):
    dibug = ''
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT reiseID, RP.abpreis, reisen_kategorie.kategorie, reisen_reise.untertitel, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) left join reisen_reisekategorien on (reiseID = reisen_reisekategorien.reise_id_id) left join reisen_kategorie on (kategorieID = kategorie_id_id) left join (select reisen_reisepreise.reise_id_id, MIN(reisen_reisepreise.preis) AS abpreis from reisen_reisepreise GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reiseID = RP.reise_id_id) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = '21a8a8c913854f41865953f6f10f538f' AND reisen_kategorie.kategorie in ('Musicals & Shows','Weihnachts- & Silvesterreisen', 'Adventsreisen & Weihnachtsmärkte', 'Kuren, Gesundheits- und Wellnessreisen', 'Flusskreuzfahrten', 'Ostern', 'kombinierte Flug- und Busreisen', 'Frühlingsreisen', 'Herbstreisen', 'Winterreisen') ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()

    kategorien = ['Herbstreisen', u'Adventsreisen & Weihnachtsmärkte', u'Weihnachts- & Silvesterreisen', 'Winterreisen', u'Frühlingsreisen', 'Ostern', u'Kuren, Gesundheits- und Wellnessreisen', 'kombinierte Flug- und Busreisen', 'Flusskreuzfahrten', 'Musicals & Shows']

    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)

    return render(request, 'reisen/index_reisen_web_alt.html', {'termine': termine, 'dibug': dibug, 'kategorien': kategorien })

########################################################
# XML Export alle Reisen nach Termin Winter2017/18     #
########################################################
def reisezielterminuebersicht(request):

    cursor = connection.cursor()
    cursor.execute("SET lc_time_names = 'de_DE';")
    cursor.execute("select date_format(reisen_reisetermine.datum_beginn, '%M') as Monat, reisen_reise.individualbuchbar, reisen_reise.neu, reisen_reise.titel as Reiseziel, CONCAT(date_format(reisen_reisetermine.datum_beginn,'%d.%m.'), '-', date_format(reisen_reisetermine.datum_ende,'%d.%m.%y')) as Termin, (to_days(reisen_reisetermine.datum_ende)-to_days(reisen_reisetermine.datum_beginn)+1) as Tage, katalogseite, anzahl_seiten_im_katalog, position_auf_seite, concat(katalogseite,if(anzahl_seiten_im_katalog>1,concat('|',katalogseite+1),'')) as Seite from reisen_reise left join reisen_reisetermine on (reisen_reise.reiseID = reisen_reisetermine.reise_id_id) left join reisen_reisekatalogzugehoerigkeit on(reisen_reise.reiseID = reisen_reisekatalogzugehoerigkeit.reise_id_id) where reisen_reisekatalogzugehoerigkeit.katalog_id_id = '21a8a8c913854f41865953f6f10f538f' AND date_format(reisen_reisetermine.datum_beginn, '%Y') > 2016 order by datum_beginn, datum_ende, katalogseite, position_auf_seite;")
    termine = namedtuplefetchall(cursor)

    month = ''
    for i in range(len(termine)):
      if termine[i].Monat != month:
        month = termine[i].Monat
      else:
        termine[i] = termine[i]._replace(Monat = '')
      if u'Kuren an der polnischen Ostseeküste' in termine[i].Reiseziel:
        termine[i] = termine[i]._replace(Reiseziel = u'Kuren an der polnischen Ostseeküste')
      if u'Kuren an der polnischen Ostseeküste' in termine[i-1].Reiseziel and u'Kuren an der polnischen Ostseeküste' in termine[i].Reiseziel and termine[i-1].Tage == termine[i].Tage:
        termine[i] = termine[i]._replace(Termin = '')
      if termine[i].individualbuchbar != '':
        termine[i] = termine[i]._replace(Reiseziel = termine[i].Reiseziel + ' (auch individuell buchbar)')
      #if (termine[i].anzahl_seiten_im_katalog == 0) and (termine[i].position_auf_seite == 1) and termine[i-1].Reiseziel != '':
        #termine[i-1] = termine[i-1]._replace(Reiseziel = termine[i-1].Reiseziel + ' (auch individuell buchbar)')
        #termine[i] = termine[i]._replace(Termin = '')

    cursor.close()

    ausgabeformat = request.GET.get('format')
    if ausgabeformat == 'html':
      return render(request, 'reisen/export_reiseterminuebersicht.html', {'termine': termine })
    else:
      return render(request, 'reisen/export_reiseterminuebersicht.xml', {'termine': termine })

########################################################
# XML Export alle Reisen nach Termin Sommer  2017      #
########################################################
def reiseterminuebersicht(request):

    cursor = connection.cursor()
    cursor.execute("SET lc_time_names = 'de_DE';")
    cursor.execute("select date_format(reisen_reisetermine.datum_beginn, '%M') as Monat, reisen_reise.individualbuchbar, reisen_reise.neu, reisen_reise.titel as Reiseziel, CONCAT(date_format(reisen_reisetermine.datum_beginn,'%d.%m.'), '-', date_format(reisen_reisetermine.datum_ende,'%d.%m.%y')) as Termin, (to_days(reisen_reisetermine.datum_ende)-to_days(reisen_reisetermine.datum_beginn)+1) as Tage, katalogseite, anzahl_seiten_im_katalog, position_auf_seite, concat(katalogseite,if(anzahl_seiten_im_katalog>1,concat('|',katalogseite+1),'')) as Seite from reisen_reise left join reisen_reisetermine on (reisen_reise.reiseID = reisen_reisetermine.reise_id_id) left join reisen_reisekatalogzugehoerigkeit on(reisen_reise.reiseID = reisen_reisekatalogzugehoerigkeit.reise_id_id) where reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' AND date_format(reisen_reisetermine.datum_beginn, '%Y') > 2016 order by datum_beginn, datum_ende, katalogseite, position_auf_seite;")
    termine = namedtuplefetchall(cursor)

    month = ''
    for i in range(len(termine)):
      if termine[i].Monat != month:
        month = termine[i].Monat
      else:
        termine[i] = termine[i]._replace(Monat = '')
      if u'Kuren an der polnischen Ostseeküste' in termine[i].Reiseziel:
        termine[i] = termine[i]._replace(Reiseziel = u'Kuren an der polnischen Ostseeküste')
      if u'Kuren an der polnischen Ostseeküste' in termine[i-1].Reiseziel and u'Kuren an der polnischen Ostseeküste' in termine[i].Reiseziel and termine[i-1].Tage == termine[i].Tage:
        termine[i] = termine[i]._replace(Termin = '')
      if termine[i].individualbuchbar != '':
        termine[i] = termine[i]._replace(Reiseziel = termine[i].Reiseziel + ' (auch individuell buchbar)')
      #if (termine[i].anzahl_seiten_im_katalog == 0) and (termine[i].position_auf_seite == 1) and termine[i-1].Reiseziel != '':
        #termine[i-1] = termine[i-1]._replace(Reiseziel = termine[i-1].Reiseziel + ' (auch individuell buchbar)')
        #termine[i] = termine[i]._replace(Termin = '')

    cursor.close()

    ausgabeformat = request.GET.get('format')
    if ausgabeformat == 'html':
      return render(request, 'reisen/export_reiseterminuebersicht.html', {'termine': termine })
    else:
      return render(request, 'reisen/export_reiseterminuebersicht.xml', {'termine': termine })

################################################################
# XML Export alle Reisen nach Zielregion/Kategorie Sommer 2017 #
################################################################
def reisezieluebersicht(request):

    cursor = connection.cursor()
    cursor.execute("SET lc_time_names = 'de_DE';")

    #cursor.execute("select * from ( (select DISTINCT reisen_reise.reiseID, reisen_reise.individualbuchbar, reisen_reise.neu, 'Kategorie' as kategorietyp, reisen_kategorie.kategorie, reisen_reise.korrektur_bemerkung_intern, reisen_reise.titel as Reise, (to_days(reisen_reisetermine.datum_ende)-to_days(reisen_reisetermine.datum_beginn)+1) as Tage, katalogseite, anzahl_seiten_im_katalog, position_auf_seite, concat(katalogseite,if(anzahl_seiten_im_katalog>1,concat('|',katalogseite+1),'')) as Seite, RP.preise from reisen_reise left join reisen_reisetermine on (reisen_reise.reiseID = reisen_reisetermine.reise_id_id) left join reisen_reisekatalogzugehoerigkeit on(reisen_reise.reiseID = reisen_reisekatalogzugehoerigkeit.reise_id_id) left join reisen_reisekategorien on (reisen_reise.reiseID = reisen_reisekategorien.reise_id_id) left join reisen_kategorie on (reisen_reisekategorien.kategorie_id_id = reisen_kategorie.kategorieID) left join (SELECT reisen_reisepreise.reise_id_id, GROUP_CONCAT(CONCAT(hauptpreis.titel, ': ', IF(reisen_reisepreise.kommentar = 'ab', 'ab ', ''), concat(replace(FORMAT(reisen_reisepreise.preis, 0),',','.'), ' €'), reisen_reisepreise.markierung, IF(reisen_reisepreise.kommentar = 'ab', ', ', IF(reisen_reisepreise.kommentar = '', ', ', concat(', ', reisen_reisepreise.kommentar, ', '))), IFNULL(subpreise.zpreis,'')) ORDER BY reisen_reisepreise.position ASC SEPARATOR ', ') as preise FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisen_reisepreiszusatz.reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(': ', subpreis.titel, replace(reisen_reisepreiszusatz.preis, '.', ',')), ' €'),  subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR ', ') as zpreis FROM reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisen_reisepreiszusatz.reisepreis_id_id) AS subpreise ON (reisen_reisepreise.reisepreisID = subpreise.reisepreis_id_id) GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reisen_reise.reiseID = RP.reise_id_id) where reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' AND date_format(reisen_reisetermine.datum_beginn, '%Y') > 2016 AND reisen_kategorie.kategorie in ('Wanderreisen', 'kombinierte Flug- und Busreisen', 'Flusskreuzfahrten') order by reisen_kategorie.kategorie, Seite) Union (select DISTINCT reisen_reise.reiseID, reisen_reise.individualbuchbar, reisen_reise.neu, 'Zielregion' as kategorietyp, reisen_zielregion.name, reisen_reise.korrektur_bemerkung_intern, reisen_reise.titel as Reise, (to_days(reisen_reisetermine.datum_ende)-to_days(reisen_reisetermine.datum_beginn)+1) as Tage, katalogseite, anzahl_seiten_im_katalog, position_auf_seite, concat(katalogseite,if(anzahl_seiten_im_katalog>1,concat('|',katalogseite+1),'')) as Seite, RP.preise from reisen_reise left join reisen_reisetermine on (reisen_reise.reiseID = reisen_reisetermine.reise_id_id) left join reisen_reisekatalogzugehoerigkeit on(reisen_reise.reiseID = reisen_reisekatalogzugehoerigkeit.reise_id_id) left join reisen_reisezielregionen on (reisen_reise.reiseID = reisen_reisezielregionen.reise_id_id) left join reisen_zielregion on (reisen_reisezielregionen.zielregion_id_id = reisen_zielregion.zielregionID) left join (SELECT reisen_reisepreise.reise_id_id, GROUP_CONCAT(CONCAT(hauptpreis.titel, ': ', IF(reisen_reisepreise.kommentar = 'ab', 'ab ', ''), concat(replace(FORMAT(reisen_reisepreise.preis, 0),',','.'), ' €'), reisen_reisepreise.markierung, IF(reisen_reisepreise.kommentar = 'ab', ', ', IF(reisen_reisepreise.kommentar = '', ', ', concat(', ', reisen_reisepreise.kommentar, ', '))), IFNULL(subpreise.zpreis,'')) ORDER BY reisen_reisepreise.position ASC SEPARATOR ', ') as preise FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisen_reisepreiszusatz.reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(': ', subpreis.titel, replace(reisen_reisepreiszusatz.preis, '.', ',')), ' €'),  subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR ', ') as zpreis FROM reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisen_reisepreiszusatz.reisepreis_id_id) AS subpreise ON (reisen_reisepreise.reisepreisID = subpreise.reisepreis_id_id) GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reisen_reise.reiseID = RP.reise_id_id) where reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' AND date_format(reisen_reisetermine.datum_beginn, '%Y') > 2016 AND reisen_zielregion.name in ('Deutschland', 'Benelux', 'Österreich / Schweiz', 'Tschechien / Slovakei / Ungarn / Rumänien', 'Frankreich', 'Italien', 'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 'Baltikum / Skandinavien / Finnland / Island', 'Polen', 'England / Schottland / Irland') order by reisen_zielregion.name, Seite)) as neuetabelle order by FIELD(neuetabelle.kategorie, 'Deutschland', 'Österreich / Schweiz', 'Benelux', 'Frankreich', 'Italien', 'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 'Tschechien / Slovakei / Ungarn / Rumänien', 'Polen', 'Baltikum / Skandinavien / Finnland / Island', 'England / Schottland / Irland', 'Wanderreisen', 'kombinierte Flug- und Busreisen', 'Flusskreuzfahrten'), katalogseite, position_auf_seite;")
    
    cursor.execute("select * from ( (select DISTINCT reisen_reise.reiseID, reisen_reise.individualbuchbar, reisen_reise.neu, 'Kategorie' as kategorietyp, reisen_kategorie.kategorie, reisen_reise.korrektur_bemerkung_intern, reisen_reise.titel as Reise, (to_days(reisen_reisetermine.datum_ende)-to_days(reisen_reisetermine.datum_beginn)+1) as Tage, katalogseite, anzahl_seiten_im_katalog, position_auf_seite, concat(katalogseite,if(anzahl_seiten_im_katalog>1,concat('|',katalogseite+1),'')) as Seite, RP.preise from reisen_reise left join reisen_reisetermine on (reisen_reise.reiseID = reisen_reisetermine.reise_id_id) left join reisen_reisekatalogzugehoerigkeit on(reisen_reise.reiseID = reisen_reisekatalogzugehoerigkeit.reise_id_id) left join reisen_reisekategorien on (reisen_reise.reiseID = reisen_reisekategorien.reise_id_id) left join reisen_kategorie on (reisen_reisekategorien.kategorie_id_id = reisen_kategorie.kategorieID) left join (SELECT reisen_reisepreise.reise_id_id, GROUP_CONCAT(CONCAT(hauptpreis.titel, ': ', IF(reisen_reisepreise.kommentar = 'ab', 'ab ', ''), concat(replace(FORMAT(reisen_reisepreise.preis, 0),',','.'), ' €'), reisen_reisepreise.markierung, IF(reisen_reisepreise.kommentar = 'ab', ', ', IF(reisen_reisepreise.kommentar = '', ', ', concat(', ', reisen_reisepreise.kommentar, ', '))), IFNULL(subpreise.zpreis,'')) ORDER BY reisen_reisepreise.position ASC SEPARATOR ', ') as preise FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisen_reisepreiszusatz.reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(': ', subpreis.titel, replace(FORMAT(reisen_reisepreiszusatz.preis, 0),',','.')), ' €'),  subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR ', ') as zpreis FROM reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisen_reisepreiszusatz.reisepreis_id_id) AS subpreise ON (reisen_reisepreise.reisepreisID = subpreise.reisepreis_id_id) GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reisen_reise.reiseID = RP.reise_id_id) where reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' AND date_format(reisen_reisetermine.datum_beginn, '%Y') > 2016 AND reisen_kategorie.kategorie in ('Wanderreisen', 'kombinierte Flug- und Busreisen', 'Flusskreuzfahrten') order by reisen_kategorie.kategorie, Seite) Union (select DISTINCT reisen_reise.reiseID, reisen_reise.individualbuchbar, reisen_reise.neu, 'Zielregion' as kategorietyp, reisen_zielregion.name, reisen_reise.korrektur_bemerkung_intern, reisen_reise.titel as Reise, (to_days(reisen_reisetermine.datum_ende)-to_days(reisen_reisetermine.datum_beginn)+1) as Tage, katalogseite, anzahl_seiten_im_katalog, position_auf_seite, concat(katalogseite,if(anzahl_seiten_im_katalog>1,concat('|',katalogseite+1),'')) as Seite, RP.preise from reisen_reise left join reisen_reisetermine on (reisen_reise.reiseID = reisen_reisetermine.reise_id_id) left join reisen_reisekatalogzugehoerigkeit on(reisen_reise.reiseID = reisen_reisekatalogzugehoerigkeit.reise_id_id) left join reisen_reisezielregionen on (reisen_reise.reiseID = reisen_reisezielregionen.reise_id_id) left join reisen_zielregion on (reisen_reisezielregionen.zielregion_id_id = reisen_zielregion.zielregionID) left join (SELECT reisen_reisepreise.reise_id_id, GROUP_CONCAT(CONCAT(hauptpreis.titel, ': ', IF(reisen_reisepreise.kommentar = 'ab', 'ab ', ''), concat(replace(FORMAT(reisen_reisepreise.preis, 0),',','.'), ' €'), reisen_reisepreise.markierung, IF(reisen_reisepreise.kommentar = 'ab', ', ', IF(reisen_reisepreise.kommentar = '', ', ', concat(', ', reisen_reisepreise.kommentar, ', '))), IFNULL(subpreise.zpreis,'')) ORDER BY reisen_reisepreise.position ASC SEPARATOR ', ') as preise FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisen_reisepreiszusatz.reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(': ', subpreis.titel, replace(FORMAT(reisen_reisepreiszusatz.preis, 0),',','.')), ' €'),  subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR ', ') as zpreis FROM reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisen_reisepreiszusatz.reisepreis_id_id) AS subpreise ON (reisen_reisepreise.reisepreisID = subpreise.reisepreis_id_id) GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reisen_reise.reiseID = RP.reise_id_id) where reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' AND date_format(reisen_reisetermine.datum_beginn, '%Y') > 2016 AND reisen_zielregion.name in ('Deutschland', 'Benelux', 'Österreich / Schweiz', 'Tschechien / Slovakei / Ungarn / Rumänien', 'Frankreich', 'Italien', 'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 'Baltikum / Skandinavien / Finnland / Island', 'Polen', 'England / Schottland / Irland') order by reisen_zielregion.name, Seite)) as neuetabelle order by FIELD(neuetabelle.kategorie, 'Deutschland', 'Österreich / Schweiz', 'Benelux', 'Frankreich', 'Italien', 'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 'Tschechien / Slovakei / Ungarn / Rumänien', 'Polen', 'Baltikum / Skandinavien / Finnland / Island', 'England / Schottland / Irland', 'Wanderreisen', 'kombinierte Flug- und Busreisen', 'Flusskreuzfahrten'), katalogseite, position_auf_seite;")
    termine = namedtuplefetchall(cursor)

    kategorie = ''
    for i in range(len(termine)):
      if termine[i].kategorie != kategorie:
        kategorie = termine[i].kategorie
      else:
        termine[i] = termine[i]._replace(kategorie = '')
      if termine[i].individualbuchbar != '':
        termine[i] = termine[i]._replace(Reise = termine[i].Reise + ' (auch individuell buchbar)')
      #if (termine[i].anzahl_seiten_im_katalog == 0) and (termine[i].position_auf_seite == 1) and  termine[i-1].Reise is not None:
        #termine[i-1] = termine[i-1]._replace(Reise = termine[i-1].Reise + ' (auch individuell buchbar)')
        #termine[i] = termine[i]._replace(Reise = None)

    cursor.close()

    ausgabeformat = request.GET.get('format')
    if ausgabeformat == 'html':
      return render(request, 'reisen/export_reisezieluebersicht.html', {'termine': termine })
    else:
      return render(request, 'reisen/export_reisezieluebersicht.xml', {'termine': termine })

##################################################################
# Winterreisen 2016 2017                                         #
##################################################################
#@python_2_unicode_compatible # For Python 3.4 and 2.7
def sommer17(request):
    dibug = ''
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT reiseID, RP.abpreis, reisen_reise.neu, reisen_reise.individualbuchbar, reisen_kategorie.kategorie, reisen_zielregion.name, reisen_reise.untertitel, korrektur_bemerkung_intern, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) left join reisen_reisekategorien on (reiseID = reisen_reisekategorien.reise_id_id) left join reisen_kategorie on (kategorieID = kategorie_id_id) left join reisen_reisezielregionen on (reiseID = reisen_reisezielregionen.reise_id_id) left join reisen_zielregion on (zielregionID = zielregion_id_id) left join (select reisen_reisepreise.reise_id_id, MIN(reisen_reisepreise.preis) AS abpreis from reisen_reisepreise GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reiseID = RP.reise_id_id) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()

    kategorien = [ u'Wanderreisen', u'kombinierte Flug- und Busreisen', u'Kuren, Gesundheits- und Wellnessreisen', u'Flusskreuzfahrten']
    zielregionen = [ u'Deutschland', u'Benelux', u'Schweiz / Österreich / Tschechien / Slovakei / Ungarn', u'Frankreich / Italien / Andorra', u'Portugal', u'England / Schottland / Irland', u'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', u'Baltikum / Skandinavien / Finnland / Island', u'Polen']

    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)

    termine_distinct = OrderedDict()
    for termin in termine:
      termine_distinct[termin.reiseID] = termin

    return render(request, 'reisen/index_sommerreisen_web_alt.html', {'termine_distinct': termine_distinct.values(), 'termine': termine, 'dibug': dibug, 'kategorien': kategorien, 'zielregionen': zielregionen })


##################################################################
# Detail Seite, Reisedetails                                     #
##################################################################
def reise_detail(request, pk):

    #dibug = request.GET['dibug']
    dibug = ''

    #data = serializers.serialize("xml", Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn'))

    qs = Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn')

    #XMLSerializer = serializers.get_serializer("xml")
    #xml_serializer = XMLSerializer()
    #xml_serializer.serialize(qs)
    #data = xml_serializer.getvalue()

    #with open("./file.xml", "w") as out:
    #    xml_serializer.serialize(qs, stream=out)

    #dibug = 'NIX PASSIERT'
    reise = get_object_or_404(Reise, pk=pk)
    termine = Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn')
    abfahrtszeiten = Abfahrtszeiten.objects.filter(reise_id=pk).order_by('position')
    leistungen = LeistungenReise.objects.filter(reise_id=pk).filter(nichtindividual=0).order_by('position')
    leistungennichtindividual = LeistungenReise.objects.filter(reise_id=pk).filter(nichtindividual=1).order_by('position')
    zusatzleistungen = Zusatzleistung.objects.filter(reise_id=pk).order_by('position')
    fruehbucherrabatte = Fruehbucherrabatt.objects.filter(reise_id=pk).order_by('datum_bis')
    tage = Reisetage.objects.filter(reise_id=pk).order_by('tagnummer')
    reisebeschreibung = Reisebeschreibung.objects.filter(reise_id=pk).order_by('position')
    # Tagnummerntext erzeugen, bei Beschreibungen für mehrere Tage, Tagnummer x. - y. Tag erzeugen
    for idx, tag in enumerate(tage):
      tag.reisetagID = str(tag.reisetagID).replace('-','')
      if tag.tagnummertext:
        tag.nummerntext = tag.tagnummertext
      else:
        naechster_tag = tage[(idx+1) % len(tage)]
        if len(tage) == 1:
            tag.nummerntext = ''
        elif (naechster_tag.tagnummer == (tag.tagnummer + 1)) or (idx == (len(tage)-1)):
            tag.nummerntext = str(tag.tagnummer) + '. Tag:'
        else:
            tag.nummerntext = str(tag.tagnummer) + '. - ' + str(naechster_tag.tagnummer-1) + '. Tag:'
    #preise = Reisepreise.objects.filter(reise_id=pk).order_by('position')
    #preistitel = Preis.objects.filter(reise_id=pk).order_by('position')
    #preiszusatz = ReisepreisZusatz

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, reisepreisID, hauptpreis.titel, REPLACE(FORMAT(reisen_reisepreise.preis, 0),',','.') as preis, reisen_reisepreise.markierung, kommentar, subpreise.zpreis FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(': ', subpreis.titel, replace(FORMAT(reisen_reisepreiszusatz.preis, 0),',','.')), ' €'), subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis from reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisepreis_id_id) AS subpreise ON (reisepreisID = reisepreis_id_id) WHERE reisen_reisepreise.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisepreise.position;");
    preise = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT ausflugspaketID, ausflugspaket_text, reisetag_id_id, reisen_ausflugspakete.titel AS aptitel, erscheint_in, kommentar_titel, kommentar, reisen_ausflugspakete.position, reisen_preis.titel as ptitel, tagnummer, reisen_reisetage.titel as rtitel, preis, apleistungen.leistungen FROM reisen_ausflugspakete LEFT JOIN (SELECT ausflugspaket_id_id, group_concat(leistung ORDER BY position ASC SEPARATOR '\n') AS leistungen FROM reisen_leistungenausflugspaket group by ausflugspaket_id_id) AS apleistungen ON (reisen_ausflugspakete.ausflugspaketID = apleistungen.ausflugspaket_id_id) LEFT JOIN reisen_ausflugspaketpreise ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketpreise.ausflugspaket_id_id) LEFT JOIN reisen_preis ON (reisen_preis.preisID = reisen_ausflugspaketpreise.preis_id_id) LEFT JOIN reisen_ausflugspaketezureisetagen ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketezureisetagen.ausflugspaket_id_id) LEFT JOIN reisen_reisetage ON (reisen_reisetage.reisetagID = reisen_ausflugspaketezureisetagen.reisetag_id_id) WHERE reisen_ausflugspakete.reise_id_id = '" + str(pk) + "' ORDER BY reisen_ausflugspakete.position;");
    aps = namedtuplefetchall(cursor)
    cursor.close()

    aps_distinct = OrderedDict()
    zusatzleistungen_distinct = OrderedDict()
    for ap in aps:
        # wenn Leistung vorhanden dann ist es ein AP
        if ap.leistungen:
          aps_distinct[ap.ausflugspaketID] = ap
        # wenn nicht dann ist es eine Zusatzleistung
        else:
          zusatzleistungen_distinct[ap.ausflugspaketID] = ap

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reisen_reisehinweise LEFT JOIN reisen_hinweis ON (reisen_reisehinweise.hinweis_id_id = reisen_hinweis.hinweisID) WHERE reisen_reisehinweise.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisehinweise.position;");
    hinweise = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reisen_reisekategorien LEFT JOIN reisen_kategorie ON (reisen_reisekategorien.kategorie_id_id = reisen_kategorie.kategorieID) WHERE reisen_reisekategorien.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisekategorien.position;");
    kategorien = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reisen_reisezielregionen LEFT JOIN reisen_zielregion ON (reisen_reisezielregionen.zielregion_id_id = reisen_zielregion.zielregionID) WHERE reisen_reisezielregionen.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisezielregionen.position;");
    zielregionen = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT bildID, zu_verwenden_in, bild, copyright, beschreibung, reisen_bild.titel as titel1, reisen_reisebilder.titel as titel2 FROM reisen_reisebilder LEFT JOIN reisen_bild ON (reisen_reisebilder.bild_id_id = reisen_bild.bildID) WHERE reisen_reisebilder.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisebilder.position;");
    bilder = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT reisen_katalog.katalogID, katalog_pdf, anzahl_seiten_im_katalog, katalogseite, reisen_katalog.titel FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) WHERE reisen_reisekatalogzugehoerigkeit.reise_id_id = '" + str(pk) + "' ORDER BY position;");
    kataloge = namedtuplefetchall(cursor)
    cursor.close()

    angebote = get_detail_angebote_queryset(pk)

    auftragsbestaetigungen = get_detail_auftragsbestaetigungen_queryset(pk)

    dibug = ''#request.GET.get('version')
    version = request.GET.get('version')
    kategorie_aktuell = request.GET.get('kategorie')
   
    #dibug = '' #querystring
    if version == 'alt':
        return render(
          request,
          'reisen/details_reisen_web_alt.html',
          {
              'reise': reise,
              'termine': termine,
              'abfahrtszeiten': abfahrtszeiten,
              'leistungen': leistungen,
              'leistungennichtindividual': leistungennichtindividual,
              'tage': tage,
              'reisebeschreibung': reisebeschreibung,
              'preise': preise,
              'aps': aps,
              'aps_distinct': aps_distinct.values(),
              'zusatzleistungen_distinct': zusatzleistungen_distinct.values(),
              'hinweise': hinweise,
              'kategorien': kategorien,
              'kategorie_aktuell': kategorie_aktuell,
              'zielregionen': zielregionen,
              'zusatzleistungen': zusatzleistungen,
              'fruehbucherrabatte': fruehbucherrabatte,
              'bilder': bilder,
              #'bild_str': bild_str,
              'kataloge': kataloge,
              'angebote': angebote,
              'auftragsbestaetigungen': auftragsbestaetigungen,
              'dibug': dibug,
          }
      )
    else:
        return render(
          request,
          'reisen/reise_detail.html',
          {
              'reise': reise,
              'termine': termine,
              'abfahrtszeiten': abfahrtszeiten,
              'leistungen': leistungen,
              'leistungennichtindividual': leistungennichtindividual,
              'tage': tage,
              'reisebeschreibung': reisebeschreibung,
              'preise': preise,
              'aps': aps,
              'aps_distinct': aps_distinct.values(),
              'zusatzleistungen_distinct': zusatzleistungen_distinct.values(),
              'hinweise': hinweise,
              'kategorien': kategorien,
              'zielregionen': zielregionen,
              'zusatzleistungen': zusatzleistungen,
              'fruehbucherrabatte': fruehbucherrabatte,
              'bilder': bilder,
              'kataloge': kataloge,
              'angebote': angebote,
              'auftragsbestaetigungen': auftragsbestaetigungen,
              'dibug': dibug,
          }
      )

##################################################################
# Detail Seite, Reisedetails                                     #
##################################################################
def reise_detail_export(request, pk):

    dibug = ''
    reise = get_object_or_404(Reise, pk=pk)
    termine = Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn')
    abfahrtszeiten = Abfahrtszeiten.objects.filter(reise_id=pk).order_by('position')

    for abfahrtszeit in abfahrtszeiten:
      if abfahrtszeit.ort == 'HBF':
        abfahrtszeit.ort = 'Hbf. Schwerin'
      elif abfahrtszeit.ort == 'VSB':
        abfahrtszeit.ort = 'HST "v. Stauffenberg Str."'
      elif abfahrtszeit.ort == 'ANK':
        abfahrtszeit.ort = 'Ankunft'
      elif abfahrtszeit.ort == 'GAR':
        abfahrtszeit.ort = 'Gartenstadt'

    leistungen = LeistungenReise.objects.filter(reise_id=pk).filter(nichtindividual=0).order_by('position')
    leistungennichtindividual = LeistungenReise.objects.filter(reise_id=pk).filter(nichtindividual=1).order_by('position')
    zusatzleistungen = Zusatzleistung.objects.filter(reise_id=pk).order_by('position')
    fruehbucherrabatte = Fruehbucherrabatt.objects.filter(reise_id=pk).order_by('datum_bis')
    tage = Reisetage.objects.filter(reise_id=pk).order_by('tagnummer')
    reisebeschreibung = Reisebeschreibung.objects.filter(reise_id=pk).order_by('position')
    # Tagnummerntext erzeugen, bei Beschreibungen für mehrere Tage, Tagnummer x. - y. Tag erzeugen
    pkquery = re.sub(r'[-]', '', str(pk))

    for idx, tag in enumerate(tage):
      	tag.reisetagID = str(tag.reisetagID).replace('-','')
        if tag.tagnummertext:
          tag.nummerntext = tag.tagnummertext + ' '
        else:
          naechster_tag = tage[(idx+1) % len(tage)]
          if len(tage) == 1:
              tag.nummerntext = ''
          elif (naechster_tag.tagnummer == (tag.tagnummer + 1)) or (idx == (len(tage)-1)):
              tag.nummerntext = str(tag.tagnummer) + '. Tag: '
          else:
              tag.nummerntext = str(tag.tagnummer) + '. - ' + str(naechster_tag.tagnummer-1) + '. Tag: '

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, reisepreisID, hauptpreis.titel, REPLACE(FORMAT(reisen_reisepreise.preis, 0),',','.') as preis, reisen_reisepreise.markierung, kommentar, subpreise.zpreis FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(':	', subpreis.titel, replace(FORMAT(reisen_reisepreiszusatz.preis, 0),',','.')), ' €'), subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis from reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisepreis_id_id) AS subpreise ON (reisepreisID = reisepreis_id_id) WHERE reisen_reisepreise.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisepreise.position;");
    preise = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT ausflugspaketID, ausflugspaket_text, reisetag_id_id, reisen_ausflugspakete.titel AS aptitel, erscheint_in, kommentar_titel, kommentar, reisen_ausflugspakete.position, reisen_preis.titel as ptitel, tagnummer, reisen_reisetage.titel as rtitel, preis, apleistungen.leistungen FROM reisen_ausflugspakete LEFT JOIN (SELECT ausflugspaket_id_id, group_concat(leistung ORDER BY position ASC SEPARATOR '\n') AS leistungen FROM reisen_leistungenausflugspaket group by ausflugspaket_id_id) AS apleistungen ON (reisen_ausflugspakete.ausflugspaketID = apleistungen.ausflugspaket_id_id) LEFT JOIN reisen_ausflugspaketpreise ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketpreise.ausflugspaket_id_id) LEFT JOIN reisen_preis ON (reisen_preis.preisID = reisen_ausflugspaketpreise.preis_id_id) LEFT JOIN reisen_ausflugspaketezureisetagen ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketezureisetagen.ausflugspaket_id_id) LEFT JOIN reisen_reisetage ON (reisen_reisetage.reisetagID = reisen_ausflugspaketezureisetagen.reisetag_id_id) WHERE reisen_ausflugspakete.reise_id_id = '" + pkquery + "' ORDER BY reisen_ausflugspakete.position;");
    aps = namedtuplefetchall(cursor)
    cursor.close()

    aps_distinct = OrderedDict()
    zusatzleistungen_distinct = OrderedDict()
    for ap in aps:
        # wenn Leistung vorhanden dann ist es ein AP
        if ap.leistungen:
          aps_distinct[ap.ausflugspaketID] = ap
        # wenn nicht dann ist es eine Zusatzleistung
        else:
          zusatzleistungen_distinct[ap.ausflugspaketID] = ap

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reisen_reisehinweise LEFT JOIN reisen_hinweis ON (reisen_reisehinweise.hinweis_id_id = reisen_hinweis.hinweisID) WHERE reisen_reisehinweise.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisehinweise.position;");
    hinweise = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reisen_reisekategorien LEFT JOIN reisen_kategorie ON (reisen_reisekategorien.kategorie_id_id = reisen_kategorie.kategorieID) WHERE reisen_reisekategorien.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisekategorien.position;");
    kategorien = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM reisen_reisezielregionen LEFT JOIN reisen_zielregion ON (reisen_reisezielregionen.zielregion_id_id = reisen_zielregion.zielregionID) WHERE reisen_reisezielregionen.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisezielregionen.position;");
    zielregionen = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    #cursor.execute("SELECT bild, beschreibung, reisen_bild.titel as titel1, reisen_reisebilder.titel as titel2 FROM reisen_reisebilder LEFT JOIN reisen_bild ON (reisen_reisebilder.bild_id_id = reisen_bild.bildID) WHERE reisen_reisebilder.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisebilder.position;");
    cursor.execute("SELECT REPLACE(bild,'images/','') as bild, beschreibung, reisen_bild.titel as titel1, reisen_reisebilder.titel as titel2, reisen_bildanbieter.bildanbieter as bildanbieter, bildnummer, copyright, url as bildurl, kommentar as bildkommentar FROM reisen_reisebilder LEFT JOIN reisen_bild ON (reisen_reisebilder.bild_id_id = reisen_bild.bildID) LEFT JOIN reisen_bildanbieter ON (reisen_bild.bildanbieter_id_id = reisen_bildanbieter.bildanbieterID) WHERE reisen_reisebilder.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisebilder.position;");
    bilder = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    #cursor.execute("SELECT katalog_pdf, anzahl_seiten_im_katalog, katalogseite, reisen_katalog.titel FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) WHERE reisen_reisekatalogzugehoerigkeit.reise_id_id = '" + str(pk) + "' ORDER BY position;");
    cursor.execute("SELECT anzahl_seiten_im_katalog, katalogseite, reisen_katalog.titel, position_auf_seite FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) WHERE reisen_reisekatalogzugehoerigkeit.reise_id_id = '" + pkquery + "' AND reisen_katalog.katalogID = 'fa81408e2b69488498ace5b91737d187'");
    katalog = namedtuplefetchall(cursor)
    cursor.close()

    bilder_anzeigen = request.GET.get('bilder')

    #dibug = '' #querystring
    if bilder_anzeigen == 'ja':
        return render(
          request,
          'reisen/reise_detail_export_mit_bildern.xml',
          {
          'reise': reise,
          'termine': termine,
          'abfahrtszeiten': abfahrtszeiten,
          'leistungen': leistungen,
          'leistungennichtindividual': leistungennichtindividual,
          'tage': tage,
          'reisebeschreibung': reisebeschreibung,
          'preise': preise,
          'aps': aps,
          'aps_distinct': aps_distinct.values(),
          'zusatzleistungen_distinct': zusatzleistungen_distinct.values(),
          'hinweise': hinweise,
          'kategorien': kategorien,
          'zielregionen': zielregionen,
          'zusatzleistungen': zusatzleistungen,
          'fruehbucherrabatte': fruehbucherrabatte,
          'bilder': bilder,
          'katalog': katalog[0],
          'dibug': dibug,
          }
        )
    elif bilder_anzeigen == 'nur':
      return render(
        request,
        'reisen/reise_detail_export_nur_bilder.xml',
        {
          'reise': reise,
          'termine': termine,
          'abfahrtszeiten': abfahrtszeiten,
          'leistungen': leistungen,
          'leistungennichtindividual': leistungennichtindividual,
          'tage': tage,
          'reisebeschreibung': reisebeschreibung,
          'preise': preise,
          'aps': aps,
          'aps_distinct': aps_distinct.values(),
          'zusatzleistungen_distinct': zusatzleistungen_distinct.values(),
          'hinweise': hinweise,
          'kategorien': kategorien,
          'zielregionen': zielregionen,
          'zusatzleistungen': zusatzleistungen,
          'fruehbucherrabatte': fruehbucherrabatte,
          'bilder': bilder,
          'katalog': katalog[0],
          'dibug': dibug,
        }
      )
    else:
      return render(
        request,
        'reisen/reise_detail_export.xml',
        {
          'reise': reise,
          'termine': termine,
          'abfahrtszeiten': abfahrtszeiten,
          'leistungen': leistungen,
          'leistungennichtindividual': leistungennichtindividual,
          'tage': tage,
          'reisebeschreibung': reisebeschreibung,
          'preise': preise,
          'aps': aps,
          'aps_distinct': aps_distinct.values(),
          'zusatzleistungen_distinct': zusatzleistungen_distinct.values(),
          'hinweise': hinweise,
          'kategorien': kategorien,
          'zielregionen': zielregionen,
          'zusatzleistungen': zusatzleistungen,
          'fruehbucherrabatte': fruehbucherrabatte,
          'bilder': bilder,
          'katalog': katalog[0],
          'dibug': dibug,
        }
      )
