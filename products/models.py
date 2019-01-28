from django.db import models

from ordermaker.utils import upload_image_path


def upload_to(instance, filename):
    """
    Obtain the local of file with the new file name
    """
    return upload_image_path(filename, 'products')


class Product(models.Model):
    name = models.CharField(max_length=120)
    unit_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.0)
    is_multiple = models.IntegerField(default=1)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.name
