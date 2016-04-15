# -*- coding: utf-8 -*-

import dateutil.parser as dup

from django.db.models import Min, F, Value as V
from django.db.models.functions import Concat
from django.db.models.expressions import RawSQL

from django_mysql.models import GroupConcat
from django_mysql.models.functions import ConcatWS
from .models import Reise, Reisetermine


def get_index_queryset_v1():
    """
    1. Versuch, gescheitert:
    - Annotation des kompletten gruppierten CONCAT-Dingsbums mit 'RawSQL'
    - Problem: Annotation wird vom Django autom. in GROUP BY gepackt und ergibt dann
        "ProgrammingError: (1111, 'Invalid use of group function')"
        (kaputte SQL-Anfrage siehe unten)
    :return: QuerySet
    """

    dt_str = "'%%d. %%m. %%Y'"
    reisetermine_rawsql = RawSQL(
        "GROUP_CONCAT(" +
            "DISTINCT CONCAT_WS(" +
                "' - ', DATE_FORMAT(%s, %s), DATE_FORMAT(%s, %s)) ORDER BY %s ASC SEPARATOR '\n')" %
        # DATE_FORMAT('datum_beginn', '%%d. %%m. %%Y') ...
        #
        ("`reisen_reisetermine`.`datum_beginn`", dt_str,
         "`reisen_reisetermine`.`datum_ende`", dt_str,
         "`reisen_reisetermine`.`datum_beginn`"), ())

    rqs = Reisetermine.objects.all()

    # Std.-sortierung aus Meta-Class (hier 'datum_beginn') aufheben, funkt sonst dazwischen
    #
    rqs = rqs.order_by()

    # erstmal nur Titel der Reise
    #
    vls = rqs.values('reise_id__titel', 'datum_beginn', 'datum_ende')

    # die Annotation zus. mit Min('datum...')
    #
    #vls = vls.annotate(rt=reisetermine_rawsql, min_dt=Min('datum_beginn'))
    #vls = vls.values('reise_id__titel', 'rt', 'min_dt')

    # ... ergibt den SQL-Fehler (siehe oben)
    #
    # >>> print vls.query
    # (siehe xyz.sql)
    # ...

    # ohne Fehler, aber falsch (ohne Min('datum...') und überhaupt:
    #
    vls = vls.annotate(rt=reisetermine_rawsql).values('reise_id__titel', 'rt')

    # kommt raus:
    #
    # {'rt': u'05. 03. 2016 - 08. 03. 2016 ... 10. 03. 2016 - 13. 03. 2016 ... 25. 03. 2016 - 28. 03. 2016 ... 31. 05. 2016 - 02. 06. 2016 ... 14. 06. 2016 - 18. 06. 2016 ... 25. 09. 2016 - 27. 09. 2016',
    #  'reise_id__titel': u'Kurztrip auf Helgoland'}

    # wg. SQL ohne GROUP BY (siehe xyz.sql):
    # ...

    # RawSQL-Bastel:
    #
    return None


