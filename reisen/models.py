# -*- coding: utf8 -*-

from django.utils import html
from django.contrib import admin
from django.utils import timezone
from django.db import models
import django.utils.encoding
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
import re
import uuid
from django.core.validators import MinValueValidator #, MaxValueValidator
import exiftool
import os
import glob

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
    ('a', 'archiviert')
)

#KATALOG_CHOICES = (
#    ('w', 'Winterkatalog'),
#    ('s', 'Sommerkatalog'),
#    ('a', 'Winter- und Sommerkatalog'),
#    ('n', 'nicht zugeordnet'),
#)

# genauen speicherort ranhängen
def get_path(instance, filename):
  #return 'kataloge/%s/%s' % (instance.katalog_id__titel, filename)
  return 'kataloge/%s/%s' % (re.sub(r'[^a-zA-Z0-9_-]', '', str(instance.katalog_id)), filename)

################
# Bildanbieter #
################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Bildanbieter(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Bildanbieter"
        verbose_name_plural = "Bildanbieter"

    # Attribute
    bildanbieterID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    bildanbieter = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Bildanbieter",
        help_text = "Wählen Sie den Bildanbieter.")

    # bildanbieter Text als Rückgabestring
    def __str__(self):
        return self.bildanbieter

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
    bildanbieter_id = models.ForeignKey(
        Bildanbieter,
        blank = True,
        null = True,
        on_delete=models.CASCADE)
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
    bildnummer = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Bildnummer",
        help_text = "Geben Sie hier die Bildnummer des Anbieters ein.")
    kommentar = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Kommentar",
        help_text = "Geben Sie hier einen Kommentar ein.")
    copyright = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Copyright",
        help_text = "Geben Sie hier den Copyrighttext ein, der auf dem Bild zu erscheinen hat.")
    url = models.URLField(
        max_length=200,
        blank = True,
        default = '',
        verbose_name = "URL",
        help_text = "Geben Sie hier die URL ein.")

    # Bildtitel als Rückgabestring
    def __str__(self):
        return self.titel #+ ' ID: ' + str(self.bildID)

    def infos(self):
        dir_path = r'/home/rss/public_html/rss2/media/%s' % (self.bild)
        file = glob.glob(dir_path)
        keywordsString = ""
        try:
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata_batch(file)
            for d in metadata:
                # Titel
                if "XMP:Title" in d:
                    if isinstance(d["XMP:Title"], int):
                        titel = str(d["XMP:Title"])
                    else:
                        titel = d["XMP:Title"].encode('utf-8')
                elif "IPTC:ObjectName" in d:
                    if isinstance(d["IPTC:ObjectName"], int):
                        titel = str(d["IPTC:ObjectName"])
                    else:
                        titel = d["IPTC:ObjectName"].encode('utf-8')
                elif "Photoshop:SlicesGroupName" in d:
                    if isinstance(d["Photoshop:SlicesGroupName"], int):
                        titel = str(d["Photoshop:SlicesGroupName"])
                    else:
                        titel = d["Photoshop:SlicesGroupName"].encode('utf-8')
                else:
                    titel = str("")
                # Beschreibung
                if "IPTC:Caption-Abstract" in d:
                    if isinstance(d["IPTC:Caption-Abstract"], int):
                        beschreibung = str(d["IPTC:Caption-Abstract"])
                    else:
                        beschreibung = d["IPTC:Caption-Abstract"].encode('utf-8')
                elif "EXIF:ImageDescription" in d:
                    if isinstance(d["EXIF:ImageDescription"], int):
                        beschreibung = str(d["EXIF:ImageDescription"])
                    else:
                        beschreibung = d["EXIF:ImageDescription"].encode('utf-8')
                elif "XMP:Description" in d:
                    if isinstance(d["XMP:Description"], int):
                        beschreibung = str(d["XMP:Description"])
                    else:
                        beschreibung = d["XMP:Description"].encode('utf-8')
                else:
                    beschreibung = str("")
                # Keywords
                if "XMP:Subject" in d:
                    keywords = d["XMP:Subject"]
                elif "IPTC:Keywords" in d:
                    keywords = d["IPTC:Keywords"]
                else:
                    keywords = str("")
                # IDURL
                if "JUMBF:Url" in d:
                    if isinstance(d["JUMBF:Url"], int):
                        bildIDURL = str(d["JUMBF:Url"])
                    else:
                        bildIDURL = d["JUMBF:Url"].encode('utf-8')
                else:
                    bildIDURL = str("")
                # ID
                if "XMP:Source" in d:
                    if isinstance(d["XMP:Source"], int):
                        bildID = str(d["XMP:Source"])
                    else:
                        bildID = d["XMP:Source"].encode('utf-8')
                elif "IPTC:Source" in d:
                    if isinstance(d["IPTC:Source"], int):
                        bildID = str(d["IPTC:Source"])
                    else:
                        bildID = d["IPTC:Source"].encode('utf-8')
                else:
                    bildID = str("")
            # keywords in String umwandeln
            for index, keyword in enumerate(keywords):
                if index < 1:
                    if isinstance(keyword, int):
                        keywordsString = keywordsString + str(keyword)
                    else:
                        keywordsString = keywordsString + keyword.encode('utf-8')
                else:
                    if isinstance(keyword, int):
                        keywordsString = keywordsString + ", " + str(keyword)
                    else:
                        keywordsString = keywordsString + ", " + keyword.encode('utf-8')
            # Rückgabestring
            informationen = titel + r"<br><br>" + beschreibung + r"<br><br>" + keywordsString + r'<br><br><a href ="' + bildIDURL + r'">' + bildIDURL + r'</a><br><br>' + bildID
            return html.mark_safe(informationen)
        except Exception as inst:
	    return html.mark_safe(inst)

    def vorschau(self):
        path = os.path.split(str(self.bild))[0]
        filename = os.path.split(str(self.bild))[1]
	#return html.mark_safe('<img src="/media/%sthumbnails/thumbnail_%s" width="300" />' % (os.path.split(str(self.bild))[0], os.path.split(str(self.bild))[1]))
	#return html.mark_safe('<img src="/media/%s/thumbnails/thumbnail_%s" />' % (path, filename))
	return html.mark_safe('<a href="/media/%s"><img src="/media/%s/thumbnails/thumbnail_%s" /></a>' % (self.bild, path, filename))
	#return html.mark_safe('<img src="/media/%s" width="300" />' % (self.bild))
