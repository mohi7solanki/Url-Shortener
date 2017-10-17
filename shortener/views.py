from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Shortener
from .forms import SubmitUrlForm
from django.urls import reverse
from django.contrib import messages


def home(request):
	if request.method == 'POST':
		form = SubmitUrlForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/success')
	else:
		form = SubmitUrlForm()
	return render(request, 'shortener/home.html', {'form': form})


def url_redirect_view(request, short_url=None):
	url = get_object_or_404(Shortener, short_url=short_url)
	url.count += 1
	url.save()
	return HttpResponseRedirect(url)


def success(request):
	full_url = Shortener.objects.latest('created_at').get_full_url()
	return render(request, 'shortener/success.html', {'url' :full_url})


