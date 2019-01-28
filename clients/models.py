from django.db import models

from ordermaker.utils import upload_image_path


def upload_to(instance, filename):
    """
    Obtain the local of file with the new file name
    """
    return upload_image_path(filename, 'clients')


class Client(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def __str__(self):
        return self.name