#	return html.mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
#        	url = self.url,
#		width = self.width,
#		height = self.height,
#	)
#    )

    #vorschau.short_description = 'Vorschau'
    #vorschau.allow_tags = True

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

############################
# Auftragsbestaetigung     #
############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Auftragsbestaetigung(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Auftragsbestätigung"
        verbose_name_plural = "Auftragsbestätigungen"

    # Attribute
    auftragsbestaetigungID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    auftragsbestaetigung = models.FileField(upload_to = 'auftragsbestaetigungen', blank = True, default = '')#, default = 'images/None/no-img.jpg')
    titel = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Titel Auftragsbestätigung",
        help_text = "Geben Sie hier den Titel der Auftragsbestätigung ein.")

    # Titel als Rückgabestring
    def __str__(self):
        return self.titel + ' ID: ' + str(self.auftragsbestaetigungID)


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
        ordering = ['hinweis']

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
        ordering = ['kategorie']

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
        ordering = ['name']

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
        ordering = ['titel']

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

    # Auswahlmöglichkeiten Veranstalter
    VERANSTALTER_CHOICES = (
        ('RS', 'Reiseservice Schwerin'),
        ('SH', 'Sewert Reisen'),
        ('RT', 'R&T Reisen Ludwigslust'),
    )

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
    veranstalter = models.CharField(
        max_length=2,
        choices=VERANSTALTER_CHOICES,
        default='RS',
        verbose_name = "Veranstalter",
        help_text = "Veranstalter")
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
    sonstigeReisebeschreibung_titel = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Zusatztitel",
        help_text = "Titel zu sonstige Reisebeschreibungen, falls nötig. (etwa 40-70 Zeichen)")
    leistungen_kopfkommentar = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Kopfkommentar zu Leistungen, falls nötig. (etwa 40-70 Zeichen)")
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
    zusatzleistungen_fuss_kommentar = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Abschließender Fuss-Kommentar für alle zusätzliche Leistungen, falls nötig. (etwa 40-70 Zeichen)")
    korrektur_bemerkung_intern  = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Korrekturfeld",
        help_text="Wird nur intern dargestellt und dient Notizen die Reise betreffend, Korrekturbemerkungen, etc."
    )
    individualbuchbar = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Hinweis auf buchbaren individuellen Aufenthalt.",
        help_text="Wird nur bei Reisen mit buchbarem individuellen Aufenthalt benötigt."
    )
    zubucher = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name = "Text Zubucherreise, falls nötig. (etwa 40-70 Zeichen)"
    )
    individualreisetitel = models.CharField(
        max_length=256,
        blank = True,
        default = '',
        verbose_name = "Titel für Individualreisen, falls nötig.",
        help_text="Wird nur bei Reisen mit buchbarem individuellen Aufenthalt benötigt."
    )
    individualreisetext = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Text für Individualreisen, falls nötig.",
        help_text="Wird nur bei Reisen mit buchbarem individuellen Aufenthalt benötigt."
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
    neu = models.BooleanField(
        default = None,
        verbose_name = "Neue Reise",
        help_text = "Neue Reise markieren."
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

#    @permalink
#    def get_absolute_url(self):
#        return ('reise', (), {
#            'slug': self.slug,
#            'reiseID': self.reiseID,
#        })

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
    tagnummertext = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name="alternativer Text für Tagnummer",
        help_text="Geben Sie hier einen alternativen Text zur Nummerierung der Tage ein. (max. 128 Zeichen)")
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

