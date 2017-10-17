from django.db import models
from.utils import create_short_url



class ShortenerManager(models.Manager):
	def all(self, *args, **kwargs):
		query_set = super().all(*args, **kwargs).filter(active=True)
		return query_set



class Shortener(models.Model):
	url = models.URLField(max_length=250)
	short_url = models.CharField(max_length=15, unique=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	count = models.IntegerField(default=0)
	active = models.BooleanField(default=True)
	objects = ShortenerManager()

	def save(self, *args, **kwargs):
		if self.short_url is None or self.short_url == "":
			self.short_url = create_short_url(self)
		super().save(*args, **kwargs)


	def __str__(self):
		return self.url


	def get_full_url(self):
		return 'http://www.slim.co:8000/{}'.format(self.short_url)