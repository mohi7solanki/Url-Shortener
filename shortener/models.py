from django.db import models
from.utils import create_short_url
from django.conf import settings


class ShortenerManager(models.Manager):
	def all(self, *args, **kwargs):
		query_set = super(ShortenerManager, self).all(*args, **kwargs).filter(active=True)
		return query_set



class Shortener(models.Model):
	url = models.URLField(max_length=2048)
	short_url = models.CharField(max_length=20, unique=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	count = models.IntegerField(default=0)
	end_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	active = models.BooleanField(default=True)
	objects = ShortenerManager()

	def save(self, *args, **kwargs):
		if self.short_url is None or self.short_url == "":
			self.short_url = create_short_url(self)
		super(Shortener, self).save(*args, **kwargs)


	def __str__(self):
		return self.url


	def get_full_url(self):
		return 'http://localhost:8000/{}'.format(self.short_url)
