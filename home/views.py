#-*- coding: utf8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import AktuellesForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import Context, loader
from django import db
from django.db import connection
from collections import namedtuple, OrderedDict
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Min, F, Value as V
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Count
from .models import Aktuelles
from reisen.models import Reise, Reisetermine, Kategorie, Reisekategorien, Reisehinweise, Zielregion, Reisezielregionen, Ausflugspakete, Ausflugspaketpreise, AusflugspaketeZuReisetagen, LeistungenAusflugspaket, Abfahrtszeiten, LeistungenReise, Reisebeschreibung, Reisetage, Reisepreise, Preis, ReisepreisZusatz, Zusatzleistung, Fruehbucherrabatt, Reisebilder, Reisekatalogzugehoerigkeit, Katalog
from .forms import ContactForm, BuchungsanfrageForm
from reisen.querysets import get_detail_hinweise_queryset, get_detail_angebote_queryset, get_detail_auftragsbestaetigungen_queryset


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

def index(request):
    #res = loader.get_template('home/index.html')
    aktuelles = Aktuelles.objects.filter(end_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'home/index.html', {'aktuelles': aktuelles})

def hol_markierung_ajax(request):
    data = {}
    if request.method == "POST":
        datum_markierung = request.POST['datum_markierung']
        datum_mark = request.POST['datum_markierung']
        pk = request.POST['reiseID']
        individualreise = request.POST['individualreise']

        cursor = connection.cursor()
        cursor.execute("SELECT reise_id_id, reisepreisID, hauptpreis.titel, REPLACE(FORMAT(reisen_reisepreise.preis, 0),',','.') as preis, reisen_reisepreise.markierung, kommentar, subpreise.zpreis FROM reisen_reisepreise LEFT JOIN reisen_preis AS hauptpreis ON (hauptpreis.preisID = reisen_reisepreise.preis_id_id) LEFT JOIN (SELECT reisepreis_id_id, GROUP_CONCAT(IF(reisen_reisepreiszusatz.preis > 0, CONCAT(CONCAT_WS(': ', subpreis.titel, replace(FORMAT(reisen_reisepreiszusatz.preis, 0),',','.')), ' €'), subpreis.titel) ORDER BY reisen_reisepreiszusatz.position ASC SEPARATOR '\n') as zpreis from reisen_reisepreiszusatz LEFT JOIN reisen_preis AS subpreis ON (subpreis.preisID = reisen_reisepreiszusatz.preis_id_id) GROUP BY reisepreis_id_id) AS subpreise ON (reisepreisID = reisepreis_id_id) WHERE reisen_reisepreise.reise_id_id = '" + str(pk) + "' ORDER BY reisen_reisepreise.position;");
        preise = namedtuplefetchall(cursor)
        cursor.close()

        try:
            for p in preise:
                if individualreise == 'true':
                    if p.markierung == datum_mark and p.titel == 'Individualpreis p.P.':
                        preis = p
                else:
                    if p.markierung == datum_mark and p.titel != 'Individualpreis p.P.':
                        preis = p
        except Exception:
            preis = 'error'

        '''try:
            data = {
	        'datum_markierung': datum_markierung,
                'success_message': 'success'
	    }
        except Exception:
            data = {
                'error_message': 'error'
            }
            return JsonResponse(data)'''
        #return JsonResponse(list(data), safe = False) 
        return JsonResponse(list(preis), safe = False) 

@csrf_exempt
def gibReisen(request):
    debug = []
    kategorien = Kategorie.objects.values_list('kategorie', flat=True)
    zielregionen = Zielregion.objects.values_list('name', flat=True)
    abdatum = request.POST.get(u'abdatum', '')
    labelText = request.POST.get(u'labelText', '')
    reiseziel = request.POST.getlist(u'reisezielregionen[]', list(zielregionen))
    reisekat = request.POST.getlist(u'reisekategorien[]', list(kategorien))
    reisezielStatisch = [
        u'Deutschland',
        u'Österreich / Schweiz',
        u'Belgien / Holland',
        u'Frankreich',
        u'Italien', 
        u'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 
        u'Tschechien / Slovakei / Ungarn / Rumänien', 
        u'Polen', 
        u'Baltikum / Skandinavien / Finnland', 
        u'England / Schottland / Irland', 
        u'webDeutschland',
        u'webÖsterreich / Schweiz',
        u'webBelgien / Holland',
        u'webFrankreich',
        u'webItalien', 
        u'webSlowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 
        u'webTschechien / Slovakei / Ungarn / Rumänien', 
        u'webPolen', 
        u'webBaltikum / Skandinavien / Finnland', 
        u'webEngland / Schottland / Irland' 
    ]

    for i, rk in enumerate(reisekat):
        reisekat[i] = rk.replace('&amp;', '&')

    andereZiele = list(zielregionen)

    if 'andere Ziele' in reiseziel:
        for rzs in reisezielStatisch:
            if rzs not in reiseziel and rzs in andereZiele:
                andereZiele.remove(rzs)
        reiseziel = andereZiele
    else:        
        for i, rz in enumerate(reiseziel):
            debug.append('web'+rz)
        reiseziel.extend(debug)

    if not abdatum:
        abdat = datetime.now()
    else:
        abdat = datetime.strptime(abdatum, '%d.%m.%Y').date()

    countReiseziel = Reisezielregionen.objects.filter(
        reise_id__reisetermine__datum_beginn__gte=abdat,
        reise_id__status='f',
        reise_id__reisetermine__datum_ende__isnull=False
      ).values(
        'zielregion_id__name'
      ).annotate(
        total=Count('zielregion_id__name')
      ).order_by(
        'total'
      )

    countReisekategorie = Reisekategorien.objects.filter(
        reise_id__reisetermine__datum_beginn__gte=abdat,
        reise_id__status='f',
        reise_id__reisetermine__datum_ende__isnull=False
      ).values(
        'kategorie_id__kategorie'
      ).annotate(
        total=Count('kategorie_id__kategorie')
      ).order_by(
        'total'
      )

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
       'debug': debug,
       'kategorien': list(kategorien),
       'reisekat': reisekat,
       'reiseziel': reiseziel,
       'andereZiele': andereZiele,
       'countReiseziel': list(countReiseziel),
       'countReisekategorie': list(countReisekategorie),
       'reisen': list(reisen)
     }

    return JsonResponse(data)


