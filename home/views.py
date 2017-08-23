# -*- coding: utf8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import AktuellesForm
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django import db
from django.db import connection
from collections import namedtuple, OrderedDict
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Min, F, Value as V
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Count
from .models import Aktuelles
from reisen.models import Reise, Reisetermine, Kategorie, Reisekategorien, Reisehinweise, Zielregion, Reisezielregionen, Abfahrtszeiten, LeistungenReise, Reisebeschreibung, Reisetage, Reisepreise, Preis, ReisepreisZusatz, Zusatzleistung, Fruehbucherrabatt, Reisebilder, Reisekatalogzugehoerigkeit, Katalog

def namedtuplefetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [ col[0] for col in desc ])
    return [ nt_result(*row) for row in cursor.fetchall() ]


def ajax(request):
    res = loader.get_template('home/ajax.html')
    kategorien = Kategorie.objects.values('kategorie')
    zielregionen = Zielregion.objects.values('name')
    countReiseziel = Reisezielregionen.objects.all().values('zielregion_id__name').annotate(total=Count('zielregion_id__name')).order_by('total')
    return render(request, 'home/ajax.html', {'kategorien': kategorien,'zielregionen': zielregionen,'countReiseziel': countReiseziel})


@csrf_exempt
def gibReisen(request):
    kategorien = Kategorie.objects.values_list('kategorie', flat=True)
    zielregionen = Zielregion.objects.values_list('name', flat=True)
    abdatum = request.POST.get(u'abdatum', '')
    labelText = request.POST.get(u'labelText', '')
    reiseziel = request.POST.getlist(u'reisezielregionen[]', list(zielregionen))
    reisekat = request.POST.getlist(u'reisekategorien[]', list(kategorien))
    for i, rk in enumerate(reisekat):
        reisekat[i] = rk.replace('&amp;', '&')

    if not abdatum:
        abdat = datetime.now()
    else:
        abdat = datetime.strptime(abdatum, '%d.%m.%Y').date()

    countReiseziel = Reisezielregionen.objects.filter(
        reise_id__reisetermine__datum_beginn__gte=abdat,
        reise_id__status='f',
        reise_id__reisetermine__datum_ende__isnull=False
      ).values('zielregion_id__name').annotate(total=Count('zielregion_id__name')).order_by('total')

    countReisekategorie = Reisekategorien.objects.filter(
        reise_id__reisetermine__datum_beginn__gte=abdat,
        reise_id__status='f',
        reise_id__reisetermine__datum_ende__isnull=False).values('kategorie_id__kategorie').annotate(total=Count('kategorie_id__kategorie')).order_by('total')

    reisen = Reise.objects.select_related().filter(
        reisetermine__datum_beginn__gte=abdat,
        status='f',
        reisetermine__datum_ende__isnull=False,
        reisepreise__preis_id__titel='Preis p.P.',
        reisepreise__markierung=F('reisetermine__markierung'),
        reisekategorien__kategorie_id__kategorie__in=reisekat,
        reisezielregionen__zielregion_id__name__in=reiseziel
      ).order_by(
        'reisetermine__datum_beginn',
        'reisepreise__preis'
      ).values(
        'reiseID',
        'titel',
        'reisetyp',
        'reisetermine__datum_beginn',
        'reisetermine__datum_ende',
        'reisepreise__preis',
        'reisepreise__preis_id__titel'
      ).distinct()

    data = {
       'successmsg': 'SUCCESS',
       'kategorien': list(kategorien),
       'reisekat': reisekat,
       'reiseziel': reiseziel,
       'countReiseziel': list(countReiseziel),
       'countReisekategorie': list(countReisekategorie),
       'reisen': list(reisen)
     }

    return JsonResponse(data)


def neustart(request):
    aktuelles = Aktuelles.objects.filter(published_date__lte=timezone.now()).order_by('start_date')
    return render(request, 'home/neustart.html', {'aktuelles': aktuelles})


def start(request):
    data = {'startinhalt': loader.get_template('home/startinhalt.html').render()
       }
    return JsonResponse(data)


