from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import UserRegistrationView, UserLoginView, LogoutView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register$', UserRegistrationView.as_view(), name='register'),
    url(r'^login$', UserLoginView.as_view(), name='loginUrl'),
    url(r'^logout$', LogoutView.as_view(), name='logoutUrl'),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url('', include('pwa.urls')),
    url(r'^', include('shortener.urls')),
]