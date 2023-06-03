from django.shortcuts import render
from django .http import HttpResponse, HttpResponseRedirect
from . forms import *
# Create your views here.

def admin_dash(request):
    if not request.user.is_authenticated:
        return render(request, 'fimswaat/index.html')
    if request.method == 'POST':
        capture_form_data = RegistrationForm(request.POST)
        if capture_form_data.is_valid():
            pass

    return render(request, 'fimswaat/index.html',{
        'Form':RegistrationForm()
    })

def login_view(request):
    return render(request, 'fimswaat/auth.html')

def user_dash_view(request):
    return render(request, 'fimswaat/user_dash.html')

def logout_view(request):
    pass
