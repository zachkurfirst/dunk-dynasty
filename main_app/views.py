import uuid
import boto3
import os
import requests
# from django.http import JsonResponse
from django.shortcuts import render, redirect
# Import for CBV
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Import for redirect
from django.urls import reverse_lazy
# Import for signup
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import for Authorization
from django.contrib.auth.decorators import login_required
# Import mixin for CBV Authorization
from django.contrib.auth.mixins import LoginRequiredMixin
# Import models
from .models import Franchise, Photo, Player
from .forms import SearchForm, AddPlayerForm

# Create your views here.

# HOME VIEW
def home(request):
    return render(request, 'home.html')

# ABOUT VIEW
def about(request):
    return render(request, 'about.html')

# FRANCHISES INDEX - ALL FRANCHISES
def franchises_index(request):
    franchises = Franchise.objects.all()
    return render(request, 'franchises/index.html', {
        'franchises': franchises
    })

# MY FRANCHISES INDEX - LOGGED IN USERS FRANCHISES
@login_required
def franchises_my_index(request):
    my_franchises = Franchise.objects.filter(user=request.user)
    if len(my_franchises) == 0:
        return redirect('franchises_create')
    else:
        return render(request, 'franchises/my_index.html', {
            'my_franchises': my_franchises
    })

# FRANCHISES DETAIL
def franchises_detail(request, franchise_id):
    franchise = Franchise.objects.get(id=franchise_id)
    return render(request, 'franchises/detail.html', {
        'franchise': franchise
    })

# FRANCHISES CREATE
class FranchiseCreate(LoginRequiredMixin, CreateView):
    model = Franchise
    fields = ['city', 'name', 'motto']

    def form_valid(self, form):
        # form.instance is the unsaved franchise object
        form.instance.user = self.request.user
        return super().form_valid(form)

# FRANCHISES UPDATE
class FranchiseUpdate(LoginRequiredMixin, UpdateView):
    model = Franchise
    fields = ['city', 'name', 'motto']

# FRANCHISES DELETE
class FranchiseDelete(LoginRequiredMixin, DeleteView):
    model = Franchise
    success_url = reverse_lazy('franchises_index')

# SIGNUP
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save user to db
            user = form.save()
            login(request, user)
            return redirect('franchises_index')
        else:
            error_message = 'Invalid sign up, please try again.'
    # Invalid POST or GET request
    form = UserCreationForm()
    context = {
        'form': form,
        'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# ADD PHOTO
@login_required
def add_photo(request, franchise_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # Need unique key for s3 (filename)
        # Keep the same file extension as uploaded file by slicing
        uniqueId = uuid.uuid4().hex[:6]
        extension = photo_file.name[photo_file.name.rfind('.'):]
        key = uniqueId + extension
        # try uploading file
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build full url
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, franchise_id=franchise_id)
            return redirect('players_search', franchise_id=franchise_id)
        except Exception as e:
            print('An error occured uploading file to S3.')
            print(e)
    return redirect('franchises_detail', franchise_id=franchise_id)

# RENDER PLAYERS SEARCH PAGE
@login_required
def players_search(request, franchise_id):
    franchise = Franchise.objects.get(id=franchise_id)
    # instantiate SearchForm to be rendered
    form = SearchForm()
    return render(request, 'franchises/search.html', {
        'franchise': franchise,
        'franchise_id': franchise_id,
        'form': form
    })

# GET PLAYERS (SEARCH RESULTS)
@login_required
def get_players(request, franchise_id):
    results = {}
    franchise = Franchise.objects.get(id=franchise_id)
    # instantiate AddPlayerForm to be rendered
    add_player_form = AddPlayerForm()
    # check if search form is submitted
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['first_name']
            endpoint = 'https://api.balldontlie.io/v1/players?per_page=10'
            token = os.environ.get('API_TOKEN_BDL')
            headers = {'Authorization': f"{token}"}
            response = requests.get(endpoint, headers=headers, params={'search': query})
            results = response.json()
    else:
        form = SearchForm()
    return render(request, 'franchises/search.html', {
        'form': form,
        'results': results,
        'franchise_id': franchise_id,
        'franchise': franchise,
        'add_player_form': add_player_form
    })

# ADD PLAYER TO FRANCHISE
@login_required
def add_player(request, franchise_id):
    if request.method == 'POST':
        player_id = request.POST.get('player-id')
        endpoint = 'https://api.balldontlie.io/v1/players/'
        token = os.environ.get('API_TOKEN_BDL')
        headers = {'Authorization': f"{token}"}
        response = requests.get(f"{endpoint}{player_id}", headers=headers)
        result = response.json()
        new_player = Player(
            id=result['data']['id'],
            first_name=result['data']['first_name'],
            last_name=result['data']['last_name'],
            position=result['data']['position'],
            height=result['data']['height'],
            weight=result['data']['weight'],
            franchise_id=franchise_id
        )
        if Player.objects.filter(id=player_id).exists():
            # player is already on a franchise
            return redirect('players_search', franchise_id=franchise_id)
        else:
            # player is available to be claimed
            new_player.save()
    return redirect('franchises_detail', franchise_id=franchise_id)

# PLAYER CUT (DELETE)
@login_required
def player_cut(request, franchise_id, player_id):
    player = Player.objects.get(id=player_id)
    player.delete()
    return redirect('franchises_detail', franchise_id=franchise_id)