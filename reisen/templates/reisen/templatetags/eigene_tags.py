from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='reise_kategorie')
@stringfilter
def reise_kategorie(kategorie, termine):
    gefilterte_reisen = termine.filter(kategorie=kategorie)
    return gefilterte_reisen if gefilterte_reisen else None
