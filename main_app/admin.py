from django.contrib import admin
# Import model
from .models import Franchise, Photo
# Register your models here.
admin.site.register(Franchise)
admin.site.register(Photo)