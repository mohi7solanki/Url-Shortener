from django import forms
from .models import Shortener
from django.core.validators import URLValidator


class SubmitUrlForm(forms.ModelForm):
	url = forms.CharField(max_length=200,
		label='Link to shorten',
		)

	short_url = forms.CharField(min_length=3, max_length=15, required=False)
	
	class Meta:
		model = Shortener
		fields = [
			'url',
			'short_url',
		]

	
	def clean_url(self):
		url = self.cleaned_data['url']
		if not 'http://' in url and not 'https://' in url:
		    url = 'http://' + url
		url_validate = URLValidator()
		try:
			url_validate(url)
		except:
			raise forms.ValidationError("Please Enter a Valid URL")
		return url

