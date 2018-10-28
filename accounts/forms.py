from django.contrib.auth.models import User
from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}),required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}), required=True)

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


class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		fields =  ('username', 'email', 'password1', 'password2')
		model = User

	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
		self.fields['password1'].help_text = None
		self.fields['password2'].help_text = None
		self.fields['email'].widget.attrs['placeholder'] = 'Enter your e-mail'
		self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
		self.fields['password1'].widget.attrs['placeholder'] = 'Enter a strong password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('That email address is already registered!')
		return email
