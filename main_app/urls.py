from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('franchises/', views.franchises_index, name='franchises_index'),
    path('franchises/<int:franchise_id>/', views.franchises_detail, name='franchises_detail'),
]