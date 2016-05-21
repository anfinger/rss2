# -*- coding: utf-8 -*-
from django.db.models import Min, F, Value as V

from .models import Reise, Reisetermine

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

def get_detail_angebote_queryset(pk):
    reise = Reise.objects.get(pk=pk)
    reise = reise.reiseangebote_set.annotate(angebot=F('angebot_id__angebot'), titel_master=F('angebot_id__titel'))
    return reise.values('position', 'titel', 'titel_master','angebot')

def get_detail_auftragsbestaetigungen_queryset(pk):
    reise = Reise.objects.get(pk=pk)
    reise = reise.reiseauftragsbestaetigungen_set.annotate(auftragsbestaetigung=F('auftragsbestaetigung_id__auftragsbestaetigung'), titel_master=F('auftragsbestaetigung_id__titel'))
    return reise.values('position', 'titel', 'titel_master','auftragsbestaetigung')
