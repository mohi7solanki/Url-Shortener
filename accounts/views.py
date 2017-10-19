from django.shortcuts import render
from .forms import UserForm, UserLoginForm
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


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
		return context

	def set_success_url(self):
		next_url = self.request.GET.get('next')
		if next_url:
			self.success_url = next_url



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

	def get_context_data(self, **kwargs):
	    context = super().get_context_data(**kwargs)
	    context['heading'] = 'Register'
	    return context


def logoutView(request):
	logout(request)
	template_name = 'shortener/home.html'
	messages.success(request, 'Logged Out successfully!')
	return HttpResponseRedirect('/')