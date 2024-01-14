from django.shortcuts import render

# Create your views here.

# HOME VIEW
def home(request):
    return render(request, 'home.html')

# ABOUT VIEW
def about(request):
    return render(request, 'about.html')