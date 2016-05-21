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
    cursor.execute("SELECT reiseID, reisen_reise.untertitel, korrektur_bemerkung_intern, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = '5fcadf9947314b82ac79802e92585c39' ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()
    dibug = ''#DefaultStorage().location + '  :::  ' + site.storage.location + site.directory + '  :::  ' + str(FileSystemStorage().directory_permissions_mode)
    return render(request, 'reisen/index.html', {'termine': termine, 'dibug': dibug})

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
    leistungen = LeistungenReise.objects.filter(reise_id=pk).order_by('position')
    zusatzleistungen = Zusatzleistung.objects.filter(reise_id=pk).order_by('position')
    fruehbucherrabatte = Fruehbucherrabatt.objects.filter(reise_id=pk).order_by('datum_bis')
    tage = Reisetage.objects.filter(reise_id=pk).order_by('tagnummer')
    reisebeschreibung = Reisebeschreibung.objects.filter(reise_id=pk).order_by('position')
    # Tagnummerntext erzeugen, bei Beschreibungen für mehrere Tage, Tagnummer x. - y. Tag erzeugen
    for idx, tag in enumerate(tage):
        tag.reisetagID = str(tag.reisetagID).replace('-','')
        naechster_tag = tage[(idx+1) % len(tage)]
        if len(tage) == 1:
            tag.nummerntext = ''
        elif (naechster_tag.tagnummer == (tag.tagnummer + 1)) or (idx == (len(tage)-1)):
            tag.nummerntext = str(tag.tagnummer) + '. Tag: '
        else:
            tag.nummerntext = str(tag.tagnummer) + '. - ' + str(naechster_tag.tagnummer-1) + '. Tag: '
    #preise = Reisepreise.objects.filter(reise_id=pk).order_by('position')
    #preistitel = Preis.objects.filter(reise_id=pk).order_by('position')
    #preiszusatz = ReisepreisZusatz

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, reisepreisID, hauptpreis.titel, reisen_reisepreise.preis, kommentar, subpreise.zpreis FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisepreis_id_id, GROUP_CONCAT(CONCAT(CONCAT_WS(': ', subpreis.titel, replace(reisen_reisepreiszusatz.preis, '.', ',')), ' EUR') ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis from reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisepreis_id_id) AS subpreise ON (reisepreisID = reisepreis_id_id) WHERE	reisen_reisepreise.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisepreise.position;");
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
    cursor.execute("SELECT bild, beschreibung, reisen_bild.titel as titel1, reisen_reisebilder.titel as titel2 FROM reisen_reisebilder LEFT JOIN reisen_bild ON (reisen_reisebilder.bild_id_id = reisen_bild.bildID) WHERE reisen_reisebilder.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisebilder.position;");
    bilder = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT katalog_pdf, anzahl_seiten_im_katalog, katalogseite, reisen_katalog.titel FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) WHERE reisen_reisekatalogzugehoerigkeit.reise_id_id = '" + str(pk) + "' ORDER BY position;");
    kataloge = namedtuplefetchall(cursor)
    cursor.close()

    angebote = get_detail_angebote_queryset(pk)

    auftragsbestaetigungen = get_detail_auftragsbestaetigungen_queryset(pk)

    #dibug = '' #querystring
    return render(
        request,
        'reisen/reise_detail.html',
        {
            'reise': reise,
            'termine': termine,
            'abfahrtszeiten': abfahrtszeiten,
            'leistungen': leistungen,
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
        })

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
        abfahrtszeit.ort = 'HST v. Stauffenberg Str.'
      elif abfahrtszeit.ort == 'ANK':
        abfahrtszeit.ort = 'Ankunft'
      elif abfahrtszeit.ort == 'GAR':
        abfahrtszeit.ort = 'Gartenstadt'

    leistungen = LeistungenReise.objects.filter(reise_id=pk).order_by('position')
    zusatzleistungen = Zusatzleistung.objects.filter(reise_id=pk).order_by('position')
    fruehbucherrabatte = Fruehbucherrabatt.objects.filter(reise_id=pk).order_by('datum_bis')
    tage = Reisetage.objects.filter(reise_id=pk).order_by('tagnummer')
    reisebeschreibung = Reisebeschreibung.objects.filter(reise_id=pk).order_by('position')
    # Tagnummerntext erzeugen, bei Beschreibungen für mehrere Tage, Tagnummer x. - y. Tag erzeugen
    pkquery = re.sub(r'[-]', '', str(pk))

    for idx, tag in enumerate(tage):
        tag.reisetagID = str(tag.reisetagID).replace('-','')
        naechster_tag = tage[(idx+1) % len(tage)]
        if len(tage) == 1:
            tag.nummerntext = ''
        elif (naechster_tag.tagnummer == (tag.tagnummer + 1)) or (idx == (len(tage)-1)):
            tag.nummerntext = str(tag.tagnummer) + '. Tag: '
        else:
            tag.nummerntext = str(tag.tagnummer) + '. - ' + str(naechster_tag.tagnummer-1) + '. Tag: '

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, reisepreisID, hauptpreis.titel, reisen_reisepreise.preis, kommentar, subpreise.zpreis FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisepreis_id_id, GROUP_CONCAT(CONCAT(CONCAT_WS(': ', subpreis.titel, replace(reisen_reisepreiszusatz.preis, '.', ',')), ' EUR') ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis from reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisepreis_id_id) AS subpreise ON (reisepreisID = reisepreis_id_id) WHERE	reisen_reisepreise.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisepreise.position;");
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
    cursor.execute("SELECT bild, beschreibung, reisen_bild.titel as titel1, reisen_reisebilder.titel as titel2, reisen_bildanbieter.bildanbieter, reisen_bildanbieterzubild.bildnummer, reisen_bildanbieterzubild.url as bildurl, reisen_bildanbieterzubild.kommentar as bildkommentar FROM reisen_reisebilder LEFT JOIN reisen_bild ON (reisen_reisebilder.bild_id_id = reisen_bild.bildID) LEFT JOIN reisen_bildanbieterzubild ON (reisen_bild.bildID = reisen_bildanbieterzubild.bild_id_id) LEFT JOIN reisen_bildanbieter ON (reisen_bildanbieterzubild.bildanbieter_id_id = reisen_bildanbieter.bildanbieterID) WHERE reisen_reisebilder.reise_id_id = '" + pkquery + "' ORDER BY reisen_reisebilder.position;");
    bilder = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    #cursor.execute("SELECT katalog_pdf, anzahl_seiten_im_katalog, katalogseite, reisen_katalog.titel FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) WHERE reisen_reisekatalogzugehoerigkeit.reise_id_id = '" + str(pk) + "' ORDER BY position;");
    cursor.execute("SELECT anzahl_seiten_im_katalog, katalogseite, reisen_katalog.titel FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) WHERE reisen_reisekatalogzugehoerigkeit.reise_id_id = '" + pkquery + "' AND reisen_katalog.katalogID = '5fcadf9947314b82ac79802e92585c39'");
    katalog = namedtuplefetchall(cursor)
    cursor.close()


    return render(
      request,
      'reisen/reise_detail_export.xml',
      {
        'reise': reise,
        'termine': termine,
        'abfahrtszeiten': abfahrtszeiten,
        'leistungen': leistungen,
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
