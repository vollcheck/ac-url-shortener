from django.db import models
import random
import string
from django.conf import settings

class ShortURL(models.Model):
    url = models.URLField()
    short_url = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visits_count = models.IntegerField(default=0)

    @classmethod
    def generate_short_url(cls):
        length = settings.SHORT_URL_LENGTH
        characters = string.ascii_letters + string.digits
        while True:
            short_url = ''.join(random.choice(characters) for _ in range(length))
            if not cls.objects.filter(short_url=short_url).exists():
                return short_url
