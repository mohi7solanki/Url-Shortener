from django.contrib.auth.models import User
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(widget=forms.PasswordInput, required=True)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		exists = User.objects.filter(username=username).exists()
		if not exists:
			raise forms.ValidationError("This '{}' user does not exist!".format(username))
		return username

	def clean_password(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		exists = User.objects.filter(username=username).exists()
		user = authenticate(username=username, password=password)
		if exists and not user:
			raise forms.ValidationError("Invalid Password")
		return password



class UserForm(forms.ModelForm):
	email = forms.EmailField(required=True, validators=[EmailValidator])
	username = forms.CharField(help_text=None)
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password =forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
		'username',
		'email',
		'password',
		]


	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('confirm_password')
		if len(password2) > 6:
			if password != password2:
				raise forms.ValidationError("Your Password doesn't match!")
		return password2

	def clean_password(self):
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('confirm_password')
		if len(password) < 6:
			raise forms.ValidationError("Password should contain atleast 6 character!")
		return password