def neustart(request):

    aktuelles = Aktuelles.objects.filter(published_date__lte=timezone.now()).order_by('start_date')

    reisen = Reise.objects.select_related().filter(
        reisetermine__datum_beginn__gte=timezone.now(),
        status='f',
        reisetermine__datum_ende__isnull=False,
        reisepreise__preis_id__titel='Preis p.P.',
        reisepreise__markierung=F('reisetermine__markierung'),
        #reisekategorien__kategorie_id__kategorie__in=reisekat,
        #reisezielregionen__zielregion_id__name__in=reiseziel
        reisezielregionen__position=0
      ).order_by(
        'reisetermine__datum_beginn',
        'reisetermine__datum_ende',
        'reisepreise__preis'
      ).values(
        'reiseID',
        'titel',
        'einleitung',
        'reisetyp',
        'reisetermine__datum_beginn',
        'reisetermine__datum_ende',
        'reisetermine__markierung',
        'reisepreise__preis',
        'reisepreise__preis_id__titel',
        'reisezielregionen__zielregion_id__name'
      ).distinct()[:5]

    version = request.GET.get('version')
    if version == 'ich':
      return render(request, 'home/neustartneu.html', {'aktuelles': aktuelles})
    elif version == 'nicepage':
      #return render(request, 'home/_start.html', {'aktuelles': aktuelles})
      return render(request, 'home/_start.html', {'reisen': reisen})
    else:
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


