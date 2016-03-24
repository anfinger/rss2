# -*- coding: utf8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import ReiseForm
from uuid import UUID
from django.utils import timezone
from django import db
from collections import namedtuple
from django.db import connection
from itertools import chain
from django.core import serializers


# Create your views here.

from .models import Reise, Reisetermine, LeistungenReise, Reisetage, Reisepreise, Preis, ReisepreisZusatz, Zusatzleistung, Fruehbucherrabatt, Reisebilder

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

##################################################################
# Index Seite, Reisen Übersicht                                  #
##################################################################
def index(request):
    dibug = ''

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine, reiseID, titel, untertitel, einleitung, reisetyp, katalogseite  FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) GROUP BY reise_id_id ORDER BY min_datum;");
    termine = namedtuplefetchall(cursor)
    cursor.close()
    dibug = termine
    #if termine.exists():
    #    for termin in termine:
    #        termin

    return render(request, 'reisen/index.html', {'termine': termine, 'dibug': dibug})

##################################################################
# Detail Seite, Reisedetails                                     #
##################################################################
def reise_detail(request, pk):

    #data = serializers.serialize("xml", Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn'))

    qs = Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn')

    #XMLSerializer = serializers.get_serializer("xml")
    #xml_serializer = XMLSerializer()
    #xml_serializer.serialize(qs)
    #data = xml_serializer.getvalue()

    #with open("./file.xml", "w") as out:
    #    xml_serializer.serialize(qs, stream=out)

    dibug = 'NIX PASSIERT'
    reise = get_object_or_404(Reise, pk=pk)
    termine = Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn')
    leistungen = LeistungenReise.objects.filter(reise_id=pk).order_by('position')
    zusatzleistungen = Zusatzleistung.objects.filter(reise_id=pk).order_by('position')
    fruehbucherrabatte = Fruehbucherrabatt.objects.filter(reise_id=pk).order_by('datum_bis')
    tage = Reisetage.objects.filter(reise_id=pk).order_by('tagnummer')
    for tag in tage:
        tag.reisetagID = str(tag.reisetagID).replace('-','')
    #preise = Reisepreise.objects.filter(reise_id=pk).order_by('position')
    #preistitel = Preis.objects.filter(reise_id=pk).order_by('position')
    #preiszusatz = ReisepreisZusatz

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, reisepreisID, hauptpreis.titel, reisen_reisepreise.preis, kommentar, subpreise.zpreis FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) INNER JOIN (SELECT reisepreis_id_id, GROUP_CONCAT(CONCAT(CONCAT_WS(': ', subpreis.titel, replace(reisen_reisepreiszusatz.preis, '.', ',')), ' EUR') ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis from reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisepreis_id_id) AS subpreise ON (reisepreisID = reisepreis_id_id) WHERE	reisen_reisepreise.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisepreise.position;");
    preise = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT ausflugspaketID, ausflugspaket_text, reisetag_id_id, reisen_ausflugspakete.titel AS aptitel, erscheint_in, kommentar_titel, kommentar, reisen_ausflugspakete.position, reisen_preis.titel as ptitel, tagnummer, reisen_reisetage.titel as rtitel, preis, apleistungen.leistungen FROM reisen_ausflugspakete LEFT JOIN (SELECT ausflugspaket_id_id, group_concat(leistung ORDER BY position ASC SEPARATOR '\n') AS leistungen FROM reisen_leistungenausflugspaket group by ausflugspaket_id_id) AS apleistungen ON (reisen_ausflugspakete.ausflugspaketID = apleistungen.ausflugspaket_id_id) LEFT JOIN reisen_ausflugspaketpreise ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketpreise.ausflugspaket_id_id) LEFT JOIN reisen_preis ON (reisen_preis.preisID = reisen_ausflugspaketpreise.preis_id_id) LEFT JOIN reisen_ausflugspaketezureisetagen ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketezureisetagen.ausflugspaket_id_id) LEFT JOIN reisen_reisetage ON (reisen_reisetage.reisetagID = reisen_ausflugspaketezureisetagen.reisetag_id_id) WHERE reisen_ausflugspakete.reise_id_id = '" + str(pk) + "';");
    aps = namedtuplefetchall(cursor)
    cursor.close()

    aps_distinct = {}
    for ap in aps:
        aps_distinct[ap.ausflugspaketID] = ap

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

    dibug = '' #querystring
    return render(
        request,
        'reisen/reise_detail.html',
        {
            'reise': reise,
            'termine': termine,
            'leistungen': leistungen,
            'tage': tage,
            'preise': preise,
            'aps': aps,
            'aps_distinct': aps_distinct.values(),
            'hinweise': hinweise,
            'kategorien': kategorien,
            'zielregionen': zielregionen,
            'zusatzleistungen': zusatzleistungen,
            'fruehbucherrabatte': fruehbucherrabatte,
            'bilder': bilder,
            'dibug': dibug
        })
