from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

# Create your models here.

class Aktuelles(models.Model):
    class Meta:
	    verbose_name_plural = "Aktuelles"

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Author')

    title = models.CharField(max_length=200)
    text = models.TextField()
    reiselink = models.URLField(
        blank = True,
        default = '',
        verbose_name = "Reiselink",
        help_text="Geben Sie hier einen Reiselink an."
    )
    reiselinktitle = models.CharField(
        max_length=200,
        blank = True,
        default = '',
        verbose_name = "Reiselinktitel",
        help_text="Geben Sie hier einen Reiselinktitel an."
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Contact(models.Model):

    FRAU = 'FR'
    HERR = 'HR'
    FIRMA = 'FI'
    KEINE = 'KA'

    ANREDE_AUSWAHL = [
        (FRAU, 'Frau'),
        (HERR, 'Herr'),
        (FIRMA, 'Firma'),
        (KEINE, 'keine Angabe'),
    ]

    anrede = models.CharField(
        max_length=2,
        choices=ANREDE_AUSWAHL,
        default=FRAU,
        verbose_name = "Anrede",
        help_text="Waehlen Sie eine Anrede."
    )

    name = models.CharField(
	max_length=255,
        verbose_name = "Name",
        help_text="Geben Sie Ihren Namen an."
    )

    email = models.EmailField(
        verbose_name = "Email",
        help_text="Geben Sie Ihre Email an."
    )

    telefon_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Die Telefonnummer muss Zahlen enthalten.")
    telefon = models.CharField(
	validators=[telefon_regex],
	max_length=17,
	blank=True,
        verbose_name = "Telefon",
        help_text="Geben Sie Ihre Telefonnummer an."
    )
    #telefon = models.CharField(max_length=17, blank=True)
    #betreff = models.CharField(max_length=255)

    nachricht = models.TextField(
        verbose_name = "Nachricht",
        help_text="Geben Sie Ihre Nachricht ein."
    )

    def __str__(self):
        return self.email

class Buchungsanfrage(models.Model):

    reise = models.CharField(
        max_length=255,
        default = "Reiseziel",
        verbose_name = "Reise",
        help_text="Reiseziel*"
    )

    datum = models.CharField(
        max_length=255,
        default = "31.12.1899",
        verbose_name = "Datum",
        help_text="Reisedatum*"
    )

    name = models.CharField(
        max_length=255,
        verbose_name = "Name",
        help_text="Geben Sie Ihren Namen an.*"
    )

    strasse = models.CharField(
        max_length=255,
        default = "",
        verbose_name = "Strasse",
        help_text="Strasse*"
    )

    hausnummer = models.CharField(
        max_length=64,
        default = "",
        verbose_name = "Hausnummer",
        help_text="Hausnummer*"
    )

    plz = models.CharField(
        max_length=10,
        default = "",
        verbose_name = "PLZ",
        help_text="PLZ*"
    )

    wohnort = models.CharField(
        max_length=255,
        default = "",
        verbose_name = "Wohnort",
        help_text="Wohnort*"
    )

    email = models.EmailField(
        verbose_name = "Email",
        default = "",
        help_text="Geben Sie eine Email-Adresse an.*"
    )

    telefon_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Die Telefonnummer muss Zahlen enthalten.")

    telefon = models.CharField(
        validators=[telefon_regex],
        max_length=17,
        blank=True,
        verbose_name = "Telefon",
        help_text="Geben Sie Ihre Telefonnummer an."
    )
    #telefon = models.CharField(max_length=17, blank=True)
    #betreff = models.CharField(max_length=255)

    nachricht = models.TextField(
        verbose_name = "Nachricht",
        help_text="Geben Sie Ihre Nachricht ein."
    )

    def __str__(self):
        return self.email
