from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('franchises/', views.franchises_index, name='franchises_index'),
    path('franchises/<int:franchise_id>/', views.franchises_detail, name='franchises_detail'),
    path('franchises/create/', views.FranchiseCreate.as_view(), name='franchises_create'),
    # use pk for class-based views
    path('franchises/<int:pk>/update/', views.FranchiseUpdate.as_view(), name='franchises_update'),
    path('franchises/<int:pk>/delete/', views.FranchiseDelete.as_view(), name='franchises_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]