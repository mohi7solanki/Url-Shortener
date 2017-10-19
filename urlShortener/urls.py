from django.conf.urls import url, include
from django.contrib import admin
from accounts.views import UserRegistrationView, UserLoginView, LogoutView
# , UserLoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register$', UserRegistrationView.as_view(), name='register'),
    url(r'^login$', UserLoginView.as_view(), name='register'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('shortener.urls')),
]
