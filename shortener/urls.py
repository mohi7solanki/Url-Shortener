from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.HomeView.as_view(), name='home'),
	url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
	url(r'^delete/(?P<short_url>[\w-]{3,15})/$', views.UrlDeleteView.as_view(), name='delete'),
	url(r'^about/$', views.AboutView.as_view(), name='about'),
	url(r'^(?P<short_url>[\w-]{3,15})/$', views.UrlRedirectView.as_view(), name='redirect'),
]