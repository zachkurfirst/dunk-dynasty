from django.shortcuts import render
# Import for CBV
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Import for redirect
from django.urls import reverse_lazy
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

# FRANCHISES INDEX
def franchises_index(request):
    franchises = Franchise.objects.all()
    return render(request, 'franchises/index.html', {
        'franchises': franchises
    })

# FRANCHISES DETAIL
def franchises_detail(request, franchise_id):
    franchise = Franchise.objects.get(id=franchise_id)
    return render(request, 'franchises/detail.html', {
        'franchise': franchise
    })

# FRANCHISES CREATE
class FranchiseCreate(CreateView):
    model = Franchise
    fields = '__all__'
    # no success url necessary -> references get_absolute_url from model

# FRANCHISES UPDATE
class FranchiseUpdate(UpdateView):
    model = Franchise
    fields = '__all__'
    # no success url necessary -> references get_absolute_url from model

# FRANCHISES DELETE
class FranchiseDelete(DeleteView):
    model = Franchise
    success_url = reverse_lazy('franchises_index')