from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Shortener
from .forms import SubmitUrlForm
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from django.http import JsonResponse
from django.db.models import F


# def home(request):
# 	if request.method == 'POST':
# 		form = SubmitUrlForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			return HttpResponseRedirect('/success')
# 	else:
# 		form = SubmitUrlForm()
# 	return render(request, 'shortener/home.html', {'form': form})


class HomeView(FormView):
	template_name = 'shortener/home.html'
	form_class = SubmitUrlForm
	success_url = '/success/'

	def form_invalid(self, form):
		response = super().form_invalid(form)
		if self.request.is_ajax():
		    return JsonResponse(form.errors, status=400)
		else:
		    return response

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		username = None
		if self.request.user.is_authenticated():
			username = self.request.user.username
		context['username'] = username
		return context


	def form_valid(self, form):
		response = super().form_valid(form)
		if self.request.is_ajax():
		    form.save()
		    full_url = Shortener.objects.latest('created_at').get_full_url()
		    data = {
		        'message': full_url
		    }
		    return JsonResponse(data)
		else:
		    return response

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		username = None
		if self.request.user.is_authenticated():
			username = self.request.user.username
		context['username'] = username
		return context



def url_redirect_view(request, short_url=None):
	url = get_object_or_404(Shortener, short_url=short_url)
	url.count = F('count') + 1
	url.save()
	return HttpResponseRedirect(url)




