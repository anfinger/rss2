from django.forms import CharField, ModelForm, Textarea#, inlineformset_factory
from django.contrib.auth.models import User
from .models import Reise, Bild, Ausflugspakete, Angebot

class ReiseForm(ModelForm):
    class Meta:
        model = Reise
        fields = "__all__"
        #korrektur_bemerkung_intern  = CharField(label='Bemerkungen', widget=Textarea(attrs={'class': 'mceEditor'}))

    def clean_author(self):
        if not self.cleaned_data['autor']:
            return User()
        return self.cleaned_data['autor']

    def clean_last_modified_by(self):
        if not self.cleaned_data['zuletzt_bearbeitet_von']:
            return User()
        return self.cleaned_data['zuletzt_bearbeitet_von']

class BildForm(ModelForm):
    class Meta:
        model = Bild
        fields = "__all__"
        #korrektur_bemerkung_intern  = CharField(label='Bemerkungen', widget=Textarea(attrs={'class': 'mceEditor'}))

class AngebotForm(ModelForm):
    class Meta:
        model = Angebot
        fields = "__all__"
        #korrektur_bemerkung_intern  = CharField(label='Bemerkungen', widget=Textarea(attrs={'class': 'mceEditor'}))

class AusflugspaketeForm(ModelForm):
    class Meta:
        model = Ausflugspakete
        fields = "__all__"
