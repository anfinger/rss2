# -*- coding: utf8 -*-

from django.contrib import admin
from django.utils import timezone
from django.forms import TextInput, Textarea
from django.db import models
#from nested_inline.admin import NestedStackedInline, NestedModelAdmin
import nested_admin
from .models import Reise
from .models import Reisetermine
from .models import Hinweis
from .models import Kategorie
from .models import Zielregion
from .models import Ausflugspakete
from .models import Preis
from .models import Reisepreise
from .models import Reisetage
from .models import LeistungenReise
from .models import Fruehbucherrabatt
from .models import Zusatzleistung
from .models import Reisehinweise
from .models import Reisekategorien
from .models import Reisezielregionen
from .models import LeistungenAusflugspaket
from .models import Ausflugspaketpreise
from .models import AusflugspaketeZuReisetagen
from .models import ReisepreisZusatz


from .forms import ReiseForm, AusflugspaketeForm

################################################################################
# Inline Klassendefinitionen (könnten auch nach admin.py wandern)              #
################################################################################

class ReisetageInline(admin.StackedInline):
    model = Reisetage
    ordering = ("tagnummer",)
    extra = 0

class ReisetermineInline(admin.TabularInline):
    model = Reisetermine
    ordering = ("datum_beginn",)
    extra = 0

class LeistungenReiseInline(admin.TabularInline):
    model = LeistungenReise
    ordering = ("position",)
    extra = 0

class FruehbucherrabattInline(admin.TabularInline):
    model = Fruehbucherrabatt
    ordering = ("position",)
    extra = 0

class ZusatzleistungInline(admin.TabularInline):
    model = Zusatzleistung
    ordering = ("position",)
    extra = 0

class ReisehinweiseInline(admin.TabularInline):
    model = Reisehinweise
    ordering = ("position",)
    extra = 0

class ReisekategorienInline(admin.TabularInline):
    model = Reisekategorien
    ordering = ("position",)
    extra = 0

class ReisezielregionenInline(admin.TabularInline):
    model = Reisezielregionen
    ordering = ("position",)
    extra = 0

class LeistungenAusflugspaketInline(nested_admin.NestedStackedInline):
    model = LeistungenAusflugspaket
    ordering = ("position",)
    #sortable_field_name = "position"
    extra = 0

class AusflugspaketpreiseInline(nested_admin.NestedStackedInline):
    model = Ausflugspaketpreise
    ordering = ("position",)
    #sortable_field_name = "position"
    extra = 0

class AusflugspaketeZuReisetagenInline(nested_admin.NestedStackedInline):
    model = AusflugspaketeZuReisetagen
    ordering = ("position",)
    #sortable_field_name = "position"
    extra = 0

#class AusflugspaketeAdmin(nested_admin.NestedAdmin):
#
#    form = AusflugspaketeForm
#
#    list_display = ('titel', 'position')
#
#    formfield_overrides = {
#        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
#        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
#    }
#
#    filter_horizontal = ('gehoert_zu_reisetagen',)

class AusflugspaketInline(nested_admin.NestedStackedInline):
    model = Ausflugspakete
    form = AusflugspaketeForm
    ordering = ("position",)
    #sortable_field_name = "position"
    inlines = [AusflugspaketpreiseInline, AusflugspaketeZuReisetagenInline, LeistungenAusflugspaketInline]
    extra = 0

class ReisepreisZusatzInline(nested_admin.NestedStackedInline):
    model = ReisepreisZusatz
    ordering = ("position",)
    #sortable_field_name = "position"
    extra = 0

class ReisepreiseInline(nested_admin.NestedStackedInline):
    model = Reisepreise
    ordering = ("position",)
    #sortable_field_name = "position"
    inlines = [ReisepreisZusatzInline]
    extra = 0

################################################################################
# Adminoberflächen                                                             #
################################################################################

#class ReiseAdmin(admin.ModelAdmin):
#class ReiseAdmin(NestedModelAdmin):
class ReiseAdmin(nested_admin.NestedAdmin):

    form = ReiseForm

    save_on_top = True
    save_as = True

    list_display = ('titel', 'reisetermine', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    #list_display_links = ('titel', 'reisetermine')
    #list_editable = ('titel',)
    list_filter = ('titel', 'reisetermine', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    search_fields = ['titel',]
    filter_vertical = ('hinweise',)

    def reisetermine(self, obj):
        str_termin = ''
        for termin in Reisetermine.objects.select_related('reise_id').filter(reise_id=obj.reiseID):
            str_termin = str_termin + str(termin) + '\n'
        return str_termin
        #return Reisetermine.objects.select_related('reise_id').filter(reise_id=obj.reiseID)[0]

    prepopulated_fields = { 'slug': ['titel'] }
    readonly_fields = ('zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'autor_id', 'datum_erzeugung')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'60'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':60})},
    }

    fieldsets = ((
        'Reise', {
            'fields': ('titel', 'slug'),
            'classes': ('wide', 'extrapretty',)
        }), (
        'Reisedetails Standard', {
            'fields': (
                'reisetyp',
                'untertitel',
                'einleitung',
                'katalogseite',
                'anzahl_seiten_im_katalog',),
            'classes': ('collapse', 'wide', 'extrapretty',)
        }), (
        'Reisedetails Zusätze', {
            'fields': (
                'leistungen_kommentar',
                'zusatzleistungen_titel',
                'zusatzleistungen_kommentar',
                'zubucher',),
            'classes': ('collapse', 'wide', 'extrapretty',)
        }), (
        'Korrekturen (NUR INTERN)', {
            'fields': ('korrektur_bemerkung_intern',),
            'classes': ('collapse', 'wide', 'extrapretty',)
        }), (
        'Informationen zur Publikation', {
            'fields': ('datum_veroeffentlichung', 'datum_verfall', 'datum_erzeugung', 'autor_id', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von'),
            'classes': ('collapse', 'wide', 'extrapretty',)
        })
    )

    inlines = (
        ReisetermineInline,
        ReisetageInline,
        LeistungenReiseInline,
        FruehbucherrabattInline,
        ZusatzleistungInline,
        ReisehinweiseInline,
        ReisekategorienInline,
        ReisezielregionenInline,
        AusflugspaketInline,
        ReisepreiseInline,
    )

    def save_model(self, request, obj, form, change):
        if not obj.autor_id:
            obj.autor_id = request.user
        obj.zuletzt_bearbeitet_von = request.user
        obj.zuletzt_bearbeitet = timezone.now()
        obj.save()

admin.site.register(Reise, ReiseAdmin)
admin.site.register(Hinweis)
admin.site.register(Kategorie)
admin.site.register(Zielregion)
admin.site.register(Preis)
#admin.site.register(Ausflugspakete, AusflugspaketeAdmin)
