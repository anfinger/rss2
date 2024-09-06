from django.forms import ModelForm, Textarea, Select, NumberInput, TextInput, EmailInput
from .models import Aktuelles, Contact, Buchungsanfrage

class AktuellesForm(ModelForm):

    class Meta:
        model = Aktuelles
        fields = ('title', 'text',)

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('anrede', 'name', 'email', 'telefon', 'nachricht')
        widgets = {
		'anrede': Select(attrs={
			'id': 'select-0c8e',
			'name': 'select',
			'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
		}),
		'name': TextInput(attrs={
			'id': 'name-350a',
                        'placeholder': 'Wie lautet Ihr Name?*',
                        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-whitea',
                        'required': 'True'
		}),
                'email': EmailInput(attrs={
                        'id': 'email-dd79',
                        'placeholder': 'Geben sie eine gueltige E-Mail-Adresse an*',
                        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-whitea',
                        'required': 'True'
                }),
		'telefon': NumberInput(attrs={
			'type': 'tel',
                        'id': 'phone-edf0',
                        'name': 'phone',
                        'placeholder': 'Ihre Telefonnummer fuer einen Rueckruf',
                        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white'
		}),
                'nachricht': Textarea(attrs={
                        'id': 'message-dccd',
                        'name': 'message',
                        'placeholder': 'Geben Sie Ihre Nachricht ein*',
                        'rows': '4',
                        'cols': '50',
                        'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white',
                        'required': 'True'
                }),
	}

class BuchungsanfrageForm(ModelForm):
    class Meta:
        model = Buchungsanfrage
        fields = ('reise', 'datum', 'name', 'strasse', 'hausnummer', 'plz', 'wohnort', 'email', 'telefon', 'nachricht')
        widgets = {
                'reise': TextInput(attrs={
                        'id': 'input_reise',
                        'placeholder': 'Reiseziel*',
                        'name': 'reise',
                        'value': '',
                        'class': 'u-input u-input-rectangle u-palette-5-light-3',
                        'required': '',
                        'readonly': ''
                }),
                'datum': TextInput(attrs={
                        'id': 'input_reisedatum',
                        'placeholder': 'Reisedatum*',
                        'name': 'reisedatum',
                        'value': '',
                        'class': 'u-input u-input-rectangle u-palette-5-light-3',
                        'required': '',
                        'readonly': ''
                }),
                'name': TextInput(attrs={
                        'id': 'input_name',
                        'placeholder': 'Geben Sie Ihren Namen ein*',
                        'name': 'name',
                        'value': '',
                        'class': 'u-input u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
                'plz': TextInput(attrs={
                        'id': 'input_plz',
                        'inputmode': 'numeric',
                        'pattern': '[0-9]{5}',
                        'placeholder': 'PLZ*',
                        'name': 'plz',
                        'value': '',
                        'class': 'u-input-4 u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
                'wohnort': TextInput(attrs={
                        'id': 'input_wohnort',
                        'placeholder': 'Wohnort*',
                        'name': 'wohnort',
                        'value': '',
                        'class': 'u-input-5 u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
                'strasse': TextInput(attrs={
                        'id': 'input_strasse',
                        'placeholder': 'Strasse*',
                        'name': 'strasse',
                        'value': '',
                        'class': 'u-input-2 u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
                'hausnummer': TextInput(attrs={
                        'id': 'input_hausnummer',
                        'placeholder': 'Hausnummer*',
                        'name': 'hausnummer',
                        'value': '',
                        'class': 'u-input-3 u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
                'email': EmailInput(attrs={
                        'id': 'input_email',
                        'placeholder': 'Email-Adresse*',
                        'name': 'email',
                        'value': '',
                        'class': 'u-input u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
                'telefon': NumberInput(attrs={
                        'type': 'tel',
                        'id': 'input_telefon',
                        'name': 'telefon',
                        'value': '',
                        'placeholder': 'Telefonnummer',
                        'class': 'u-input u-input-rectangle u-palette-5-light-3'
                }),
                'nachricht': Textarea(attrs={
                        'id': 'input_nachricht',
                        'placeholder': 'Geben Sie Ihre Nachricht ein*',
                        'name': 'nachricht',
                        'value': '',
                        'rows': '2',
                        'cols': '50',
                        'class': 'u-input u-input-rectangle u-palette-5-light-3',
                        'required': 'True'
                }),
        }

	def clean(self):

		cleaned_data = super().clean()

		telefon = cleaned_data.get("telefon")
		email = cleaned_data.get("email")

		if not (telefon or email):
			raise forms.ValidationError(
				"Sie muessen eine Email-Addresse oder Telefonnummer angeben!"
			)
