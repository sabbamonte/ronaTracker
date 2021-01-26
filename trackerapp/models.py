from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

class New_Post(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    timestamp = models.DateField(auto_now_add=True)
    diagnosis = models.CharField(max_length=200, default=None)
    city = models.CharField(max_length=20, default=None)
    state = models.CharField(max_length=20, default=None)
    zip = models.PositiveIntegerField(blank=False, validators=[MaxValueValidator(99950)], default=None)
    is_archived = models.BooleanField(default=False)

    def valid_zip(self):
        return self.zip != 0 and len(str(self.zip)) <= 5
    
    


