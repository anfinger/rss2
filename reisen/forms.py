from django.forms import CharField, ModelForm, Textarea#, inlineformset_factory
from django.contrib.auth.models import User
from .models import Reise, Bild, Ausflugspakete, Angebot, Zielregion, Hinweis, Kategorie, Preis

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
#    class ReiseauswahlFeld(forms.ModelChoiceField):
#        def label_from_instance(self, obj):
#            return "Category: {}".format(obj.name)

class AngebotForm(ModelForm):
    class Meta:
        model = Angebot
        fields = "__all__"
        #korrektur_bemerkung_intern  = CharField(label='Bemerkungen', widget=Textarea(attrs={'class': 'mceEditor'}))

class AusflugspaketeForm(ModelForm):
    class Meta:
        model = Ausflugspakete
        fields = "__all__"

class ZielregionForm(ModelForm):
    class Meta:
        model = Zielregion
        fields = "__all__"

class HinweisForm(ModelForm):
    class Meta:
        model = Hinweis
        fields = "__all__"

class KategorieForm(ModelForm):
    class Meta:
        model = Kategorie
        fields = "__all__"

class PreisForm(ModelForm):
    class Meta:
        model = Preis
        fields = "__all__"

