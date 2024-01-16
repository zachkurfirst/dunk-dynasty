from django.db import models
from django.urls import reverse

# Create your models here.
class Franchise(models.Model):
    city = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    motto = models.CharField(max_length=100)
    established = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} {self.name}"

    def get_absolute_url(self):
        return reverse('franchises_detail', kwargs={
            'franchise_id': self.id
        })
