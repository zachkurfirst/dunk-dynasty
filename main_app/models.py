from django.db import models
from django.urls import reverse
# Import the User
from django.contrib.auth.models import User

# Create your models here.
class Franchise(models.Model):
    city = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    motto = models.CharField(max_length=100)
    established = models.DateField(auto_now_add=True)
    # adds user_id to FK column
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.city} {self.name}"

    # redirect when creating and updating a franchise
    def get_absolute_url(self):
        return reverse('franchises_detail', kwargs={
            'franchise_id': self.id
        })

# 1:1 -> Franchise:Photo
class Photo(models.Model):
    url = models.CharField(max_length=200)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    # franchise = models.OneToOneField(Franchise, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        # more efficient to use franchise_id since it is part of Photo object
        # don't have to do separate db hit (as we would in self.franchise.name)
        return f"Photo for franchise_id: {self.franchise_id} at {self.url}"

# 1:M -> Franchise:Player
class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=3, null=True)
    height_feet = models.IntegerField(null=True)
    height_inches = models.IntegerField(null=True)
    weight_pounds = models.IntegerField(null=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} on franchise_id: {self.franchise_id}"