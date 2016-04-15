# -*- coding: utf-8 -*-

from django.shortcuts import render
from .querysets import get_index_queryset_v3, get_detail_hinweise_queryset, get_detail_preise_queryset


def index(request):

    termine = get_index_queryset_v3()
    return render(request, 'reisen/indexpopindex.html', {'termine': termine})


def reise_detail(request, pk):

    template = 'reisen/detailpopail.html'
    hinweise = get_detail_hinweise_queryset(pk)
    preise = get_detail_preise_queryset(pk)
    return render(request, template, {'preise': preise,
                                      'hinweise': hinweise})
