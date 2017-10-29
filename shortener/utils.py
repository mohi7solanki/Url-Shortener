import random
import string


def generate_short_url(size=6, chars=string.ascii_lowercase + string.digits + string.ascii_uppercase):
	return ''.join(random.choice(chars) for _ in range(size))


def create_short_url(instance, size=6):
	short_url = generate_short_url()
	Class = instance.__class__
	duplicate = Class.objects.filter(short_url=short_url).exists()
	if duplicate:
		return create_short_url(instance)
	return short_url