def reisen(request):
    res = 'Alle Reisen, Unternavigation'
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT reiseID, RP.abpreis, reisen_reise.neu, reisen_reise.individualbuchbar, reisen_kategorie.kategorie, reisen_zielregion.name, reisen_reise.untertitel, korrektur_bemerkung_intern, einleitung, reisetyp, KT.katalogseiten, RT.reise_id_id, reisen_reise.titel, RT.min_datum, RT.reisetermine FROM reisen_reise LEFT JOIN (SELECT reise_id_id, MIN(datum_beginn) AS min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reisetermine FROM reisen_reisetermine GROUP BY reise_id_id ORDER BY min_datum) AS RT ON (RT.reise_id_id = reiseID) LEFT JOIN (SELECT reise_id_id, group_concat(DISTINCT CONCAT_WS(' auf der Seite ', reisen_katalog.titel, katalogseite) ORDER BY position ASC SEPARATOR ' und im Katalog ') AS katalogseiten FROM reisen_reisekatalogzugehoerigkeit LEFT JOIN reisen_katalog ON (reisen_katalog.katalogID = reisen_reisekatalogzugehoerigkeit.katalog_id_id) GROUP BY reise_id_id) as KT ON (KT.reise_id_id = reiseID) LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reisen_reisekatalogzugehoerigkeit.reise_id_id = reisen_reise.reiseID) left join reisen_reisekategorien on (reiseID = reisen_reisekategorien.reise_id_id) left join reisen_kategorie on (kategorieID = kategorie_id_id) left join reisen_reisezielregionen on (reiseID = reisen_reisezielregionen.reise_id_id) left join reisen_zielregion on (zielregionID = zielregion_id_id) left join (select reisen_reisepreise.reise_id_id, MIN(reisen_reisepreise.preis) AS abpreis from reisen_reisepreise GROUP BY reisen_reisepreise.reise_id_id) AS RP ON (reiseID = RP.reise_id_id) WHERE reisen_reisekatalogzugehoerigkeit.katalog_id_id = 'fa81408e2b69488498ace5b91737d187' ORDER BY RT.min_datum;")
    termine = namedtuplefetchall(cursor)
    cursor.close()
    kategorien = [
     u'Wanderreisen', u'kombinierte Flug- und Busreisen', u'Kuren, Gesundheits- und Wellnessreisen', u'Flusskreuzfahrten']
    zielregionen = [u'Deutschland', u'Benelux', u'Schweiz / \xd6sterreich / Tschechien / Slovakei / Ungarn', u'Frankreich / Italien / Andorra', u'Portugal', u'England / Schottland / Irland', u'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', u'Baltikum / Skandinavien / Finnland / Island', u'Polen']
    termine_distinct = OrderedDict()
    for termin in termine:
        termine_distinct[termin.reiseID] = termin

    return JsonResponse({'termine_distinct': termine_distinct.values(),'termine': termine,'kategorien': kategorien,'zielregionen': zielregionen})


@csrf_exempt
def tagesfahrten(request):

    termine = Reisetermine.objects.select_related().filter(
        datum_beginn__gte=datetime.now(),
        reise_id__status='f'
      ).filter(
        Q(reise_id__reisetyp='Tagesfahrt') | Q(reise_id__reisetyp='Musicalfahrt')
      ).order_by(
        'datum_beginn'
      ).values(
        'datum_beginn',
        'reise_id__reiseID',
        'reise_id__titel',
        'reise_id__untertitel',
        'reise_id__einleitung',
        'reise_id__veranstalter',
        'reise_id__sonstigeReisebeschreibung_titel'
      ).distinct()

    tagesfahrten = [
      {
        'monat': int(datetime.strftime(termin['datum_beginn'], '%-m')) - int(datetime.strftime(termine[i - 1]['datum_beginn'], '%-m')) if i > 0 else 1,
        'datum_beginn': termin['datum_beginn'],
        'titel': termin['reise_id__titel'],
        'untertitel': termin['reise_id__untertitel'],
        'einleitung': termin['reise_id__einleitung'],
        'veranstalter': termin['reise_id__veranstalter'] if termin['reise_id__veranstalter'] != 'RS' else '',
        'abfahrtszeiten': [ 
          {
            'ort': abfahrt.ort,
            'zeit': abfahrt.zeit
          } for abfahrt in Abfahrtszeiten.objects.filter(reise_id=termin['reise_id__reiseID']).order_by('position')
        ],
        'preise': [
          {
            'preistitel': str(preis.preis_id),
            'preis': preis.preis,
            'markierung': preis.markierung,
            'kommentar': preis.kommentar,
            'zpreise': [
              {
                'zpreistitel': str(zpreis.preis_id),
                'zpreis': zpreis.preis
              } for zpreis in ReisepreisZusatz.objects.filter(reisepreis_id=preis.reisepreisID)
            ]
          } for preis in Reisepreise.objects.filter(reise_id=termin['reise_id__reiseID'])
        ],
        'hinweise': [
          {
            'hinweis': str(hinweis.hinweis_id)
          } for hinweis in Reisehinweise.objects.filter(reise_id=termin['reise_id__reiseID'])
        ]
      } for i, termin in enumerate(termine)
    ]

    data = {
      u'successmsg': 'SUCCESS',
      u'typ': str(type(tagesfahrten)),
      u'tagesfahrten': tagesfahrten,
      u'termine': list(termine)
    }

    return JsonResponse(data)

