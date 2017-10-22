from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import UserRegistrationView, UserLoginView, LogoutView
# , UserLoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register$', UserRegistrationView.as_view(), name='register'),
    url(r'^login$', UserLoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^account/', include('django.contrib.auth.urls')),
    url('', include('pwa.urls')),
    url(r'^', include('shortener.urls')),
]
