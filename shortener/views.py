from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Shortener
from .forms import SubmitUrlForm
from django.urls import reverse


def home(request):
	if request.method == 'POST':
		form = SubmitUrlForm(request.POST)
		if form.is_valid():
			print('valid')
			pass
		else:
			print('not valid')
	else:
		form = SubmitUrlForm()
	return render(request, 'shortener/home.html', {'form': form})


def url_redirect_view(request, short_url=None):
	url = get_object_or_404(Shortener, short_url=short_url)
	url.count += 1
	url.save()
	return HttpResponseRedirect(url)
