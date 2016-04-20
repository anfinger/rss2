# -*- coding: utf8 -*-

from django.contrib import admin
from django.utils import timezone
from django.db import models
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
import re
import uuid
from django.core.validators import MinValueValidator #, MaxValueValidator

#from django.core.files.storage import FileSystemStorage
#from django.core.files.storage import DefaultStorage
#from filebrowser.sites import FileBrowserSite
#from filebrowser.sites import site
#from filebrowser.fields import FileBrowseField
#from filer.fields.image import FilerImageField
#from filer.fields.file import FilerFileField

#site = FileBrowserSite(name='bild_id', storage=DefaultStorage())
#site.directory = "/images/"
#print 'MODELS  : ' + site.storage.location + site.directory

#site = FileBrowserSite(name='filebrowser', storage=DefaultStorage())
#site.directory = 'images/'
#site.storage.location = DefaultStorage().location
# = FileSystemStorage(location='/var/www/reiseservice-schwerin/rss2', base_url='/media/')

STATUS_CHOICES = (
    ('i', 'Idee'),
    ('e', 'Entwurf'),
    ('f', 'fertiggestellt'),
)

#KATALOG_CHOICES = (
#    ('w', 'Winterkatalog'),
#    ('s', 'Sommerkatalog'),
#    ('a', 'Winter- und Sommerkatalog'),
#    ('n', 'nicht zugeordnet'),
#)

###########
# Bild    #
###########
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Bild(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Bild"
        verbose_name_plural = "Bilder"

    # Attribute
    bildID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    bild = models.ImageField(upload_to = 'images', blank = True, default = '' )#, default = 'images/None/no-img.jpg')
    #bild = FileBrowseField('filebrowser', max_length=200, directory="images/", extensions=[".jpg",".jpeg",".tif",".png",".tiff"], blank=True, null=True)#, default = 'images/None/no-img.jpg')
    #bild = FileBrowseField('id_bild', directory = '/images/', max_length=200, blank=True, null=True)#, default = 'images/None/no-img.jpg')
    #bild = FilerImageField(null=True, blank=True, related_name="reisen_bilder")
    titel = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Bildtitel",
        help_text = "Geben Sie hier den Titel des Bildes ein.")
    beschreibung = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Bildbeschreibung",
        help_text = "Geben Sie hier eine Bildbeschreibung ein.")
    bildquelle = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Bildquelle",
        help_text = "Geben Sie hier den Bildquelle ein. (privat, Kunde, Internet, BildDB)")

    # Bildtitel als Rückgabestring
    def __str__(self):
        return self.titel + ' ID: ' + str(self.bildID)

###############
# Angebot     #
###############
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Angebot(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Angebot"
        verbose_name_plural = "Angebote"

    # Attribute
    angebotID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    #angebot = FileBrowseField(max_length=200, directory="angebote/", extensions=[".pdf",".doc",".docx"], blank=True, null=True)#, default = 'images/None/no-img.jpg')
    angebot = models.FileField(upload_to = 'angebote', blank = True, default = '')#, default = 'images/None/no-img.jpg')
    titel = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Angebottitel",
        help_text = "Geben Sie hier den Titel des Angebots ein.")

    # Angebottitel als Rückgabestring
    def __str__(self):
        return self.titel + ' ID: ' + str(self.angebotID)

###########
# Katalog #
###########
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Katalog(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Katalog"
        verbose_name_plural = "Kataloge"

    # Attribute
    katalogID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Katalogtitel",
        help_text = "Geben Sie hier den Titel des Katalogs ein.")
    untertitel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Kataloguntertitel",
        help_text = "Geben Sie hier den Untertitel des Katalogs ein.")
    datum_beginn = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name = "Katalogstartdatum")
    datum_ende = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name = "Katalogendedatum")
    katalogseitenanzahl = models.PositiveSmallIntegerField(
        null = True,
        blank=True,
        verbose_name = "Anzahl der Katalogseiten")

    # hinweis Text als Rückgabestring
    def __str__(self):
        return self.titel

###########
# Hinweis #
###########
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Hinweis(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Hinweis"
        verbose_name_plural = "Hinweise"

    # Attribute
    hinweisID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    hinweis = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Hinweis",
        help_text = "Geben Sie hier den Hinweis ein.")

    # hinweis Text als Rückgabestring
    def __str__(self):
        return self.hinweis

