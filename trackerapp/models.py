from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class New_Post(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    timestamp = models.DateField(auto_now_add=True)
    infected = models.BooleanField(default=False)
    exposed = models.BooleanField(default=False)
    healthy = models.BooleanField(default=False)

class Cities(models.Model):
    objects = models.Manager()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    zip = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(9950)])


