# -*- coding: utf8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.humanize.templatetags.humanize import intcomma
from collections import OrderedDict 
import re
import datetime
#import locale

register = template.Library()

@register.assignment_tag
def reise_kategorie_alt(kategorie, termine):
    gefilterte_reisen = [termin for termin in termine if termin.kategorie == kategorie]
    return gefilterte_reisen if gefilterte_reisen else None

@register.assignment_tag
def reise_kategorie(kategorie, termine):
    gefilterte_reisen = OrderedDict()
    for termin in termine:
      if termin.kategorie == kategorie:
        gefilterte_reisen[termin.reiseID] = termin
    return gefilterte_reisen.values() if gefilterte_reisen.values() else None

@register.assignment_tag
def reise_zielregion(zielregion, termine):
    gefilterte_reisen = OrderedDict()
    for termin in termine:
      if termin.name == zielregion:
        gefilterte_reisen[termin.reiseID] = termin
    return gefilterte_reisen.values() if gefilterte_reisen.values() else None

@register.assignment_tag
def reise_webZielregion(zielregion, termine):
    gefilterte_reisen = OrderedDict()
    for termin in termine:
      webZielregion = termin.name
      if webZielregion[:3]  == 'web':
        webZielregion = webZielregion[3:]

      """
      if "webItalien" in termin.name:
        webZielregion = re.sub(r'webItalien', 'Italien', termin.name)
      if "webFrankreich / Spanien / Portugal" in termin.name:
        webZielregion = re.sub(r'webFrankreich / Spanien / Portugal', 'Frankreich / Spanien / Portugal', termin.name)
      #if "webOesterreich / Schweiz" in termin.name:
      #  webZielregion = re.sub(r'webOesterreich / Schweiz', 'Österreich / Schweiz', termin.name)
      if u"webOesterreich" in termin.name:
        webZielregion = re.sub(r'webOesterreich', u'Österreich / Schweiz', termin.name)
      if u"webSlovakei" in termin.name:
        webZielregion = re.sub(r'webSlovakei', u'Schweiz / Österreich / Tschechien / Slovakei / Ungarn', termin.name)
      if u"webSkandinavien" in termin.name:
        webZielregion = re.sub(r'webSkandinavien', u'Skandinavien / Baltikum / Finnland', termin.name)
      if u"webDeutschland" in termin.name:
        webZielregion = re.sub(r'webDeutschland', u'Deutschland', termin.name)
      if u"webBenelux" in termin.name:
        webZielregion = re.sub(r'webBenelux', u'Benelux', termin.name)
      if u"webOsteuropa" in termin.name:
        webZielregion = re.sub(r'webOsteuropa', u'Osteuropa', termin.name)
      if u"webBritische Inseln" in termin.name:
        webZielregion = re.sub(r'webBritische Inseln', u'Britische Inseln', termin.name)
      """

      if webZielregion == zielregion:
        gefilterte_reisen[termin.reiseID] = termin
    return gefilterte_reisen.values() if gefilterte_reisen.values() else None

@register.assignment_tag
def bilder_web(keyword, bilder):
    gefilterte_bilder = [bild for bild in bilder if keyword in bild.zu_verwenden_in]
    return gefilterte_bilder if gefilterte_bilder else None

@register.filter
def preisformat(preis):
    if preis:
        if ((preis-int(preis))>0):
          return preis
        else:
          return intcomma(int(preis))
          #locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')
          #locale.format('%d', preis, 1)
          #return "{:,}".format(preis)
    else:
        return ''

@register.filter
@stringfilter
def bildweb(bild):
    if bild:
      return re.sub(r'images/', 'images/web_', str(bild))
    else:
      return ''

@register.filter
@stringfilter
def bildwebfixedheight(bild):
    if bild:
      return re.sub(r'images/', 'images/wx200/web_fixed_height_', str(bild))
    else:
      return ''

@register.filter
@stringfilter
def terminekomma(termine):
    if termine:
      return re.sub(r'\n', ', ', str(termine))
    else:
      return ''

@register.filter
@stringfilter
def kategorie_get(kategorie):
    if kategorie:
      return re.sub(r'&', 'und', kategorie)
    else:
      return ''

@register.filter
@stringfilter
def ohneminus(uuid):
    if uuid:
      return re.sub(r'-', '', str(uuid))
    else:
      return ''

@register.filter
@stringfilter
def zielumbenennen(zielregion):
    if zielregion:
      zielregion = re.sub(r'Benelux', u'Belgien / Holland', zielregion)
      zielregion = re.sub(r'Schweiz .*', u'Österreich / Schweiz / Slovakei / Tschechien / Ungarn / Rumänien', zielregion)
      zielregion = re.sub(r'Frankreich / Italien / Andorra', 'Frankreich / Italien',  zielregion)
      zielregion = re.sub(r'Baltikum / Skandinavien / Finnland / Island', 'Baltikum / Skandinavien / Finnland',  zielregion)
      #zielregion = re.sub(r'Wanderreisen', u'Rad- und Wanderreisen', zielregion)
      # zielregion = re.sub(r'Slowenien / Kroatien / Montenegro / Bosnien und Herzegowina', 'Bosnien und Herzegowina / Kroatien / Montenegro / Slowenien',  zielregion)
      return zielregion
    else:
      return ''