#############
# Kategorie #
#############
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Kategorie(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    # Attribute
    kategorieID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    kategorie = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Kategorie",
        help_text = "Geben Sie hier die Kategorie ein.")

    # Kategorie Text als Rückgabestring
    def __str__(self):
        return self.kategorie

##############
# Zielregion #
##############
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Zielregion(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Zielregion"
        verbose_name_plural = "Zielregionen"

    # Attribute
    zielregionID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Zielregion",
        help_text = "Geben Sie hier die Zielregion ein.")

    # name als Rückgabestring
    def __str__(self):
        return self.name

##############
# Preis      #
##############
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Preis(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Preis"
        verbose_name_plural = "Preise"

    # Attribute
    preisID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    titel = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Titel/Preisart",
        help_text = "Geben Sie hier ein, was dann vorm Eurobetrag stehen soll.")

    # name als Rückgabestring
    def __str__(self):
        return self.titel

#########
# Reise #
#########
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reise(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reise"
        verbose_name_plural = "Reisen"

    # Attribute
    reiseID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    slug = models.SlugField(
        default = '',
        help_text="Geben Sie hier einen evtl. abweichenden URL-String ein.")
    autor_id = models.ForeignKey(
        User,
        related_name='reisen',
        blank = True,
        null = True)
    reisetyp = models.CharField(
        max_length=60,
        blank = True,
        default = '',
        verbose_name = "Reisetyp",
        help_text="Geben Sie hier den Typ der Reise ein. (max. 30 Zeichen) (Kann evtl. automatisch gefüllt werden.)")
    titel = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Reisetitel",
        help_text="Geben Sie hier den Titel der Reise ein. (max. 60 Zeichen)")
    untertitel = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Reiseuntertitel (etwa 40-70 Zeichen)")
    einleitung = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Reise Zusammenfassungstext (etwa 300-550 Zeichen)")
    datum_erzeugung = models.DateTimeField(
        default=timezone.now,
        verbose_name = "Erzeugungsdatum")
    zuletzt_bearbeitet = models.DateTimeField(
        default=timezone.now)
    zuletzt_bearbeitet_von = models.ForeignKey(
        User,
        related_name='reisen_bearbeiter',
        default = '',
        blank=True,
        null = True)
    datum_veroeffentlichung = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name = "Veröffentlichungsdatum")
    datum_verfall = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name = "Verfallsdatum")
    leistungen_kommentar = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Kommentar zu Leistungen, falls nötig. (etwa 40-70 Zeichen)")
    zusatzleistungen_titel = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Titelzeile für zusätzliche Leistungen, falls nötig. (etwa 40-70 Zeichen)")
    zusatzleistungen_kommentar = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Kommentar für zusätzliche Leistungen, falls nötig. (etwa 40-70 Zeichen)")
    korrektur_bemerkung_intern  = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Korrekturfeld",
        help_text="Wird nur intern dargestellt und dient Notizen die Reise betreffend, Korrekturbemerkungen, etc."
    )
    zubucher = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Text Zubucherreise, falls nötig. (etwa 40-70 Zeichen)"
    )
    hinweise = models.ManyToManyField(
        Hinweis,
        blank = True,
        through='Reisehinweise'
    )
    status = models.CharField(
        default = 'i',
        max_length = 1,
        choices = STATUS_CHOICES,
        verbose_name = "Status der Reise",
        help_text = "Hier den Status einer Reise wählen."
    )
#    welcher_katalog = models.CharField(
#        default = 'n',
#        max_length = 1,
#        choices = KATALOG_CHOICES,
#        verbose_name = "Welcher Katalog?",
#        help_text = "Hier Katalog für eine Reise wählen."
#    )

    #tage = models.ManyToManyField(Tag, through='Reisetage')
    #preis = models.DecimalField(max_digits=6, decimal_places=2, null = True, verbose_name = "Reisepreis")
    #@property
    #def preis(self):
    #    return "€%s" % self.preis
    #anzahlung = models.DecimalField(max_digits=6, decimal_places=2, null = True, verbose_name = "Anz. bei Buchung")
    #einzelzimmer_zuschlag = models.DecimalField(max_digits=6, decimal_places=2, null = True, verbose_name = "EZ-Zuschlag")
    #fruehbucherrabatt = models.DecimalField(max_digits=6, decimal_places=2, null = True, verbose_name = "Frühbucherrabatt")
    #fruehbucherrabatt_bis = models.DateTimeField(blank=True, null=True, verbose_name = "Verfallsdatum")

    # funktioniert nicht?
    #def publish(self):
    #    self.datum_veroeffentlichung = timezone.now()
    #    self.save()

    # Reisetitel als Rückgabestring
    def __str__(self):
        return self.titel

