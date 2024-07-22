from django.db import models


class Product(models.Model):
    asin = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    rating = models.FloatField()
    average_rating = models.FloatField()

    def __str__(self):
        return self.name