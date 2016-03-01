# -*- coding: utf8 -*-

from django.contrib import admin
from django.utils import timezone
from django.forms import TextInput, Textarea
from django.db import models
from django.db import connection
#from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from tabbed_admin import TabbedModelAdmin
import nested_admin
#from grappelli.forms import GrappelliSortableHiddenMixin
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
from .models import Bild
from .models import Reisebilder

from .views import namedtuplefetchall

from .forms import ReiseForm, AusflugspaketeForm

################################################################################
# Inline Klassendefinitionen (könnten auch nach admin.py wandern)              #
################################################################################

class ReisetageInline(admin.StackedInline):
    model = Reisetage
    ordering = ("tagnummer",)
    #sortable_field_name = "tagnummer"
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisetermineInline(admin.TabularInline):
    model = Reisetermine
    ordering = ("datum_beginn",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class LeistungenReiseInline(admin.TabularInline):
    model = LeistungenReise
    #fields = ("leistung" , "position",)
    #ordering = ("position",)
    sortable_field_name = "position"
    classes = ('grp-collapse grp-closed',)
    extra = 0

class FruehbucherrabattInline(admin.TabularInline):
    model = Fruehbucherrabatt
    ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ZusatzleistungInline(admin.TabularInline):
    model = Zusatzleistung
    ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisehinweiseInline(admin.TabularInline):
    model = Reisehinweise
    #ordering = ("position",)
    sortable_field_name = "position"
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisekategorienInline(admin.TabularInline):
    model = Reisekategorien
    ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisezielregionenInline(admin.TabularInline):
    model = Reisezielregionen
    ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisebilderInline(admin.TabularInline):
    model = Reisebilder
    ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
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
    #raw_id_fields = ('reisetag_id',)
    #related_lookup_fields = {
    #    'fk': ['reisetag_id'],
    #}

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
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisepreisZusatzInline(nested_admin.NestedStackedInline):
    model = ReisepreisZusatz
    ordering = ("position",)
    #sortable_field_name = "position"
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisepreiseInline(nested_admin.NestedStackedInline):
    model = Reisepreise
    ordering = ("position",)
    #sortable_field_name = "position"
    inlines = [ReisepreisZusatzInline]
    classes = ('grp-collapse grp-closed',)
    extra = 0

################################################################################
# Adminoberflächen                                                             #
################################################################################

#class ReiseAdmin(admin.ModelAdmin):
#class ReiseAdmin(NestedModelAdmin):
#class ReiseAdmin(nested_admin.NestedAdmin):
class ReiseAdmin(nested_admin.NestedAdmin): #TabbedModelAdmin,

    form = ReiseForm

    save_on_top = True
    save_as = True

    list_display = ('titel', 'reisetermine', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    #list_display_links = ('titel', 'reisetermine')
    #list_editable = ('titel',)
    list_filter = ('titel', 'reisetermine', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    search_fields = ['titel',]
    #filter_vertical = ('hinweise',)

    #def reisetermine(self, obj):
    #    str_termin = ''
    #    for termin in Reisetermine.objects.select_related('reise_id').filter(reise_id=obj.reiseID).order_by('datum_beginn'):
    #        str_termin = str_termin + str(termin) + '\n'
    #    return str_termin
        #return Reisetermine.objects.select_related('reise_id').filter(reise_id=obj.reiseID).order_by('datum_beginn')[0]

    #reisetermine.admin_order_field = 'datum_beginn'

    def reisetermine(self, obj):
        cursor = connection.cursor()
        #cursor.execute("SELECT MIN(datum_beginn) as min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d.'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR ' ::: ') AS reise_termine FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "' GROUP BY reise_id_id ORDER BY datum_beginn;");
        cursor.execute("SELECT MIN(datum_beginn) as min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d.'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR ' ::: ') AS reise_termine FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "' GROUP BY reise_id_id ORDER BY min_datum;");
        termine = namedtuplefetchall(cursor)
        cursor.close()
        return termine[0].reise_termine
        #return termine

    #def reisetermine_ordnung(self, obj):
    #    cursor = connection.cursor()
    #    cursor.execute("SELECT MIN(datum_beginn) as min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d.'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR '\n') AS reise_termine FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "' GROUP BY reise_id_id ORDER BY datum_beginn;");
    #    termine = namedtuplefetchall(cursor)
    #    cursor.close()
    #    return termine[0].min_datum
        #return termine

    #rt = str(type(rtt))
    #reisetermine.admin_order_field = 'reisetermine_ordnung'

    prepopulated_fields = { 'slug': ['titel'] }
    readonly_fields = ('zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'autor_id', 'datum_erzeugung')

    formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        #models.TextField: {'widget': Textarea(attrs={'rows':'4', 'cols':'10'})},
        models.CharField: {'widget': TextInput(attrs={'size':'80', 'class': "vTextField"})},
        #models.TextField: {'widget': TextInput(attrs={'rows':'50', 'class': "vLargeTextField"})},
    }

    fieldsets = ((
        'Korrekturen (NUR INTERN)', {
            'fields': ('korrektur_bemerkung_intern',),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-open',)
        }), (
        'Reise', {
            'fields': ('titel', 'slug'),
            'classes': ('wide', 'extrapretty', 'extrapretty', 'grp-collapse grp-open',)
        }), (
        'Reisedetails Standard', {
            'fields': (
                'reisetyp',
                'untertitel',
                'einleitung',
                'katalogseite',
                'anzahl_seiten_im_katalog',),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-closed',)
        }), (
        'Reisedetails Zusätze', {
            'fields': (
                'leistungen_kommentar',
                'zusatzleistungen_titel',
                'zusatzleistungen_kommentar',
                'zubucher',),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-closed',)
        }), (
        'Informationen zur Publikation', {
            'fields': ('datum_veroeffentlichung', 'datum_verfall', 'datum_erzeugung', 'autor_id', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von'),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-closed',)
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
        ReisebilderInline,
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
admin.site.register(Bild)
#admin.site.register(Reisetage)
#admin.site.register(AusflugspaketeZuReisetagen)
#admin.site.register(Ausflugspakete, AusflugspaketeAdmin)
