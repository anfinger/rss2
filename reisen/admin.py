# -*- coding: utf8 -*-

from django.core.files.storage import DefaultStorage
#from filebrowser.sites import FileBrowserSite

from django.contrib import admin
from django.utils import timezone
from django.forms import TextInput, Textarea
from django.db import models
from django.db import connection
import nested_admin
#from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin
from grappelli.forms import GrappelliSortableHiddenMixin
from .models import Reise
from .models import Reisetermine
from .models import Abfahrtszeiten
from .models import Hinweis
from .models import Kategorie
from .models import Zielregion
from .models import Ausflugspakete
from .models import Preis
from .models import Reisepreise
from .models import Reisetage
from .models import Reisebeschreibung
from .models import LeistungenReise
from .models import Fruehbucherrabatt
from .models import Zusatzleistung
from .models import Reisehinweise
from .models import Reisekategorien
from .models import Reisezielregionen
from .models import Bildzielregionen
from .models import LeistungenAusflugspaket
from .models import Ausflugspaketpreise
from .models import AusflugspaketeZuReisetagen
from .models import ReisepreisZusatz
from .models import Bild
from .models import Reisebilder
from .models import Bildanbieter
from .models import Bildanbieterzubild
from .models import Angebot
from .models import Reiseangebote
from .models import Katalog
from .models import Reisekatalogzugehoerigkeit
from .models import Auftragsbestaetigung
from .models import Reiseauftragsbestaetigungen

from .forms import ReiseForm, BildForm, AusflugspaketeForm

from .views import namedtuplefetchall

# Default FileBrowser site
#site = FileBrowserSite(name='filebrowser', storage=DefaultStorage())
#site.storage.location = "www.reiseservice-schwerin.de/media"

#print 'DEBUG' + site.storage.location + site.directory

################################################################################
# Inline Klassendefinitionen (könnten auch nach admin.py wandern)              #
################################################################################

#class ReisetageInline(admin.StackedInline):
class ReisetageInline(admin.TabularInline):
    model = Reisetage
    ordering = ("tagnummer",)
    #sortable_field_name = "tagnummer"
    classes = ('grp-collapse grp-closed',)
    #can_delete = True
    extra = 0

class ReisebeschreibungInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisebeschreibung
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisetermineInline(admin.TabularInline):
#class ReisetermineInline(admin.StackedInline):
    model = Reisetermine
    ordering = ("datum_beginn",)
    fields = ('datum_beginn', 'datum_ende', 'kommentar', 'markierung')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class AbfahrtszeitenInline(GrappelliSortableHiddenMixin, admin.TabularInline):
#class ReisetermineInline(admin.StackedInline):
    model = Abfahrtszeiten
    fields = ('ort', 'zeit', 'kommentar', 'position', )
    classes = ('grp-collapse grp-closed',)
    extra = 0

class LeistungenReiseInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = LeistungenReise
    fields = ('position', 'leistung')
    #ordering = ("position",)
    #sortable_field_name = "position"
    classes = ('grp-collapse grp-closed',)
    extra = 0