def get_index_queryset_v2():
    """
    2. Versuch, schon besser:
    - DB-Funktionen aus django-mysql
        > http://django-mysql.readthedocs.org/en/latest/database_functions.html#django_mysql.models.functions.ConcatWS
        > http://django-mysql.readthedocs.org/en/latest/aggregates.html#django_mysql.models.GroupConcat
    - Problem: alle CONCATs liefern Text als Ergebnis; Datums-Info und damit Filtern / Sortieren / Rechnen mit
      Datumstypen is futschikato
    - UND: Alphanumerische sortierung nach Min('datum...') mit TEUTSCHEM Format fällt aus (wg. Tag zuerst)
    - Wörkeraunt: Datum in ISO formatieren & die Strings wieder in Datumstypen parsen via dateutil.parser
        > http://dateutil.readthedocs.org/en/latest/parser.html
    :return: QuerySet
    """

    # TEUTSCHLAND
    #
    dt_raw_beginn = RawSQL("DATE_FORMAT(`reisen_reisetermine`.`datum_beginn`, '%%d. %%m. %%Y')", ())
    dt_raw_ende = RawSQL("DATE_FORMAT(`reisen_reisetermine`.`datum_ende`, '%%d. %%m. %%Y')", ())

    rqs = Reise.objects.all()
    rqs = rqs.order_by('pk', 'reisetermine__datum_beginn')
    vls = rqs.values('titel', 'reisetermine__datum_beginn', 'reisetermine__datum_ende')
    vls = vls.annotate(termine=ConcatWS(dt_raw_beginn, dt_raw_ende, separator=' - '))
    vls = vls.values('titel', 'termine')

    # comes out:
    #
    # {'titel': u'Saisoner\xf6ffnungsfahrt', 'termine': u'10. 03. 2016 - 13. 03. 2016'}
    # {'titel': u'Kurztrip auf Helgoland', 'termine': u'31. 05. 2016 - 02. 06. 2016'}
    # {'titel': u'Kurztrip auf Helgoland', 'termine': u'25. 09. 2016 - 27. 09. 2016'}
    # {'titel': u'Ostern in Lissabon', 'termine': u'25. 03. 2016 - 28. 03. 2016'}
    # {'titel': u'REISE TEST', 'termine': u'05. 03. 2016 - 08. 03. 2016'}
    # {'titel': u'REISE TEST', 'termine': u'14. 06. 2016 - 18. 06. 2016'}

    vls = vls.annotate(alle_termine=GroupConcat('termine', ordering='asc'))
    vls = vls.values('titel', 'alle_termine')

    # comes out (nah dran):
    #
    # {'titel': u'Saisoner\xf6ffnungsfahrt', 'alle_termine': u'10. 03. 2016 - 13. 03. 2016'}
    # {'titel': u'Kurztrip auf Helgoland', 'alle_termine': u'25. 09. 2016 - 27. 09. 2016,31. 05. 2016 - 02. 06. 2016'}
    # {'titel': u'Ostern in Lissabon', 'alle_termine': u'25. 03. 2016 - 28. 03. 2016'}
    # {'titel': u'REISE TEST', 'alle_termine': u'05. 03. 2016 - 08. 03. 2016,14. 06. 2016 - 18. 06. 2016'}

    # Std. Trennzeichen ist ',', versuche tauschen gegen was anderes:
    #
    #vls = vls.annotate(alle_termine=GroupConcat('termine', ordering='asc', separator='\n'))
    #vls = vls.values('titel', 'alle_termine')

    # macht aua; 'ordering' und 'separator' zusammen ergeben
    #   "ProgrammingError: (1064, "You have an error in your SQL syntax;..."
    # geht nur eins von beiden - Sortierung is eh hin bei deutsch, also
    # hübschen Separator aussuchen, an dem man später den String gut splitten kann
    # (siehe unten, spricht aber auch nix gegen ',')
    # '\n' würde ich nicht nehmen, sondern alle, die untereinander sollen, in Liste hauen und
    # im Template die '<br/>' usw. entspr. setzen ...
    #
    # daher:
    #
    vls = [{'titel': d['titel'], 'alle_termine': d['alle_termine'].split(',')} for d in vls]

    # ...
    #
    # {'titel': u'Saisoner\xf6ffnungsfahrt', 'alle_termine': [u'10. 03. 2016 - 13. 03. 2016']}
    # {'titel': u'Kurztrip auf Helgoland', 'alle_termine': [u'31. 05. 2016 - 02. 06. 2016', u'25. 09. 2016 - 27. 09. 2016']}
    # {'titel': u'Ostern in Lissabon', 'alle_termine': [u'25. 03. 2016 - 28. 03. 2016']}
    # {'titel': u'REISE TEST', 'alle_termine': [u'14. 06. 2016 - 18. 06. 2016', u'05. 03. 2016 - 08. 03. 2016']}

    # ####################################################
    # un nu nochma mit ISO Datum und gängiger Sortierung
    #
    dt_raw_beginn = 'reisetermine__datum_beginn'
    dt_raw_ende = 'reisetermine__datum_ende'
    vls = rqs.values('titel', 'reisetermine__datum_beginn', 'reisetermine__datum_ende')
    vls = vls.annotate(termine=ConcatWS(dt_raw_beginn, dt_raw_ende, separator=':'))
    vls = vls.values('titel', 'termine')
    vls = vls.annotate(alle_termine=GroupConcat('termine', ordering='asc'))
    vls = vls.values('titel', 'alle_termine')

    # ...
    #
    # {'titel': u'Saisoner\xf6ffnungsfahrt', 'alle_termine': u'2016-03-10:2016-03-13'}
    # {'titel': u'Kurztrip auf Helgoland', 'alle_termine': u'2016-05-31:2016-06-02,2016-09-25:2016-09-27'}
    # {'titel': u'Ostern in Lissabon', 'alle_termine': u'2016-03-25:2016-03-28'}
    # {'titel': u'REISE TEST', 'alle_termine': u'2016-03-05:2016-03-08,2016-06-14:2016-06-18'}

    vls = [{'titel': d['titel'], 'alle_termine': d['alle_termine'].split(',')} for d in vls]
    res = []
    for d in vls:
        alle_termine = []
        for zeitraum in d['alle_termine']:
            # beginn:ende
            #
            neuer_zeitraum = zeitraum.split(':')
            # als Datumstupel
            #
            neuer_zeitraum = (dup.parse(neuer_zeitraum[0]), dup.parse(neuer_zeitraum[1]))
            alle_termine.append(neuer_zeitraum)
        res.append({
            'titel': d['titel'],
            'alle_termine': alle_termine
        })

    # das kann man im Template gut verwursten (und im Client dann auch filtern / sortieren usw.)
    #
    # {'titel': u'Saisoner\xf6ffnungsfahrt', 'alle_termine': [(datetime.datetime(2016, 3, 10, 0, 0), datetime.datetime(2016, 3, 13, 0, 0))]}
    # {'titel': u'Kurztrip auf Helgoland', 'alle_termine': [(datetime.datetime(2016, 5, 31, 0, 0), datetime.datetime(2016, 6, 2, 0, 0)),
    #                                                       (datetime.datetime(2016, 9, 25, 0, 0), datetime.datetime(2016, 9, 27, 0, 0))]}
    # {'titel': u'Ostern in Lissabon', 'alle_termine': [(datetime.datetime(2016, 3, 25, 0, 0), datetime.datetime(2016, 3, 28, 0, 0))]}
    # {'titel': u'REISE TEST', 'alle_termine': [(datetime.datetime(2016, 3, 5, 0, 0), datetime.datetime(2016, 3, 8, 0, 0)),
    #                                           (datetime.datetime(2016, 6, 14, 0, 0), datetime.datetime(2016, 6, 18, 0, 0))]}

    # ABER: ziemlich umständlich > go to ...v3()
    #
    return res