#############
# Reisetage #
#############
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisetage(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reisetag"
        verbose_name_plural = "Reisetage"
        ordering = ['tagnummer']

    # Attribute
    reisetagID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    tagnummer = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        null = True,
        verbose_name = "Tagesnummer zum Ordnen")
    titel = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name="Titel Tagesbeschreibung",
        help_text="Geben Sie hier den Titel der Tagesbeschreibung ein. (max. 70 Zeichen)")
    beschreibung = models.TextField(
        verbose_name = "Beschreibung Tag",
        blank = True,
        default = '',
        help_text="Geben Sie hier Tagesbeschreibung ein. (Die max. Anzahl Zeichen ist abhängig von Anzahl der Tage und Bilder je Reise etc. (etwa800))")
    zusatz = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Zusatz zur Tagesbeschreibung",
        help_text="Geben Sie hier zusätzliche Informationen zur Tagesbeschreibung ein. (Tipps, etc.)")

    # Titel Tagesbeschreibung als Rückgabestring
    def __str__(self):
        return str(self.tagnummer) + '. Tag: ' + self.titel

################
# Reisetermine #
################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisetermine(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reisetermin"
        verbose_name_plural = "Reisetermine"
        ordering = ['datum_beginn']

    # Attribute
    reiseterminID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        #related_name = '+',
        on_delete=models.CASCADE)
    markierung = models.CharField(
        max_length=20,
        blank = True,
        verbose_name = "Markierung",
        help_text = "Markierung für evt. Spezialtermine (*)")
    kommentar = models.CharField(
        max_length=20,
        blank = True,
        verbose_name = "Kommentar",
        help_text = "Kommentar/Hinweise")
    datum_beginn = models.DateField(
        blank = True,
        default = '',
        null = False,
        verbose_name = "Reisebeginn")
    datum_ende = models.DateField(
        blank = True,
        default = '',
        null = True,
        verbose_name = "Reiseende")

    # Start Datum als Rückgabestring
    def __str__(self):
        return str(self.datum_beginn)

    # @property
    # def id(self):
    #     return self.reiseterminID
    #
    # def related_label(self):
    #     return u"%s (%s)" % (self.datum_beginn, self.id)

########################
# Leistungen der Reise #
########################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class LeistungenReise(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reiseleistung"
        verbose_name_plural = "Reiseleistungen"
        ordering = ['position']

    # Attribute
    leistung_reiseID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    leistung = models.CharField(
        max_length=128,
        blank = True,
        verbose_name = "Leistung",
        help_text = "einzelne Leistung zur Reise")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Sortierung")

    # Leistung Text als Rückgabestring
    def __str__(self):
        return self.leistung

##############################
# Frühbucherrabatt zur Reise #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Fruehbucherrabatt(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Frühbucherrabatt"
        verbose_name_plural = "Frühbucherrabatte"
        ordering = ['position']

    # Attribute
    fruehbucherrabattID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    datum_bis = models.DateField(
        blank = True,
        default = '',
        null = False,
        verbose_name = "Datum Gültigkeit Frühbucherrabatt")
    rabatt = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null = True,
        verbose_name = "Rabatt")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge der Leistung bei der Darstellung")

    # datum_bis Text als Rückgabestring
    def __str__(self):
        return str(self.datum_bis)

##############################
# Zusatzleistungen zur Reise #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Zusatzleistung(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Zusatzleistung"
        verbose_name_plural = "Zusatzleistungen"
        ordering = ['position']

    # Attribute
    zusatzleistungID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Zusatzleistung",
        help_text="Geben Sie hier die Zusatzleistung ein.")
    preis = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null = True,
        verbose_name = "Preis")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge der Leistung bei der Darstellung")

    # datum_bis Text als Rückgabestring
    def __str__(self):
        return self.titel

