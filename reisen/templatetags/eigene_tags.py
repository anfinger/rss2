# -*- coding: utf8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.humanize.templatetags.humanize import intcomma
from collections import OrderedDict 
import re
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
      if "webItalien" in termin.name:
        webZielregion = re.sub(r'webItalien', 'Frankreich / Italien / Andorra', termin.name)
      if u"webOesterreich" in termin.name:
        webZielregion = re.sub(r'webOesterreich', u'Schweiz / Österreich / Tschechien / Slovakei / Ungarn', termin.name)
      if u"webSlovakei" in termin.name:
        webZielregion = re.sub(r'webSlovakei', u'Schweiz / Österreich / Tschechien / Slovakei / Ungarn', termin.name)
      if u"webSkandinavien" in termin.name:
        webZielregion = re.sub(r'webSkandinavien', u'Baltikum / Skandinavien / Finnland / Island', termin.name)
      if u"webDeutschland" in termin.name:
        webZielregion = re.sub(r'webDeutschland', u'Deutschland', termin.name)
      if u"webBenelux" in termin.name:
        webZielregion = re.sub(r'webBenelux', u'Benelux', termin.name)
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
    else:
      return ''
