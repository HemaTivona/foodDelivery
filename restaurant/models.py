from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    rating =models.FloatField(default = 1.0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


def __str__(self):
    return self.name