##############################
# Reisekatalogzugehoerigkeit #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisekatalogzugehoerigkeit(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Welcher Katalog?"
        verbose_name_plural = "Welche Kataloge"
        ordering = ['position']

    # Attribute
    reisekatalog_zugehoerigkeitID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    katalog_id = models.ForeignKey(
        Katalog,
        verbose_name = "Katalog",
        help_text = "Suchen Sie hier einen Katalog aus.",
        on_delete=models.CASCADE)
    katalogseite = models.PositiveSmallIntegerField(
        null = True,
        blank=True,
        verbose_name = "Katalogseite")
    anzahl_seiten_im_katalog = models.PositiveSmallIntegerField(
        null = True,
        blank=True,
        verbose_name = "Anzahl der Seiten für diese Reise im Katalog")
    #katalog_pdf = FileBrowseField(max_length=200, directory="kataloge/", extensions=[".pdf"], blank=True, null=True)#, default = 'images/None/no-img.jpg')
    katalog_pdf = models.FileField(upload_to = 'kataloge', blank = True, default = '')#, default = 'images/None/no-img.jpg')
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "optionaler Titel",
        help_text="Geben Sie hier einen optionalen Titel ein. (Ersetzt Katalogtitel)")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Sortierung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position)

##############################
# Reisehinweise zur Reise    #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisehinweise(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reisehinweis"
        verbose_name_plural = "Reisehinweise"
        ordering = ['position']

    # Attribute
    reisehinweiseID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    hinweis_id = models.ForeignKey(
        Hinweis,
        verbose_name = "Hinweis",
        help_text = "Suchen Sie hier einen Hinweistext aus.",
        on_delete=models.CASCADE)
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "optionaler Titel",
        help_text="Geben Sie hier einen optionalen Titel ein.")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Sortierung")

    # titel Text als Rückgabestring
    def __str__(self):
        return self.titel

##############################
# Bilder zur Reise           #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisebilder(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reisebild"
        verbose_name_plural = "Reisebilder"
        ordering = ['position']

    # Attribute
    reisebildID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    bild_id = models.ForeignKey(
        Bild,
        on_delete=models.CASCADE)
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "optionaler Titel",
        help_text="Geben Sie hier einen optionalen Titel ein. (Überschreibt Standard Bildtitel)")
    zu_verwenden_in = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Bild verwenden in ...",
        help_text = "Geben Sie an ob das Bild etwa im Katalog, Internet, Katalogvorstellung, Reisetagebuch, etc. veröffentlicht werden soll. (kommaseparierte Liste)")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge der Bilder bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position)

##############################
# Angebote zur Reise         #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reiseangebote(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reiseangebot"
        verbose_name_plural = "Reiseangebote"
        ordering = ['position']

    # Attribute
    reiseangebotID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    angebot_id = models.ForeignKey(
        Angebot,
        on_delete=models.CASCADE)
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "optionaler Titel",
        help_text="Geben Sie hier einen optionalen Titel ein. (Überschreibt Standard Angebottitel)")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge der Angebote bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position)

###########################
# Kategorien zur Reise    #
###########################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisekategorien(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reisekategorie"
        verbose_name_plural = "Reisekategorien"
        ordering = ['position']

    # Attribute
    reisekategorienID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    kategorie_id = models.ForeignKey(
        Kategorie,
        verbose_name = "Reisekategorie",
        help_text = "Suchen Sie hier eine Reisekategorie aus.",
        on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Kategorien bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position)

#############################
# Zielregionen zur Reise    #
#############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisezielregionen(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Zielregion"
        verbose_name_plural = "Zielregionen"
        ordering = ['position']

    # Attribute
    reisezielregionenID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    zielregion_id = models.ForeignKey(
        Zielregion,
        verbose_name = "Zielregion",
        help_text = "Suchen Sie hier eine Zielregion aus.",
        on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Zielregionen bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position)

############################
# Ausflugspakete zur Reise #
############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Ausflugspakete(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Ausflugspaket"
        verbose_name_plural = "Ausflugspakete"
        ordering = ['position']

    # Attribute
    ausflugspaketID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    gehoert_zu_reisetagen = models.ManyToManyField(
        Reisetage,
        through='AusflugspaketeZuReisetagen')
    titel = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Titel Ausflugspaket",
        help_text = "Hier den Titel des Ausflugspakets eingeben")
    kommentar_titel = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Titelkommentar Ausflugspaket",
        help_text = "Hier den Titelkommentar zum Ausflugspaket eingeben")
    kommentar = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "kommentar Ausflugspaket",
        help_text = "Hier den Kommentar zum Ausflugspaket eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge der Leistung bei der Darstellung")

    # Leistung Text als Rückgabestring
    def __str__(self):
        return self.titel

