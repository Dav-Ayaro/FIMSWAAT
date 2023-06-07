from django.shortcuts import render
from django .http import HttpResponse, HttpResponseRedirect
from . forms import RegistrationForm, LoginForm
from . models import department, UserAccounts,Registration
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
import random, string,  socket
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.


class SystemRequirements():
    def __init__(self):
        self.departments = department

    def random_func(self, length):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range (length)])
    
    def Time(self):
        return timezone.datetime.now
    


class RenderUrls(SystemRequirements):
    def anonymousUser(self, request):
        if request.user.is_superuser:
            return 'admin_view'
        elif request.user.is_staff:
            return 'manager_view'
        else:
            return 'logout_view'


    def render_view(self, request, view_file, **kwargs):
        return render(request, view_file, kwargs)

    def redirection_func(self, redirect_path=None, **kwargs):
        if kwargs:
            redirect_path += '?' + urlencode(kwargs)
        return HttpResponseRedirect(reverse(redirect_path))
    

    def all_table_data(request, table):
        return table.object.all()
    
    def filteration(self, table, kwargs):
        return table.objects.filter(kwargs)

    def not_superuser(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            return 'manager_view'

    def not_staff(self, request):
        if request.user.is_superuser:
            return 'admin_view'

object = RenderUrls()

def generate_random_password(length=8):
    # Generate a random password with 8 characters
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def index_view(request):
    if request.method == 'POST':
        capture_form_data = RegistrationForm(request.POST)
        if capture_form_data.is_valid():
            fullName = capture_form_data.cleaned_data['fullName']
            email = capture_form_data.cleaned_data['email']
            department = capture_form_data.cleaned_data['department']
            empId = capture_form_data.cleaned_data['empId']
            officeName = capture_form_data.cleaned_data['officeName']
            officeCode = capture_form_data.cleaned_data['officeCode']
            # Generate random password
            password = generate_random_password()
            # Create UserAccounts entry
            user = UserAccounts.objects.create(username=email, email=email,password=make_password(password))
            # Create Registration entry
            Registration.objects.create(user=user,fullName=fullName,department=department,empId=empId,officeName=officeName,officeCode=officeCode)
            try:
                # Send email
                subject = 'Registration Successful'
                message = f"Dear {fullName},\n\nThank you for registering. Your registration details:\n\nFull Name: {fullName}\nEmail: {email}\nDepartment: {department}\nEmployee ID: {empId}\nOffice Name: {officeName}\nOffice Code: {officeCode}\n\nYour password is: {password} use this password to login then you will change the password"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list)
                return object.redirection_func(redirect_path='login_view')
            except (OSError, socket.gaierror):
                return object.render_view(request, view_file='fimswaat/index.html',email_succesfully=True)
    return object.render_view(request, view_file='fimswaat/index.html', capture_form_data=RegistrationForm())


def login_view(request):
    if request.user.is_authenticated:
        return object.redirection_func(redirect_path=object.anonymousUser(request))
    
    if request.method == 'POST':
        login_data = LoginForm(request.POST)
        if login_data.is_valid():
            email = login_data.cleaned_data['email']
            password = login_data.cleaned_data['passcode']
            try:
                user = UserAccounts.objects.get(email=email)
            except UserAccounts.DoesNotExist:
                user = None
            if user:
                username = user.username
            if user and user.check_password(password):
                login(request, user)
                if request.user.is_superuser:
                    return HttpResponseRedirect('/admin/')
                else:
                    return object.redirection_func(redirect_path='manager_view')
            else:
                return object.render_view(request,view_file='fimswaat/auth.html', login_info=login_data, wrong_login='wrong_login')
        return object.render_view(request, view_file='fimswaat/auth.html', invalid_data='invalid_data',login_info=login_data)
    return object.render_view(request, view_file='fimswaat/auth.html',login_info=LoginForm())

@staff_member_required(login_url=reverse_lazy('login_view'))
def admin_view(request):
    if not request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_superuser(request))
    
    return HttpResponseRedirect('/admin/')

@login_required(login_url=reverse_lazy('login_view'))
def manager_view(request):
    if request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_staff(request))
    
    return object.render_view(request, view_file='fimswaat/manager.html')
    

def logout_view(request):
    logout(request)
    return object.redirection_func(redirect_path= 'login_view')