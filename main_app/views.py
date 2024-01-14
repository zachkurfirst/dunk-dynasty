from django.shortcuts import render

franchises = [
    {'city': 'Cincinnati',
     'name': 'Pythons',
     'motto': 'Winning is the only option.',
     'established': 'Jan 2024'},
     {'city': 'Buffalo',
     'name': 'Wings',
     'motto': 'Buffalo built.',
     'established': 'Jan 2024'},
     {'city': 'Seattle',
      'name': 'Swish',
      'motto': 'Bringing hoops back to where it belongs.',
      'established': 'Jan 2024'},
]

# Create your views here.

# HOME VIEW
def home(request):
    return render(request, 'home.html')

# ABOUT VIEW
def about(request):
    return render(request, 'about.html')

# FRANCHISES INDEX
def franchises_index(request):
    return render(request, 'franchises/index.html', {
        'franchises': franchises
    })