from django import forms

from .models import Aktuelles

class AktuellesForm(forms.ModelForm):

    class Meta:
        model = Aktuelles
        fields = ('title', 'text',)
