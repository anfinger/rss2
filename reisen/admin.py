# -*- coding: utf8 -*-

from django.contrib import admin
from django.utils import timezone
from django.forms import TextInput, Textarea
from django.db import models
from django.db import connection
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
from .models import Angebot
from .models import Reiseangebote

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
    fields = ('datum_beginn', 'datum_ende', 'kommentar', 'markierung')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class LeistungenReiseInline(admin.TabularInline):
    model = LeistungenReise
    fields = ('position', 'leistung')
    #ordering = ("position",)
    sortable_field_name = "position"
    classes = ('grp-collapse grp-closed',)
    extra = 0

class FruehbucherrabattInline(admin.TabularInline):
    model = Fruehbucherrabatt
    fields = ('position', 'rabatt', 'datum_bis')
    ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ZusatzleistungInline(admin.TabularInline):
    model = Zusatzleistung
    ordering = ("position",)
    fields = ('position', 'titel', 'preis')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisehinweiseInline(admin.TabularInline):
    model = Reisehinweise
    #ordering = ("position",)
    sortable_field_name = "position"
    fields = ('position', 'hinweis_id', 'titel')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisekategorienInline(admin.TabularInline):
    model = Reisekategorien
    ordering = ("position",)
    fields = ('position', 'kategorie_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisezielregionenInline(admin.TabularInline):
    model = Reisezielregionen
    ordering = ("position",)
    fields = ('position', 'zielregion_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisebilderInline(admin.TabularInline):
    model = Reisebilder
    ordering = ("position",)
    fields = ('position', 'titel', 'zu_verwenden_in', 'bild_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReiseangeboteInline(admin.TabularInline):
    model = Reiseangebote
    ordering = ("position",)
    fields = ('position', 'titel', 'angebot_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class LeistungenAusflugspaketInline(nested_admin.NestedStackedInline):
    model = LeistungenAusflugspaket
    ordering = ("position",)
    fields = ('position', 'leistung')
    classes = ('grp-collapse grp-closed',)
    #sortable_field_name = "position"
    extra = 0

class AusflugspaketpreiseInline(nested_admin.NestedStackedInline):
    model = Ausflugspaketpreise
    ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'preis', 'preis_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class AusflugspaketeZuReisetagenInline(nested_admin.NestedStackedInline):
    model = AusflugspaketeZuReisetagen
    ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'ausflugspaket_text', 'erscheint_in', 'reisetag_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0
    #raw_id_fields = ('reisetag_id',)
    #related_lookup_fields = {
    #    'fk': ['reisetag_id'],
    #}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reisetag_id":
            parent_obj_id = request.resolver_match.args[0]
            kwargs["queryset"] = Reisetage.objects.filter(reise_id=parent_obj_id)
            #kwargs["queryset"] = Reisetage.objects.filter(reise_id='0045c00949724a9ebfd0dd3bca286aff')
        return super(AusflugspaketeZuReisetagenInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class AusflugspaketInline(nested_admin.NestedStackedInline):
    model = Ausflugspakete
    form = AusflugspaketeForm
    ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'titel', 'kommentar_titel', 'kommentar')
    classes = ('grp-collapse grp-closed',)

    # fieldsets = (
    #     ("Ausflugspakete",
    #         {
    #             "classes": ("grp-collapse grp-closed",),
    #             "fields": ('position', 'titel', 'kommentar_titel', 'kommentar'),
    #         }
    #     ),
    #     ("Leistungen Ausflugspaket",
    #         {
    #             "classes": ("placeholder ausflugspaket_id-group",),
    #             "fields" : (),
    #         }
    #     ),
    # )

    inlines = [AusflugspaketpreiseInline, AusflugspaketeZuReisetagenInline, LeistungenAusflugspaketInline]
    extra = 0

class ReisepreisZusatzInline(nested_admin.NestedStackedInline):
    model = ReisepreisZusatz
    ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'preis_id', 'preis')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisepreiseInline(nested_admin.NestedStackedInline):
    model = Reisepreise
    ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'preis_id', 'preis', 'kommentar')
    classes = ('grp-collapse grp-closed',)
#    fieldsets = (
#    ("Reisepreise",
#        {
#            "classes": ("grp-collapse grp-closed",),
#            "fields": ('position', 'preis_id', 'preis', 'kommentar'),
#        }
#    ),)
#    ("Reisepreisdetails",
#        {
#            "classes": ("placeholder reisepreis_id-group",),
#            "fields" : ('position', 'preis_id', 'preis'),
#        }
#    ),)
    inlines = [ReisepreisZusatzInline]
    extra = 0

################################################################################
# Adminoberflächen                                                             #
################################################################################

class ReiseAdmin(nested_admin.NestedAdmin): #TabbedModelAdmin,

    form = ReiseForm

    save_on_top = True
    save_as = True

    actions = ['make_published', 'make_unpublished', 'make_finish','make_idea','make_draft', 'make_sommer', 'make_winter', 'make_sommer_und_winter', 'make_keinkatalog']

    # Satus Funktionen für alle Reisen
    def make_finish(self, request, queryset):
        rows_updated = queryset.update(status='f')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich veröffentlicht." % message_bit)
    make_finish.short_description = "fertigstellen"
    def make_idea(self, request, queryset):
        rows_updated = queryset.update(status='i')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich als Idee markiert." % message_bit)
    make_idea.short_description = "als Idee markieren"
    def make_draft(self, request, queryset):
        rows_updated = queryset.update(status='e')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich als Entwurf markiert." % message_bit)
    make_draft.short_description = "als Entwurf markieren"
    def make_sommer(self, request, queryset):
        rows_updated = queryset.update(welcher_katalog='s')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich dem Sommerkatalog zugeordnet." % message_bit)
    make_sommer.short_description = "Sommerkatalog zuordnen"
    def make_winter(self, request, queryset):
        rows_updated = queryset.update(welcher_katalog='w')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich dem Winterkatalog zugeordnet." % message_bit)
    make_winter.short_description = "Winterkatalog zuordnen"
    def make_sommer_und_winter(self, request, queryset):
        rows_updated = queryset.update(welcher_katalog='a')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich dem Sommer- und Winterkatalog zugeordnet." % message_bit)
    make_sommer_und_winter.short_description = "Sommer- und Winterkatalog zuordnen"
    def make_keinkatalog(self, request, queryset):
        rows_updated = queryset.update(welcher_katalog='n')
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich keinem Katalog zugeordnet." % message_bit)
    make_keinkatalog.short_description = "keinem Katalog zuordnen"
    def make_published(self, request, queryset):
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        rows_updated = queryset.update(datum_veroeffentlichung = timezone.now())
        rows_updated = queryset.update(datum_verfall = None)
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich veröffentlicht." % message_bit)
    make_published.short_description = "Veröffentlichen"
    def make_unpublished(self, request, queryset):
        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
        rows_updated = queryset.update(datum_veroeffentlichung = None)
        rows_updated = queryset.update(datum_verfall = None)
        if rows_updated == 1:
            message_bit = "1 Reise wurde"
        else:
            message_bit = "%s Reisen wurden" % rows_updated
        self.message_user(request, "%s erfolgreich \"un\"-veröffentlicht." % message_bit)
    make_unpublished.short_description = "\"un\"-Veröffentlichen"

    list_display = ('titel', 'reisetermine', 'status', 'welcher_katalog', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    #list_display_links = ('titel', 'reisetermine')
    #list_editable = ('titel',)
    list_filter = ('titel', 'reisetermine', 'status', 'welcher_katalog', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    search_fields = ['titel',]
    #filter_vertical = ('hinweise',)

    # def reisetermine(self, obj):
    #     qs = obj.reisetermine_set.all().order_by('datum_beginn')
    #     termine = ''
    #     for termin in obj.reisetermine_set.all().order_by('datum_beginn'):
    #         termine = termine + str(termin) + '\nhuhu\n'
    #     return termine
    #     #return qs.values_list('datum_beginn', flat=True)[0] #+ qs.values('datum_ende')
    #
    #def reisetermin_ordnung(self, obj):
    #     cursor = connection.cursor()
    #     cursor.execute("SELECT MIN(datum_beginn) as min_datum FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "' GROUP BY reise_id_id ORDER BY min_datum;");
    #     termine = namedtuplefetchall(cursor)
    #     cursor.close()
    #     return termine[0].reise_termine
    #reisetermine.admin_order_field = 'reisetermin_ordnung'

    def reisetermine(self, obj):
        cursor = connection.cursor()
        cursor.execute("SELECT MIN(datum_beginn) as min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d.'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR ' ::: ') AS reise_termine FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "' GROUP BY reise_id_id ORDER BY min_datum;");
        termine = namedtuplefetchall(cursor)
        cursor.close()
        return termine[0].reise_termine

    prepopulated_fields = { 'slug': ['titel'] }
    readonly_fields = ('zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'autor_id', 'datum_erzeugung')

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80', 'class': "vTextField"})},
    }

    fieldsets = ((
        'Korrekturen (NUR INTERN)', {
            'fields': ('korrektur_bemerkung_intern',),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-open',)
        }), (
        'Reise', {
            'fields': ('titel', 'slug', ('status', 'welcher_katalog')),
            'classes': ('wide', 'extrapretty', 'extrapretty', 'grp-collapse grp-open',)
        }), (
        'Reisedetails Standard', {
            'fields': (
                'reisetyp',
                'untertitel',
                'einleitung',
                ('katalogseite', 'anzahl_seiten_im_katalog'),
            ),
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
            'fields': (('datum_veroeffentlichung', 'datum_verfall'), ('datum_erzeugung', 'autor_id', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von')),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-closed',)
#        }), (
#        'ReisetermineInline', {
#            'fields' : ('datum_beginn', 'datum_ende', 'kommentar', 'markierung'),
#            'classes': ("placeholder reisetermine-group",),
        }),
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
        ReiseangeboteInline,
    )

    def save_model(self, request, obj, form, change):
        #if '_saveasnew' in request.POST: #falls anderes verhalten bei save as new
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
admin.site.register(Angebot)
