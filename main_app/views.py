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
# Import Franchise Model
from .models import Franchise

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
    return render(request, 'franchises/my_index.html', {
        'franchises': my_franchises
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