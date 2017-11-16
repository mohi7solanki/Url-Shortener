from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Shortener
from .forms import SubmitUrlForm
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import FormView, DeleteView
from django.http import JsonResponse
from django.db.models import F
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.base import RedirectView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.validators import URLValidator


class HomeView(View):
	template_name = 'shortener/home.html'
	
	def get(self, request):
		form = SubmitUrlForm()
		context = {'form': form }
		return render(request, self.template_name, context)

	def post(self, request):
		form = SubmitUrlForm(request.POST)
		if form.is_valid():
			url = form.save(commit=False)
			user = None
			if request.user.is_authenticated():
				user = request.user
			url.end_user = user
			url.save()
			full_url = Shortener.objects.latest('created_at').get_full_url()
			data = {
			    'message': full_url
			}
			return JsonResponse(data)
		return JsonResponse(form.errors, status=400)



class ProfileView(LoginRequiredMixin, ListView):
	login_url = '/login'
	context_object_name = 'urls'
	template_name = 'shortener/profile.html'

	def get_queryset(self):
		return Shortener.objects.filter(end_user=self.request.user).order_by('-created_at')


class AboutView(TemplateView):
    template_name = 'shortener/about.html'


class UrlRedirectView(RedirectView):
	
	def get_redirect_url(self, short_url):
		url = get_object_or_404(Shortener, short_url=short_url)
		url.count = F('count') + 1
		url.save()
		return url


class UrlDeleteView(LoginRequiredMixin, DeleteView):
	login_url = '/login'
	model = Shortener
	template_name = 'shortener/confirm_delete.html'
	success_url = '/profile'

	def get_object(self, queryset=None):
		short_url = self.kwargs.get('short_url')
		return Shortener.objects.get(short_url=short_url)

	def get(self, request, *args, **kwargs):
		if not request.user == self.get_object().end_user:
			raise Http404
		return super().get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		messages.success(request, 'Url Deleted successfully!')
		return super().post(request, *args, **kwargs)


def fast_track_service(request):
	fast_track_url = request.get_full_path()[1:].replace('/?','?')
	if 'favicon.ico' in fast_track_url:
		return HttpResponse()
	if fast_track_url[-1] == '/':
		fast_track_url = fast_track_url[:-1]
	url_validate = URLValidator()
	try:
		url_validate(fast_track_url)
	except:
		fast_track_url = 'http://' + fast_track_url
		try:
			url_validate(fast_track_url)
		except:
			raise Http404
	f_url = Shortener.objects.create(url=fast_track_url)
	return render(request, 'shortener/fast_track.html', {'f_url': f_url})