def musicals(request):
    res = loader.get_template('home/musicals.html')
    return HttpResponse(res.render())


def zusatzangebote(request):
    res = 'Hier kommen die Zusatzangebote ...'
    return HttpResponse(res)


def reiseberatung(request):
    res = 'Fremdveranstalter, Flüge, Flusskreuzfahrten, Mietbus ....'
    return HttpResponse(res)


def service(request):
    res = 'Kontakt, Anfahrt, Gutscheine, Reisebedingung, Katalog anfordern, ...'
    return HttpResponse(res)


def kontakt(request):
    res = 'Hier kommt Kontakt und die Anfahrt ...'
    return HttpResponse(res)


def aktuelles(request):
    aktuelles = Aktuelles.objects.filter(published_date__lte=timezone.now()).order_by('start_date')
    return render(request, 'home/aktuelles.html', {'aktuelles': aktuelles})


def aktuell_detail(request, pk):
    aktuell = get_object_or_404(Aktuelles, pk=pk)
    return render(request, 'home/aktuell_detail.html', {'aktuell': aktuell})


@csrf_exempt
def reisedetails(request):
    reise = get_object_or_404(Reise, pk=request.GET.get('reiseID'))
    data = {u'successmsg': 'SUCCESS',
       u'typ': str(type(reise)),
       u'reisetitel': reise.titel,
       u'reiseuntertitel': reise.untertitel
       }
    return JsonResponse(data)


@login_required
def aktuell_neu(request):
    if request.method == 'POST':
        form = AktuellesForm(request.POST)
        if form.is_valid():
            aktuell = form.save(commit=False)
            aktuell.author = request.user
            aktuell.save()
            return redirect('home.views.aktuell_detail', pk=aktuell.pk)
    else:
        form = AktuellesForm()
    return render(request, 'home/aktuell_edit.html', {'form': form})


@login_required
def aktuell_edit(request, pk):
    aktuell = get_object_or_404(Aktuelles, pk=pk)
    if request.method == 'POST':
        form = AktuellesForm(request.POST, instance=aktuell)
        if form.is_valid():
            aktuell = form.save(commit=False)
            aktuell.author = request.user
            aktuell.published_date = timezone.now()
            aktuell.save()
            return redirect('home.views.aktuell_detail', pk=aktuell.pk)
    else:
        form = AktuellesForm(instance=aktuell)
    return render(request, 'home/aktuell_edit.html', {'form': form})


@login_required
def aktuell_draft_list(request):
    aktuelles = Aktuelles.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'home/aktuell_draft_list.html', {'aktuelles': aktuelles})


@login_required
def aktuell_publish(request, pk):
    aktuell = get_object_or_404(Aktuelles, pk=pk)
    aktuell.publish()
    return redirect('home.views.aktuell_detail', pk=pk)


@login_required
def aktuell_remove(request, pk):
    aktuell = get_object_or_404(Aktuelles, pk=pk)
    aktuell.delete()
    return redirect('home.views.aktuelles')
# okay decompiling /home/rss/public_html/rss2/home/views.pyc
