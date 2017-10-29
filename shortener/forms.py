from django import forms
from .models import Shortener
from django.core.validators import URLValidator


class SubmitUrlForm(forms.ModelForm):
	internal_name = ('profile', 'contact', 'disclaimer', 'sitemap.xml', 'robots.txt')

	url = forms.CharField(max_length=200,
		label='Link to shorten',
		required=False,
		)

	short_url = forms.CharField(min_length=3, max_length=15, required=False)
	
	class Meta:
		model = Shortener
		fields = [
			'url',
			'short_url',
		]
		exclude = ["end_user"]

	
	def clean_url(self):
		url = self.cleaned_data['url']
		if len(url) == 0 or url is None:
			raise forms.ValidationError("One day I'll have superpower to shorten that blank URL ;)")
		if not 'http://' in url and not 'https://' in url:
		    url = 'http://' + url
		url_validate = URLValidator()
		try:
			url_validate(url)
		except:
			raise forms.ValidationError("Please Enter a Valid URL")
		return url

	
	def clean_short_url(self):
		short_url = self.cleaned_data['short_url']
		if short_url:
			if short_url in SubmitUrlForm.internal_name:
				raise forms.ValidationError("Bummer! We love that word, Please choose another one.")
			exists = Shortener.objects.filter(short_url=short_url).exists()
			if exists:
				raise forms.ValidationError("Please Choose another short link. This '{}' already exists.".format(short_url))
		return short_url

