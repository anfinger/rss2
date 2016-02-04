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

    #termine = Reisetermine.objects.select_related('reise_id').all().order_by('reise_id__titel')
    #Usage: MyModel.objects.all().annotate(new_attribute=Concat('related__attribute', separator=':')
    #termine = Reisetermine.objects.select_related('reise_id').all().annotate(reisebeginn=Concat('datum_beginn', separator='\n'))
    #termine = Reisetermine.objects.select_related('reise_id').filter('reise_id').values('reise_id').annotate(reisetermine = Concat('datum_beginn', separator='\n' )).order_by('reise_id__titel')
    #termine = Reisetermine.objects.select_related('reise_id').extra(select={'titel':'titel',}).annotate(reisetermine = Concat('datum_beginn', separator='\n' )).order_by('reise_id__titel')
    #dibug = termine.query

    cursor = connection.cursor()
    cursor.execute("SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d.'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine, reiseID, titel, untertitel, einleitung, reisetyp, katalogseite  FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) GROUP BY reise_id_id ORDER BY datum_beginn;");
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
    querystring = "SELECT reisen_reisepreise.reisepreisID, reisen_reisepreise.reise_id_id, reisen_reisepreise.preis_id_id as rppid, reisen_reisepreise.preis as preis, reisen_reisepreise.position, reisen_reisepreiszusatz.preis_id_id as rpzpid, reisen_reisepreiszusatz.reisepreis_id_id, group_concat(CONCAT_WS(': ', subpreis.titel, Concat(replace(reisen_reisepreiszusatz.preis, '.', ','), ' €')) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis, hauptpreis.preisID, hauptpreis.titel FROM reisen_reisepreise LEFT JOIN reisen_reisepreiszusatz ON (reisen_reisepreise.reisepreisID = reisen_reisepreiszusatz.reisepreis_id_id) LEFT JOIN reisen_preis as hauptpreis ON (reisen_reisepreise.preis_id_id = hauptpreis.preisID) LEFT JOIN reisen_preis as subpreis ON (reisen_reisepreiszusatz.preis_id_id = subpreis.preisID)  WHERE reisen_reisepreise.reise_id_id ='" + str(pk) + "' GROUP BY reisen_reisepreiszusatz.reisepreis_id_id ORDER BY reisen_reisepreise.position;"
    cursor.execute("SELECT reisen_reisepreise.kommentar, reisen_reisepreise.reisepreisID, reisen_reisepreise.reise_id_id, reisen_reisepreise.preis_id_id as rppid, reisen_reisepreise.preis as preis, reisen_reisepreise.position, reisen_reisepreiszusatz.preis_id_id as rpzpid, reisen_reisepreiszusatz.reisepreis_id_id, group_concat(CONCAT_WS(': ', subpreis.titel, Concat(replace(reisen_reisepreiszusatz.preis, '.', ','), ' €')) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis, hauptpreis.preisID, hauptpreis.titel FROM reisen_reisepreise LEFT JOIN reisen_reisepreiszusatz ON (reisen_reisepreise.reisepreisID = reisen_reisepreiszusatz.reisepreis_id_id) LEFT JOIN reisen_preis as hauptpreis ON (reisen_reisepreise.preis_id_id = hauptpreis.preisID) LEFT JOIN reisen_preis as subpreis ON (reisen_reisepreiszusatz.preis_id_id = subpreis.preisID)  WHERE reisen_reisepreise.reise_id_id ='" + str(pk) + "' GROUP BY reisen_reisepreiszusatz.reisepreis_id_id ORDER BY reisen_reisepreise.position;");
    #cursor.execute(querystring)
    preise = namedtuplefetchall(cursor)
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("SELECT reisen_ausflugspakete.ausflugspaketID, reisen_ausflugspaketezureisetagen.ausflugspaket_text, reisen_ausflugspaketezureisetagen.reisetag_id_id, reisen_ausflugspakete.titel as aptitel, reisen_ausflugspaketezureisetagen.erscheint_in, reisen_ausflugspakete.kommentar_titel, reisen_ausflugspakete.kommentar, reisen_ausflugspakete.position, group_concat(reisen_leistungenausflugspaket.leistung ORDER BY reisen_leistungenausflugspaket.position ASC SEPARATOR '\n') as leistung, reisen_preis.titel as ptitel, reisen_reisetage.tagnummer, reisen_reisetage.titel as rtitel, reisen_ausflugspaketpreise.preis FROM reisen_ausflugspakete LEFT JOIN reisen_leistungenausflugspaket ON (reisen_ausflugspakete.ausflugspaketID = reisen_leistungenausflugspaket.ausflugspaket_id_id) LEFT JOIN reisen_ausflugspaketpreise ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketpreise.ausflugspaket_id_id) LEFT JOIN reisen_preis ON (reisen_preis.preisID = reisen_ausflugspaketpreise.preis_id_id) LEFT JOIN reisen_ausflugspaketezureisetagen ON (reisen_ausflugspakete.ausflugspaketID = reisen_ausflugspaketezureisetagen.ausflugspaket_id_id) LEFT JOIN reisen_reisetage ON (reisen_reisetage.reisetagID = reisen_ausflugspaketezureisetagen.reisetag_id_id) WHERE reisen_ausflugspakete.reise_id_id = '" + str(pk) + "' GROUP BY reisen_ausflugspaketezureisetagen.ausflugspakete_zu_reisetagenID ORDER BY reisen_ausflugspakete.reise_id_id, reisen_ausflugspakete.position;");
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

    dibug = querystring
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
