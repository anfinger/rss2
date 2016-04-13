# -*- coding: utf-8 -*-

from django.shortcuts import render
from .querysets import get_index_queryset_v3


def index(request):

    reisen = get_index_queryset_v3()
    return render(request, 'reisen/indexpopindex.html', {'reisen': reisen})
