from django import forms


class ContactForm(forms.Form):
	first_name = forms.CharField(max_length = 50, label='Prénom')
	last_name = forms.CharField(max_length = 50, label='Nom')
	email_address = forms.EmailField(max_length = 150, label='Email')
	message = forms.CharField(widget = forms.Textarea, max_length = 2000, label='Message')
 
 