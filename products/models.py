from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)
    unit_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    is_multiple = models.IntegerField(default=1)

    def __str__(self):
        return self.name