def mehrtagesfahrten(request):

    mehrtagesfahrten = Reise.objects.select_related().filter(
        reisetermine__datum_beginn__gte=timezone.now(),
        status='f',
        reisetermine__datum_ende__isnull=False,
        reisepreise__preis_id__titel='Preis p.P.',
        reisepreise__markierung=F('reisetermine__markierung'),
        #reisekategorien__kategorie_id__kategorie__in=reisekat,
        #reisezielregionen__zielregion_id__name__in=reiseziel
        reisezielregionen__position=0
      ).order_by(
        'reisetermine__datum_beginn',
        'reisetermine__datum_ende',
        'reisepreise__preis'
      ).values(
        'reiseID',
        'titel',
        'sonstigeReisebeschreibung_titel',
        'einleitung',
        'reisetyp',
        'reisetermine__datum_beginn',
        'reisetermine__datum_ende',
        'reisetermine__markierung',
        'reisepreise__preis',
        'reisepreise__preis_id__titel',
        'reisezielregionen__zielregion_id__name'
      ).distinct()

    return render(request, 'home/_mehrtagesfahrten.html', {'mehrtagesfahrten': mehrtagesfahrten })

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
        'markierung',
        'kommentar',
        'reise_id__reiseID',
        'reise_id__titel',
        'reise_id__untertitel',
        'reise_id__einleitung',
        'reise_id__veranstalter',
        'reise_id__sonstigeReisebeschreibung_titel'
      ).distinct()

    tagesfahrten = [
      {
        'reiseID': termin['reise_id__reiseID'],
        'monat': int(datetime.strftime(termin['datum_beginn'], '%-m')) - int(datetime.strftime(termine[i - 1]['datum_beginn'], '%-m')) if i > 0 else 1,
        'datum_beginn': termin['datum_beginn'],
        "datum_kommentar": termin['kommentar'],
        "datum_markierung": termin['markierung'],
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

    if request.method == 'POST':
      form = BuchungsanfrageForm(request.POST)
      if form.is_valid():
        #form.save()
        subject = "[RSS Buchungsanfrage per Webseite] " + form.cleaned_data['datum'] + ", " + form.cleaned_data['reise']  
        body = {
          'Nachricht': 'Nachricht: ' + form.cleaned_data['nachricht'],
          'Name': 'Name: ' + form.cleaned_data['name'],
          'Telefon': 'Telefon: ' + form.cleaned_data['telefon']
        }
        message = "\n".join(body.values())
        try:
          #send_mail(subject, message, form.cleaned_data['email'], ['info@heebeegeebees.de'])
          return HttpResponse('Invalid header found.')
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
        #return redirect ("home:tagesfahrten")
        #return HttpResponseRedirect('tagesfahrten')

    form = BuchungsanfrageForm()

    #return JsonResponse(data)
    return render(request, 'home/_tagesfahrten.html', {'tagesfahrten': tagesfahrten, 'form': form })

def musicals(request):
    res = loader.get_template('home/musicals.html')
    return HttpResponse(res.render())


def zusatzangebote(request):
    res = 'Hier kommen die Zusatzangebote ...'
    return HttpResponse(res)


def reiseberatung(request):
    res = 'Pauschalreisen, Mietwagen, Flüge, Kreuzfahrten, ...'
    #return HttpResponse(res)
    return render(request, 'home/_reiseberatung.html', {'res': res})


def service(request):
    res = 'Kontakt, Anfahrt, Gutscheine, Reisebedingung, Katalog anfordern, ...'
    return HttpResponse(res)


def kontakt(request):
    #res = 'Hier kommt Kontakt und die Anfahrt ...'
    #kontakt = 'Hier kommt Kontakt und die Anfahrt ...'
    #return HttpResponse(res)

#    if request.method == 'POST':
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return render(request, 'home/_start.html')
#    form = ContactForm(
#	initial = {
#   		'anrede': 'FR'
#	}
#    )
#
#    return render(request, 'home/_kontakt.html', {'form': form})

    if request.method == 'POST':
      form = BuchungsanfrageForm(request.POST)
      if form.is_valid():
        subject = "Buchungsanfrage per Webseite"
        body = {
          'Name': form.cleaned_data['name'], 
          'Email': form.cleaned_data['email'], 
          'Nachricht':form.cleaned_data['nachricht'], 
        }
        message = "\n".join(body.values())
        try:
          #send_mail(subject, message, 'info@heebeegeebees.de', ['info@heebeegeebees.de']) 
          return HttpResponse('Invalid header found.')
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
      return redirect ("home:tagesfahrten")
      
    form = ContactForm()
    return render(request, "home/_tagesfahrten.html", {'form':form})

def aktuelles(request):
    aktuelles1 = 'Hier kommt Kontakt und die Anfahrt ...'
    #aktuelles = Aktuelles.objects.filter(published_date__lte=timezone.now()).order_by('start_date')
    return render(request, 'home/aktuelles.html', {'aktuelles': aktuelles1})

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

##################################################################
# Detail Seite, Reisedetails                                     #
##################################################################
def detail(request, pk):

    dibug = request.method

#    if request.method == 'POST':
#        form = ContactForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return render(request, 'home/_start.html')
#    form = ContactForm(
#        initial = {
#                'anrede': 'FR'
#        }
#    )

    datum_markierung = request.GET.get('dm')
    datum_ende = request.GET.get('datum')

    qs = Reisetermine.objects.filter(reise_id=pk).order_by('datum_beginn')
    reise = get_object_or_404(Reise, pk=pk)
    termine = Reisetermine.objects.filter(
      reise_id=pk,
      datum_beginn__gte=timezone.now()
    ).order_by('datum_beginn')
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

    #dibug = ''#request.GET.get('version')
    version = request.GET.get('version')
    kategorie_aktuell = request.GET.get('kategorie')

    if request.method == 'POST':
      form = BuchungsanfrageForm(request.POST)
      if form.is_valid():
        #form.save()
        subject = "[RSS Buchungsanfrage per Webseite] " + form.cleaned_data['datum'] + ", " + form.cleaned_data['reise']
        body = {
          'Nachricht': 'Nachricht: ' + form.cleaned_data['nachricht'],
          'Name': 'Name: ' + form.cleaned_data['name'],
          'Telefon': 'Telefon: ' + form.cleaned_data['telefon']
        }
        message = "\n".join(body.values())
        try:
          #send_mail(subject, message, form.cleaned_data['email'], ['info@heebeegeebees.de'])
          return HttpResponse('Invalid header found.')
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
        #return redirect ("home:tagesfahrten")
        #return HttpResponseRedirect('tagesfahrten')

    form = BuchungsanfrageForm()

    return render(
      request,
      'home/_reise.html',
      {
        'datum_markierung': datum_markierung,
        'datum_ende': datum_ende,
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
        'form': form,
      }
    )
