from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('franchises/all/', views.franchises_index, name='franchises_index'),
    path('franchises/', views.franchises_my_index, name='franchises_my_index'),
    path('franchises/<int:franchise_id>/', views.franchises_detail, name='franchises_detail'),
    path('franchises/create/', views.FranchiseCreate.as_view(), name='franchises_create'),
    path('franchises/<int:pk>/update/', views.FranchiseUpdate.as_view(), name='franchises_update'),
    path('franchises/<int:pk>/delete/', views.FranchiseDelete.as_view(), name='franchises_delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('franchises/<int:franchise_id>/add_photo/', views.add_photo, name='add_photo'),
    path('franchises/<int:franchise_id>/search/', views.players_search, name='players_search'),
    path('franchises/<int:franchise_id>/get_players/', views.get_players, name='get_players'),
    path('franchises/<int:franchise_id>/add_player/', views.add_player, name='add_player'),
    path('franchises/<int:franchise_id>/player/<int:player_id>/', views.player_cut, name='player_cut'),
]