@register.filter
@stringfilter
def sternweg(leistung):
    if str(leistung)[0] == '*':
      #leistung = re.sub(r'\*', u'', leistung)
      str(leistung)[0] = ''
      return leistung
      #return leistung[1:]
    else:
      return ''

@register.filter
@stringfilter
def abfahrtsorte(ort):
    if ort:
      ort = re.sub(r'HBF', u'Hbf Schwerin', ort)
      ort = re.sub(r'VSB', u'HAST v. Stauffenberg Str.', ort)
      ort = re.sub(r'GAR', u'Gartenstadt', ort)
      ort = re.sub(r'WIS', u'ZOB Wismar', ort)
      ort = re.sub(r'ROG', u'Gadebusch Roggendorfer Str.', ort)
      ort = re.sub(r'ANK', u'Ankunft', ort)
      return ort
    else:
      return ''

@register.simple_tag
def dauer(ende, beginn):
    if ende:
      tage = ende - beginn
      return tage.days + 1
    else:
      return 1

@register.filter
@stringfilter
def nurbetrag(zpreis):
    if zpreis:
      zpreis = re.sub(r'EZ-Zuschlag: ', u'', zpreis)
      zpreis = re.sub(r'EZ-Zuschlag', u'0 €', zpreis)
      zpreis = re.sub(r'\n', u'</td><td>', zpreis)
      zpreis = re.sub(r'Zuschlag gr. DZ: ', u'', zpreis)
      zpreis = re.sub(r'VP-Zuschlag: ', u'', zpreis)
      zpreis = re.sub(r'VP-Zuschlag', u'0 €', zpreis)
      return zpreis
    else:
      return ''

@register.filter
@stringfilter
def ohnetage(reisetyp):
    if 'Flug- & Busreise' in reisetyp:
      return 'FLUGREISE'
    elif 'Busreise' in reisetyp:
      return 'BUSREISE'
    elif 'Flugreise' in reisetyp:
      return 'FLUGREISE'
    elif 'anderreise' in reisetyp:
      return 'WANDERREISE'
    elif 'Kurreise' in reisetyp:
      return 'KURREISE'
    elif 'Schiffsreise' in reisetyp:
      return 'SCHIFFSREISE'
    elif 'Fluss' in reisetyp:
      return 'SCHIFFSREISE'
    else:
      return ''

@register.filter
@stringfilter
def ohnetageklein(reisetyp):
    if 'Flug- & Busreise' in reisetyp:
      return 'Flugreise'
    elif 'Busreise' in reisetyp:
      return 'Busreise'
    elif 'Flugreise' in reisetyp:
      return 'Flugreise'
    elif 'anderreise' in reisetyp:
      return 'Wanderreise'
    elif 'Kurreise' in reisetyp:
      return 'Kurreise'
    elif 'Schiffsreise' in reisetyp:
      return 'Schiffsreise'
    elif 'Fluss' in reisetyp:
      return 'Schiffsreise'
    else:
      return ''

@register.filter
@stringfilter
def mittageklein(reisetyp):
    if 'Flug- & Busreise' in reisetyp:
      return re.sub(r'Flug- & Busreise', u'Flugreise', reisetyp)
    elif 'Busreise' in reisetyp:
      return reisetyp
    elif 'Flugreise' in reisetyp:
      return reisetyp
    elif 'Bus- & Radwanderreise' in reisetyp:
      return re.sub(r'Bus- & Radwanderreise', u'Radwanderreise', reisetyp)
    if 'Bus- & Wanderreise' in reisetyp:
      return re.sub(r'Bus- & Wanderreise', u'Wanderreise', reisetyp)
    elif 'Wanderreise' in reisetyp:
      return reisetyp
    elif 'Kurreise' in reisetyp:
      return reisetyp
    if 'Bus- & Schiffsreise' in reisetyp:
      return re.sub(r'Bus- & Schiffsreise', u'Schiffsreise', reisetyp)
    elif 'Schiffsreise' in reisetyp:
      return reisetyp
    elif 'Fluss' in reisetyp:
      return reisetyp
    else:
      return ''


@register.filter
@stringfilter
def reisetypfarbe(reisetyp):
    if 'Flug- & Busreise' in reisetyp:
      return 'u-palette-1-light-1'
    elif 'Busreise' in reisetyp:
      return 'u-palette-2-base'
    elif 'Flugreise' in reisetyp:
      return 'u-palette-1-light-1'
    elif 'anderreise' in reisetyp:
      return 'u-custom-color-1'
    elif 'Kurreise' in reisetyp:
      return 'u-palette-4-base'
    elif 'Schiffsreise' in reisetyp:
      return 'u-palette-1-base'
    elif 'Fluss' in reisetyp:
      return 'u-palette-1-base'
    else:
      return ''

@register.filter
@stringfilter
def land(reiseziel):
    if 'web' in reiseziel:
      return re.sub(r'web', u'', reiseziel)
   # elif 'Busreise' in reisetyp:
   #   return reisetyp
    else:
      return reiseziel