class FruehbucherrabattInline(admin.TabularInline):
    model = Fruehbucherrabatt
    fields = ('rabattbezeichnung', 'rabatt', 'datum_bis')
    #ordering = ("position",)
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ZusatzleistungInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Zusatzleistung
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'titel', 'preis')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisehinweiseInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisehinweise
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'hinweis_id', 'titel')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisekatalogzugehoerigkeitInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisekatalogzugehoerigkeit
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'katalog_id', 'katalogseite', 'anzahl_seiten_im_katalog', 'position_auf_seite', 'titel', 'katalog_pdf')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisekategorienInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisekategorien
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'kategorie_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "kategorie_id":
        kwargs["queryset"] = Kategorie.objects.order_by('kategorie')
        return super(ReisekategorienInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class BildanbieterzubildInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Bildanbieterzubild
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'bildanbieter_id', 'bildnummer', 'url', 'kommentar')
    classes = ('grp-collapse grp-closed',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "bildanbieter_id":
        kwargs["queryset"] = Bildanbieter.objects.order_by('bildanbieter')
        return super(BildanbieterzubildInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ReisezielregionenInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisezielregionen
    #ordering = ("zielregion_id")
    #sortable_field_name = "position"
    fields = ('position', 'zielregion_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "zielregion_id":
        kwargs["queryset"] = Zielregion.objects.order_by('name')
        return super(ReisezielregionenInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class BildzielregionenInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Bildzielregionen
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'zielregion_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "zielregion_id":
        kwargs["queryset"] = Zielregion.objects.order_by('name')
        return super(BildzielregionenInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ReisebilderInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisebilder
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'titel', 'zu_verwenden_in', 'bild_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "bild_id":
        kwargs["queryset"] = Bild.objects.order_by('titel')
        return super(ReisebilderInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class BilderzurreiseInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reisebilder
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'titel', 'zu_verwenden_in', 'reise_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
      if db_field.name == "reise_id":
        kwargs["queryset"] = Reise.objects.order_by('titel')
        return super(BilderzurreiseInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ReiseangeboteInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reiseangebote
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'titel', 'angebot_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReiseauftragsbestaetigungenInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Reiseauftragsbestaetigungen
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'titel', 'auftragsbestaetigung_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class LeistungenAusflugspaketInline(GrappelliSortableHiddenMixin, nested_admin.NestedStackedInline):
    model = LeistungenAusflugspaket
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'leistung')
    classes = ('grp-collapse grp-closed',)
    #sortable_field_name = "position"
    extra = 0

class AusflugspaketpreiseInline(GrappelliSortableHiddenMixin, nested_admin.NestedStackedInline):
    model = Ausflugspaketpreise
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'preis', 'preis_id')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class AusflugspaketeZuReisetagenInline(GrappelliSortableHiddenMixin, nested_admin.NestedStackedInline):
    model = AusflugspaketeZuReisetagen
    #ordering = ("position",)
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
            #try:
            if len(request.resolver_match.args) > 0:
                parent_obj_id = request.resolver_match.args[0]
                #kwargs["queryset"] = Reisetage.objects.filter(reise_id = parent_obj_id)
            else:
            #except:
                parent_obj_id = None
                #kwargs["queryset"] = Reisetage.objects.filter(reise_id = parent_obj_id)
            #kwargs["queryset"] = Reisetage.objects.filter(reise_id='0045c00949724a9ebfd0dd3bca286aff')
            kwargs["queryset"] = Reisetage.objects.filter(reise_id = parent_obj_id)
        return super(AusflugspaketeZuReisetagenInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class AusflugspaketInline(GrappelliSortableHiddenMixin, nested_admin.NestedStackedInline):
    model = Ausflugspakete
    form = AusflugspaketeForm
    #ordering = ("position",)
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

class ReisepreisZusatzInline(GrappelliSortableHiddenMixin, nested_admin.NestedStackedInline):
    model = ReisepreisZusatz
    #ordering = ("position",)
    #sortable_field_name = "position"
    fields = ('position', 'preis_id', 'preis')
    classes = ('grp-collapse grp-closed',)
    extra = 0

class ReisepreiseInline(GrappelliSortableHiddenMixin, nested_admin.NestedStackedInline):
    model = Reisepreise
    #ordering = ("position",)
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

#    class Media:
#        js = [
#            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
#            '/static/grappelli/tinymce_setup/tinymce_setup.js',
#        ]

    form = ReiseForm

    save_on_top = True
    save_as = True

    actions = ['make_published', 'make_unpublished', 'make_finish','make_idea','make_draft']#, 'make_sommer', 'make_winter', 'make_sommer_und_winter', 'make_keinkatalog']

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
#    def make_sommer(self, request, queryset):
#        rows_updated = queryset.update(welcher_katalog='s')
#        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
#        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
#        if rows_updated == 1:
#            message_bit = "1 Reise wurde"
#        else:
#            message_bit = "%s Reisen wurden" % rows_updated
#        self.message_user(request, "%s erfolgreich dem Sommerkatalog zugeordnet." % message_bit)
#    make_sommer.short_description = "Sommerkatalog zuordnen"
#    def make_winter(self, request, queryset):
#        rows_updated = queryset.update(welcher_katalog='w')
#        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
#        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
#        if rows_updated == 1:
#            message_bit = "1 Reise wurde"
#        else:
#            message_bit = "%s Reisen wurden" % rows_updated
#        self.message_user(request, "%s erfolgreich dem Winterkatalog zugeordnet." % message_bit)
#    make_winter.short_description = "Winterkatalog zuordnen"
#    def make_sommer_und_winter(self, request, queryset):
#        rows_updated = queryset.update(welcher_katalog='a')
#        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
#        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
#        if rows_updated == 1:
#            message_bit = "1 Reise wurde"
#        else:
#            message_bit = "%s Reisen wurden" % rows_updated
#        self.message_user(request, "%s erfolgreich dem Sommer- und Winterkatalog zugeordnet." % message_bit)
#    make_sommer_und_winter.short_description = "Sommer- und Winterkatalog zuordnen"
#    def make_keinkatalog(self, request, queryset):
#        rows_updated = queryset.update(welcher_katalog='n')
#        rows_updated = queryset.update(zuletzt_bearbeitet_von = request.user)
#        rows_updated = queryset.update(zuletzt_bearbeitet = timezone.now())
#        if rows_updated == 1:
#            message_bit = "1 Reise wurde"
#        else:
#            message_bit = "%s Reisen wurden" % rows_updated
#        self.message_user(request, "%s erfolgreich keinem Katalog zugeordnet." % message_bit)
#    make_keinkatalog.short_description = "keinem Katalog zuordnen"
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

    def welcherkatalog(self, obj):
        cursor = connection.cursor()
        cursor.execute("SELECT reisen_reise.titel, reisen_katalog.titel AS katalogtitel FROM reisen_reise LEFT JOIN reisen_reisekatalogzugehoerigkeit ON (reiseID = reise_id_id) LEFT JOIN reisen_katalog ON (katalogID = katalog_id_id) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "';");
        katalog = namedtuplefetchall(cursor)
        cursor.close()
        if len(katalog) > 0:
            return katalog[0].katalogtitel
        else:
            return ''

    list_display = ('titel', 'reisetermine', 'reisetyp', 'veranstalter', 'status', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id')
    #list_display_links = ('titel', 'reisetermine')
    #list_editable = ('titel',)
    list_filter = ('titel', 'reisetermine', 'status', 'datum_veroeffentlichung', 'datum_verfall', 'zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'datum_erzeugung', 'autor_id', 'reisetyp', 'veranstalter')
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
        cursor.execute("SELECT MIN(datum_beginn) as min_datum, group_concat(DISTINCT CONCAT_WS(' - ', DATE_FORMAT(datum_beginn,'%d. %m. %Y'), DATE_FORMAT(datum_ende,'%d. %m. %Y')) ORDER BY datum_beginn ASC SEPARATOR ' ::: ') AS reise_termine FROM reisen_reisetermine INNER JOIN reisen_reise ON (reise_id_id = reiseID) WHERE reise_id_id ='" + str(obj.reiseID).replace('-','') + "' GROUP BY reise_id_id ORDER BY min_datum;");
        termine = namedtuplefetchall(cursor)
        cursor.close()
        if len(termine) > 0:
            return termine[0].reise_termine
        else:
            return ''

    prepopulated_fields = { 'slug': ['titel'] }
    readonly_fields = ('zuletzt_bearbeitet', 'zuletzt_bearbeitet_von', 'autor_id', 'datum_erzeugung')

    #tinyMCE.init({
        
    #});
        
    formfield_overrides = {
        #models.CharField: {'widget': TextInput(attrs={'size':'80', 'class': "vTextField"})},
        #models.TextField: {'widget': Textarea(attrs={'class':'mceEditor', 'rows': '50', 'id':'id_korrektur_bemerkung_intern'})},
    }

    fieldsets = ((
        'Korrekturen (NUR INTERN)', {
            'fields': ('korrektur_bemerkung_intern',),
            'classes': ('collapse', 'wide', 'extrapretty', 'grp-collapse grp-open',)
        }), (
        'Reise', {
            'fields': (('veranstalter', 'reisetyp', 'status',), 'titel', 'slug', 'untertitel', 'einleitung'),
            'classes': ('wide', 'extrapretty', 'extrapretty', 'grp-collapse grp-open',)
        }), (
        'Reisedetails', {
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
        ReisekatalogzugehoerigkeitInline,
        ReisetermineInline,
        AbfahrtszeitenInline,
        ReisebeschreibungInline,
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
        ReiseauftragsbestaetigungenInline,
    )

    def save_model(self, request, obj, form, change):
        #if '_saveasnew' in request.POST: #falls anderes verhalten bei save as new
        if not obj.autor_id:
            obj.autor_id = request.user
        obj.zuletzt_bearbeitet_von = request.user
        obj.zuletzt_bearbeitet = timezone.now()
        obj.save()

class BildAdmin(admin.ModelAdmin): #TabbedModelAdmin,

    form = BildForm

    save_on_top = True
    save_as = True

    list_display = ('titel', 'beschreibung')
    list_filter = ('titel', 'beschreibung')
    search_fields = ['titel', 'beschreibung']

    inlines = (
        BildzielregionenInline,
        BildanbieterzubildInline,
        BilderzurreiseInline,
    )

admin.site.register(Reise, ReiseAdmin)
admin.site.register(Hinweis)
admin.site.register(Kategorie)
admin.site.register(Zielregion)
admin.site.register(Preis)
admin.site.register(Bild, BildAdmin)
admin.site.register(Bildanbieter)
#admin.site.register(Reisebilder)
admin.site.register(Angebot)
admin.site.register(Auftragsbestaetigung)
admin.site.register(Katalog)
