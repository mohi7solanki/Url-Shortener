from django.shortcuts import render
from .forms import UserForm, UserLoginForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


class UserLoginView(FormView):
	template_name = 'accounts/form.html'
	form_class = UserLoginForm
	success_url = '/'

	def form_invalid(self, form):
		response = super().form_invalid(form)
		return response

	def form_valid(self, form):
		response = super().form_valid(form)
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return response


class UserRegistrationView(FormView):
	template_name = 'accounts/form.html'
	form_class = UserForm
	success_url = '/'

	def form_invalid(self, form):
		response = super().form_invalid(form)
		return response

	def form_valid(self, form):
		response = super().form_valid(form)
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		user = authenticate(username=user.username, password=password)
		login(self.request, user)
		return response