def get_index_queryset_v3():
    """
    3. Versuch, so würd' ich ihn bauen:
    - nix CONCAT, nix django-mysql (aber gut zu wissen, dass es das gibt), nix parsen, zack feddich
    :return:
    """

    rqs = Reisetermine.objects.all()
    # distinct IDs
    #
    reiseIDs = rqs.values_list('reise_id', flat=True).distinct()

    rqs = rqs.order_by('reise_id__titel', 'datum_beginn')
    vls = rqs.values('reise_id', 'reise_id__titel', 'datum_beginn', 'datum_ende')

    res = []
    i = 0
    for r in vls:
        at = (r['datum_beginn'], r['datum_ende'])
        if i > 0 and res[i-1]['reise_id'] == r['reise_id']:
            # hänge Datumstupel ('beginn', 'ende') an, immer wenn ID mätscht
            #
            res[i-1]['alle_termine'].append(at)
        else:
            # neuer Eintrag
            #
            res.append({
                'reise_id': r['reise_id'],
                'titel': r['reise_id__titel'],
                'alle_termine': [at]
            })
            i += 1

    # 'reiseIDs' sind echte UUID-Objekte, wir brauchen den Hex-String
    # ("in-place" wg. "by reference" mit dict-Objekten in Listen)
    #
    ignore = [d.update({'reise_id': d['reise_id'].hex}) for d in res]

    # ...
    #
    # {'alle_termine': [(datetime.date(2016, 3, 10), datetime.date(2016, 3, 13))], 'titel': u'Saisoner\xf6ffnungsfahrt'}
    # {'alle_termine': [(datetime.date(2016, 5, 31), datetime.date(2016, 6, 2)),
    #                   (datetime.date(2016, 9, 25), datetime.date(2016, 9, 27))], 'titel': u'Kurztrip auf Helgoland'}
    # {'alle_termine': [(datetime.date(2016, 3, 25), datetime.date(2016, 3, 28))], 'titel': u'Ostern in Lissabon'}
    # {'alle_termine': [(datetime.date(2016, 3, 5), datetime.date(2016, 3, 8)),
    #                   (datetime.date(2016, 6, 14), datetime.date(2016, 6, 18))], 'titel': u'REISE TEST'}
    return res


def get_detail_hinweise_queryset(pk):
    """
    Zwei Möglichkeiten:
        1.  nur den Hinweistext "transparent" durch das 'through'-Model (via 'Hinweis.__str()__')
        2.  zus. Attribute aus 'Reisehinweise' (='through') via '.reisehinweise_set...'
    :param pk:
    :return:
    """

    # 1.
    #
    # qs = Reise.objects.filter(pk=pk)
    # return qs.annotate(hinweis=F('hinweise__hinweis')).values('hinweis')

    # 2.
    #
    reise = Reise.objects.get(pk=pk)
    reise = reise.reisehinweise_set.annotate(hinweis=F('hinweis_id__hinweis'))
    return reise.values('position', 'titel', 'hinweis')


def get_detail_preise_queryset(pk):
    """
    Bleiben Fragen zur Formatierung ...
        - hier oder im Template
        - Bsp. 'Preis': ohne 'Concat' kommt 'Decimal'-Objekt zurück und wird im Template durch Magic mit ','
          gerändert
    :param pk:
    :return:
    """

    preise = Reise.objects.get(pk=pk)
    # nochma der Versuch mit 'django-mysql' ('GroupConcat')
    # ('ordering' und 'separator' zusammen gehen immer noch nicht ...)
    #
    preise = preise.reisepreise_set.annotate(zpreis=GroupConcat(Concat('reisepreiszusatz__position', V('__'),
                                                                       'reisepreiszusatz__preis_id__titel', V(': '),
                                                                       # 'EUR' hier oder im Template ?
                                                                       #
                                                                       'reisepreiszusatz__preis', V(' EUR')),
                                                                separator='||'),
                                                                # ordering='asc'),
                                             titel=F('preis_id__titel'))
    preise = preise.values('titel', 'preis', 'kommentar', 'zpreis')

    # Formatierungs-Gerödel von Nöten ... (wg. Sorteirung etc.)
    #
    for r in preise:
        # mache Liste (vgl. 'separator=...' oben)
        #
        r['zpreis'] = r['zpreis'].split('||')
        r['zpreis'].sort()
        r['zpreis'] = [p.split('__')[1] for p in r['zpreis']]

    return preise