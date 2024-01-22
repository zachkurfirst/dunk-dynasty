from django.forms import ModelForm
from .models import Player

class SearchForm(ModelForm):
    class Meta:
        model = Player
        fields = ['first_name']

class AddPlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['id']
    