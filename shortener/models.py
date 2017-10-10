from django.db import models


class Shortener(models.Model):
	url = models.URLField(max_length=250)
	shortened_url = models.CharField(max_length=20, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.url
