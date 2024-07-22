from django.db import models

from apps.core.models import BaseModel


class Product(BaseModel):
    asin = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    rating = models.FloatField()
    average_rating = models.FloatField()

    def __str__(self):
        return self.name