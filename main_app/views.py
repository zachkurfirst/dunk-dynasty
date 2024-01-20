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

# franchises = [{'city': 'Cincinnati', 'name': 'Pythons', 'motto': 'Winning is the only option.', 'established': 'Jan 2024'}, {'city': 'Buffalo', 'name': 'Wings', 'motto': 'Buffalo built.', 'established': 'Jan 2024'}, {'city': 'Seattle', 'name': 'Swish', 'motto': 'Bringing hoops back to where it belongs.', 'established': 'Jan 2024'}]

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
@login_required # decorator takes function as input and returns a new function
def franchises_my_index(request):
    my_franchises = Franchise.objects.filter(user=request.user)
    if len(my_franchises) == 0:
        return redirect('franchises_create')
    else:
        return render(request, 'franchises/my_index.html', {
            'my_franchises': my_franchises
    })

# FRANCHISES DETAIL
# NOTE: Consider protecting detail view with decorator - for now keeping open
def franchises_detail(request, franchise_id):
    franchise = Franchise.objects.get(id=franchise_id)
    return render(request, 'franchises/detail.html', {
        'franchise': franchise
    })

# FRANCHISES CREATE
class FranchiseCreate(LoginRequiredMixin, CreateView):
    model = Franchise
    fields = ['city', 'name', 'motto']
    # no success url necessary -> references get_absolute_url from model

    # Assign logged in user (self.request.user) to newly created object
    # Save object and redirect
    def form_valid(self, form):
        # form.instance is the unsaved cat object
        form.instance.user = self.request.user
        return super().form_valid(form)

# FRANCHISES UPDATE
class FranchiseUpdate(LoginRequiredMixin, UpdateView):
    model = Franchise
    fields = ['city', 'name', 'motto']
    # no success url necessary -> references get_absolute_url from model

# FRANCHISES DELETE
class FranchiseDelete(LoginRequiredMixin, DeleteView):
    model = Franchise
    success_url = reverse_lazy('franchises_index')

# SIGNUP
def signup(request):
    error_message = ''
    if request.method == 'POST':
        # UserCreationForm is a modelform, pass in the request data
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save user to db
            user = form.save()
            login(request, user)
            return redirect('franchises_index')
        else:
            error_message = 'Invalid sign up, please try again.'
    # Invalid POST or GET request -> render signup.html with empty form
    form = UserCreationForm()
    # create a variable for the context dictionary
    context = {
        'form': form,
        'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# ADD PHOTO
def add_photo(request, franchise_id):
    # photo-file maps to 'name' attribute on <input type="file">
    # print(request.FILES)
    # print(dir(request.FILES))
    # print(Photo.objects.get(franchise_id=franchise_id))
    # if Photo.objects.get(franchise_id=franchise_id):
    #     photo = Photo.objects.get(franchise_id=franchise_id)
    #     photo.url = 
    # print(photo_file)
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
            # assign to franchise_id or franchise (if object exists)
            Photo.objects.create(url=url, franchise_id=franchise_id)
        except Exception as e:
            print('An error occured uploading file to S3.')
            print(e)
    return redirect('franchises_detail', franchise_id=franchise_id)

# RENDER PLAYERS SEARCH PAGE
def players_search(request, franchise_id):
    franchise = Franchise.objects.get(id=franchise_id)
    # instantiate SearchForm to be rendered
    form = SearchForm() # invoke ModelForm
    return render(request, 'franchises/search.html', {
        'franchise': franchise,
        'franchise_id': franchise_id,
        'form': form
    })

# GET PLAYERS (SEARCH RESULTS)
def get_players(request, franchise_id):
    results = {}
    franchise = Franchise.objects.get(id=franchise_id)
    # instantiate AddPlayerForm to be rendered
    add_player_form = AddPlayerForm()
    # check if search form is submitted
    if request.method == 'POST':
        form = SearchForm(request.POST)
        # print(form)
        if form.is_valid():
            # print(f"form.cleaned_data: {form.cleaned_data}")
            query = form.cleaned_data['first_name']
            print(f"query: {query}")
            endpoint = 'https://www.balldontlie.io/api/v1/players?per_page=20'
            # try:
            response = requests.get(endpoint, params={'search': query})
            results = response.json()

                # print(results['data'])
                # jsonResults = JsonResponse(results['data'], safe=False)
                # return jsonResults
                # print(f"jsonResults: {jsonResults}")
                # return JsonResponse(results['data'], safe=False)
                # return render(request, 'franchises/search.html',
                #     )
                # return redirect('players_search', {
                #     'franchise': franchise,
                #     'results': jsonResults
                # })

            # except requests.RequestException as e:
            #     print(f"An error occured while fetching data from API: {e}")
            #     return JsonResponse({
            #         'error': 'An error occured while fetching from the API'
            #     }, status=500)
    else:
        form = SearchForm()    
        # return JsonResponse({'error': 'Invalid request'}, status=400)
    return render(request, 'franchises/search.html', {
        'form': form,
        'results': results,
        'franchise_id': franchise_id,
        'franchise': franchise,
        'add_player_form': add_player_form
    })

# ADD PLAYER TO FRANCHISE
def add_player(request, franchise_id):
    if request.method == 'POST':
        player_id = request.POST.get('player-id')
        # print(player_id)
        endpoint = 'https://www.balldontlie.io/api/v1/players/'
        response = requests.get(f"{endpoint}{player_id}")
        # print(response.url)
        result = response.json()
        # print(result['id'])
        new_player = Player(
            id=result['id'],
            first_name=result['first_name'],
            last_name=result['last_name'],
            position=result['position'],
            height_feet=result['height_feet'],
            height_inches=result['height_inches'],
            weight_pounds=result['weight_pounds'],
            franchise_id=franchise_id
        )
        new_player.save()

    #     add_player_form = AddPlayerForm(request.POST)
    #     if add_player_form.is_valid():
    #         response = requests.get(f"{endpoint}")
    #         results = response.json()


    #         new_player = add_player_form.save(commit=False)
    #         new_player.franchise_id = franchise_id
    #         new_player.save()
    else:
        print('No post')
    return redirect('get_players', franchise_id=franchise_id)