from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('franchises/', views.franchises_index, name='franchises_index'),
]