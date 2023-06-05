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
        if request.request.is_superuser():
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
        return HttpResponseRedirect((redirect_path))
    

    def all_table_data(request, table):
        return table.object.all()
    
    def filteration(self, table, kwargs):
        return table.objects.filter(kwargs)

    def not_superuser(self, request):
        if request.user.is_staff:
            return 'manager_view'
        else:
            return False

    def not_staff(self, request):
        if request.user.is_superuser:
            return 'admin_view'
        else:
            return False

object = RenderUrls()


from django.core.exceptions import ValidationError

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
            User_password = ''.join([random.choice(string.digits) for i in range(6)])

            try:
                # Create a new user account
                user_account = UserAccounts.objects.create(email=email)

                # Create a new registration entry
                registration_entry = Registration(
                    fullName=fullName,
                    department=department,
                    empId=empId,
                    officeName=officeName,
                    officeCode=officeCode,
                    user=user_account
                )
                registration_entry.full_clean()  # Validate the registration entry

                # Send email
                subject = 'FIXED INVENTORY MANAGEMENT SYSTEM ANALYTICS AND TRACKING'
                message = f'hello this is FIXED INVENTORY MANAGEMENT SYSTEM ANALYTICS AND TRACKING Your password is {User_password}'
                mail_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                send_mail(subject, message, mail_from, recipient_list)

                # Save the registration entry
                registration_entry.save()

                return object.render_view(request, view_file='fimswaat/index.html', registration_data=RegistrationForm(), success=True)
            
            except ValidationError:
                # Handle validation errors
                return object.render_view(request, view_file='fimswaat/index.html', registration_data=capture_form_data, internal_server_error=True)
            
            except IntegrityError:
                # Handle duplicate email error
                return object.render_view(request, view_file='fimswaat/index.html', registration_data=capture_form_data, data_exist='email already exists')
    
    return object.render_view(request, view_file='fimswaat/index.html', registration_data=RegistrationForm())



def login_view(request):
    if request.user.is_authenticated:
        return object.redirection_func(redirect_path=object.anonymousUser(request))
    
    if request.method == 'POST':
        login_data = LoginForm(request.POST)
        if login_data.is_valid():
            username = login_data.cleaned_data['username']
            password = login_data.cleaned_data['passcode']
            login_user = authenticate(username=username, password=password)
            if login_user is not None:
                login(request, login_user)
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
    if not request.user.is_staff:
        return object.redirection_func(redirect_path=object.not_staff(request))
    
    return object.render_view(request, view_file='fimswaat/manager.html')
    

def logout_view(request):
    logout(request)
    return object.redirection_func(redirect_path='login_view')
