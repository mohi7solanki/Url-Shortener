from django.shortcuts import render
from .forms import UserLoginForm, UserCreateForm
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class UserLoginView(FormView):
	template_name = 'accounts/form.html'
	form_class = UserLoginForm
	success_url = '/'

	def form_invalid(self, form):
		response = super().form_invalid(form)
		return response

	def form_valid(self, form):
		self.set_success_url()
		response = super().form_valid(form)
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return response

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = 'Login'
		context['forgot'] = 'forgot'
		return context

	def set_success_url(self):
		next_url = self.request.GET.get('next')
		if next_url:
			self.success_url = next_url


class LogoutView(LoginRequiredMixin, RedirectView):
	url = '/'
	login_url = '/login'

	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, 'Logged Out successfully!')
		return super().get(request, *args, **kwargs)


class UserRegistrationView(SuccessMessageMixin, CreateView):
	template_name = 'accounts/form.html'
	form_class = UserCreateForm
	success_url = '/login'
	success_message = "Registered Succesfully! Now Please Login"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['heading'] = 'Register'
		return context