##############################
# sonstige Reisebeschreibung #
##############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reisebeschreibung(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "sonstige Reisebeschreibung"
        verbose_name_plural = "sonstige Reisebeschreibungen"
        ordering = ['position']

    # Attribute
    reisebeschreibungID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge bei der Darstellung")
    titel = models.CharField(
        max_length=128,
        blank = True,
        default = '',
        verbose_name="Titel Reisebeschreibung",
        help_text="Geben Sie hier den Titel der Reisebeschreibung ein. (max. 70 Zeichen)")
    beschreibung = models.TextField(
        verbose_name = "Beschreibung",
        blank = True,
        default = '',
        help_text="Geben Sie hier die Reisebeschreibung ein. (Die max. Anzahl Zeichen ist abhängig von Anzahl der Tage und Bilder je Reise etc. (etwa800))")
    zusatz = models.TextField(
        blank = True,
        default = '',
        verbose_name = "Zusatz zur Beschreibung",
        help_text="Geben Sie hier zusätzliche Informationen zur Reisebeschreibung ein. (Tipps, etc.)")

    # Titel Tagesbeschreibung als Rückgabestring
    def __str__(self):
        return self.titel


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

###########################
# Abfahrtszeiten, Ankunft #
###########################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Abfahrtszeiten(models.Model):

    # Auswahlmöglichkeiten Zeiten
    ORT_CHOICES = (
        ('HBF', 'Schwerin Hauptbahnhof'),
        ('VSB', 'von-Stauffenberg-Str.'),
        ('GAR', 'Gartenstadt'),
        ('WIS', 'ZOB Wismar'),
        ('ROG', 'Gadebusch Roggendorfer Str.'),
        ('ANK', 'Ankunft zurück in Schwerin'),
    )

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Abfahrtszeit/Ankunft"
        verbose_name_plural = "Abfahrtszeit/Ankunft"
        ordering = ['position']

    # Attribute
    abfahrtszeitID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        #related_name = '+',
        on_delete=models.CASCADE)
    ort = models.CharField(
        max_length=3,
        choices=ORT_CHOICES,
        default='HBF',
        verbose_name = "Abfahrtsort/Ankunft",
        help_text = "Abfahrtsort/Ankunft")
    kommentar = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Kommentar",
        help_text = "Kommentar/Hinweise")
    zeit = models.TimeField(
        blank = True,
        default = '',
        null = False,
        verbose_name = "Abfahrts-/Ankunftszeit")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Zeiten bei der Darstellung")

    # Abfahrtszeit als Rückgabestring
    def __str__(self):
        return str(self.zeit)

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
        max_length=256,
        blank = True,
        verbose_name = "Leistung",
        help_text = "einzelne Leistung zur Reise")
    nichtindividual = models.BooleanField(
        default = None,
        verbose_name = "Gilt nicht für Individualreise.",
        help_text = "Leistung gilt nicht für Individualreise."
    )
    leistungkurhotel = models.BooleanField(
        default = None,
        verbose_name = "Nicht allgemeine Leistung. Gilt nur für Kurhotel.",
        help_text = "Nicht allgemeine Leistung. Gilt nur für Kurhotel."
    )
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
        ordering = ['datum_bis']

    # Attribute
    fruehbucherrabattID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id  = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    rabattbezeichnung = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Rabattbezeichnung",
        help_text = "Bezeichnung des Rabatts")
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
    # wenn anzahl der seiten im katalog = 0, dann gibt es mehrere reisen auf einer seite -> deshalb position zum ordnen
    position_auf_seite = models.PositiveSmallIntegerField(
        null = True,
        default = 0,
        verbose_name = "Position auf der Seite",
        help_text = "Position zur Sortierung falls mehrere Reisen auf einer Seite")
    #katalog_pdf = FileBrowseField(max_length=200, directory="kataloge/", extensions=[".pdf"], blank=True, null=True)#, default = 'images/None/no-img.jpg')
    katalog_pdf = models.FileField(upload_to = get_path, blank = True, default = '')#, default = 'images/None/no-img.jpg')
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
        verbose_name = "Bild zur Reise"
        verbose_name_plural = "Bilder zur Reise"
        ordering = ['position']

    # Attribute
    reisebildID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        verbose_name = "Reise",
        help_text="Wählen Sie eine Reise.",
        on_delete=models.CASCADE)
    bild_id = models.ForeignKey(
        Bild,
        verbose_name = "Bild",
        help_text="Wählen Sie ein Bild.",
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
        help_text = "Geben Sie an ob das Bild etwa im Katalog, Web, Katalogvorstellung, Reisetagebuch, etc. veröffentlicht werden soll. (kommaseparierte Liste)")
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