###############################
# Leistungen zu Ausflugspaket #
###############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class LeistungenAusflugspaket(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Leistung zum Ausflugspaket"
        verbose_name_plural = "Leistungen zum Ausflugspaket"
        ordering = ['position']

    # Attribute
    leistung_ausflugspaketID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    ausflugspaket_id = models.ForeignKey(
        Ausflugspakete,
        on_delete=models.CASCADE)
    leistung = models.CharField(
        max_length = 256,
        blank = True,
        verbose_name = "Leistung Ausflugspaket",
        help_text = "Hier die Leistung zum Ausflugspaket eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge der Leistung bei der Darstellung")

    # Leistung Text als Rückgabestring
    def __str__(self):
        return self.leistung

#############################
# Preise zu Ausflugspaket   #
#############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Ausflugspaketpreise(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Ausflugspaketpreis"
        verbose_name_plural = "Ausflugspaketpreise"
        ordering = ['position']

    # Attribute
    ausflugspaketpreiseID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    ausflugspaket_id = models.ForeignKey(
        Ausflugspakete,
        on_delete=models.CASCADE)
    preis_id = models.ForeignKey(
        Preis,
        on_delete=models.CASCADE)
    preis = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null = True,
        verbose_name = "Preisdetail")
    #kommentar = models.CharField(
    #    max_length=256,
    #    blank = True,
    #    verbose_name = "Bemerkung zum Preis",
    #    help_text = "Hier Bemerkung zum Preis eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Ausflugspaketpreise bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return 'Preis ' + str(self.ausflugspaket_id) +  ': ' + str(self.preis) + ' &euro;'

###################################
# Ausflugspakete zu Reisetagen    #
###################################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class AusflugspaketeZuReisetagen(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Zuordnung von Ausflugspaket zu Reisetag"
        verbose_name_plural = "Zuordnung von Ausflugspaketen zu Reisetagen"
        ordering = ['position']

    # Attribute
    ausflugspakete_zu_reisetagenID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reisetag_id = models.ForeignKey(
        Reisetage,
        verbose_name = "Reisetag",
        help_text = "Wählen hier Sie die Zuordnung zu einem Reisetag.",
        on_delete=models.CASCADE)
    ausflugspaket_id = models.ForeignKey(
        Ausflugspakete,
        on_delete=models.CASCADE)
    erscheint_in = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Erscheint in",
        help_text = "Bitte wählen ob Titel oder Tagesbeschreibung")
    ausflugspaket_text = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Text Ausflugspaket",
        help_text = "Bitte Text zum Ausflugspaket eingeben.")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Ausflugspakete bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        #return 'Ausflugspaket zu ' + str(self.reisetag_id) + ' (erscheint im ' + self.erscheint_in + ')'
        #return 'Ausflugspaket zu ' + re.sub(r'\W+', ' ', str(self.reisetag_id)) + ' (erscheint in Tag-' + self.erscheint_in + ')'
        return 'Ausflugspaket zu ' + re.sub(r'[^a-zA-Z0-9_ ."-]', '', str(self.reisetag_id)) + ' (erscheint in Tag-' + self.erscheint_in + ')'


#############################
# Preise zur Reise          #
#############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisepreise(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Reisepreis"
        verbose_name_plural = "Reisepreise"
        ordering = ['position']

    # Attribute
    reisepreisID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    preis_id = models.ForeignKey(
        Preis,
        verbose_name = "Bezeichnung Preis",
        help_text = "Wählen Sie hier die Art des Preises aus.",
        on_delete=models.CASCADE)
    preis = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null = True,
        verbose_name = "Preis")
    kommentar = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Bemerkung zum Preis",
        help_text = "Hier Bemerkung zum Preis eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Reisepreise bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position+1) + '. ' + str(self.preis_id) + ': ' + str(self.preis) + ' &euro;' + self.kommentar

#############################
# Detailpreise zur Reise    #
#############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class ReisepreisZusatz(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Preisdetail"
        verbose_name_plural = "Preisdetails"
        ordering = ['position']

    # Attribute
    reisepreis_zusatzID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reisepreis_id = models.ForeignKey(
        Reisepreise,
        on_delete=models.CASCADE)
    preis_id = models.ForeignKey(
        Preis,
        verbose_name = "Bezeichnung Preis",
        help_text = "Wählen Sie hier die Art des Preises aus.",
        on_delete=models.CASCADE)
    preis = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null = True,
        verbose_name = "Preisdetail")
    #kommentar = models.CharField(
    #    max_length=256,
    #    blank = True,
    #    verbose_name = "Bemerkung zum Preis",
    #    help_text = "Hier Bemerkung zum Preis eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Reisepreisdetails bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position) + '. ' + str(self.preis_id) + ': ' + str(self.preis) + ' &euro;' # + self.kommentar
