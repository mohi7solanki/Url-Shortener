from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'^(?P<short_url>[\w-]{3,15})/$', views.url_redirect_view, name='redirect'),
]