#######################################
# Auftragsbestaetigung zur Reise      #
#######################################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Reiseauftragsbestaetigungen(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Auftragsbestätigung"
        verbose_name_plural = "Auftragsbestätigungen"
        ordering = ['position']

    # Attribute
    reiseauftragsbestaetigungID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reise_id = models.ForeignKey(
        Reise,
        on_delete=models.CASCADE)
    auftragsbestaetigung_id = models.ForeignKey(
        Auftragsbestaetigung,
        on_delete=models.CASCADE)
    titel = models.TextField(
        blank = True,
        default = '',
        verbose_name = "optionaler Titel",
        help_text="Geben Sie hier einen optionalen Titel ein. (Überschreibt Standard Titel)")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge bei der Darstellung")

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

#############################
# Zielregionen zur Reise    #
#############################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Bildzielregionen(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Zielregion"
        verbose_name_plural = "Zielregionen"
        ordering = ['position']

    # Attribute
    bildzielregionenID = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    bild_id = models.ForeignKey(
        Bild,
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


#############################################
# Ausflugspakete/Zusatzleistungen zur Reise #
#############################################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Ausflugspakete(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Ausflugspaket/Zusatzleistung"
        verbose_name_plural = "Ausflugspakete/Zusatzleistungen"
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
        verbose_name = "Titel",
        help_text = "Hier den Titel eingeben")
    kommentar_titel = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Titelkommentar",
        help_text = "Hier den Titelkommentar eingeben")
    kommentar = models.CharField(
        max_length=256,
        blank = True,
        verbose_name = "Kommentar",
        help_text = "Hier den Kommentar eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "position",
        help_text = "Position zur Bestimmung der Reihenfolge bei der Darstellung")

    # Leistung Text als Rückgabestring
    def __str__(self):
        return self.titel

#################################################################################
# Leistungen zu Ausflugspaket                                                   #
# Wenn keine Leistungen vorhanden dann ist es kein AP sonder Zusatzleistung !!! #
#################################################################################
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

############################################
# Preise zu Ausflugspaket/Zusatzleistung   #
############################################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class Ausflugspaketpreise(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Preis Ausflugspaket/Zusatzleistung"
        verbose_name_plural = "Preise Ausflugspaket/Zusatzleistung"
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
        blank = True,
        verbose_name = "Preis")
    #kommentar = models.CharField(
    #    max_length=256,
    #    blank = True,
    #    verbose_name = "Bemerkung zum Preis",
    #    help_text = "Hier Bemerkung zum Preis eingeben")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Preise bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        #return 'Preis ' + str(self.ausflugspaket_id) +  ': ' + str(self.preis) + ' &euro;'
        return 'Preis ' + re.sub(r'[^a-zA-Z0-9_ ."-]', '', str(self.ausflugspaket_id)) + ': ' + str(self.preis) + ' &euro;'

####################################################
# Ausflugspakete/Zusatzleistungen zu Reisetagen    #
####################################################
@python_2_unicode_compatible # For Python 3.4 and 2.7
class AusflugspaketeZuReisetagen(models.Model):

    # Titel für das Admin Backend
    class Meta:
        verbose_name = "Zuordnung zu Reisetag"
        verbose_name_plural = "Zuordnung zu Reisetagen"
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
        verbose_name = "Text Ausflugspaket/Zusatzleistung",
        help_text = "Bitte Text zum Ausflugspaket/Zusatzleistung eingeben.")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Ausflugspakete/Zusatzleistungen bei der Darstellung")

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
    markierung = models.CharField(
        max_length=20,
        blank = True,
        verbose_name = "Markierung",
        help_text = "Markierung z.B. für terminspezifische Preise (*)")
    position = models.PositiveSmallIntegerField(
        null = True,
        verbose_name = "Position",
        help_text = "Position zur Bestimmung der Reihenfolge der Reisepreise bei der Darstellung")

    # titel Text als Rückgabestring
    def __str__(self):
        return str(self.position+1) + '. ' + re.sub(r'[^a-zA-Z0-9_ ."-]', '', str(self.preis_id)) + ': ' + str(self.preis) + ' &euro;'

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
        # return str(self.position) + '. ' + str(self.preis_id) + ': ' + str(self.preis) + ' &euro;' # + self.kommentar
        return str(self.position+1) + '. ' + re.sub(r'[^a-zA-Z0-9_ ."-]', '', str(self.preis_id)) + ': ' + str(self.preis) + ' &euro;'
