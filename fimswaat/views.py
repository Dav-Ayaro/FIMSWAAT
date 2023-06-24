from django.shortcuts import render
from django .http import HttpResponseRedirect
from . forms import RegistrationForm, LoginForm, ChangePassword
from . models import Department, UserAccounts,Registration
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import  login, logout
import random, string,  socket
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import re
from .models import Location, Product

# Create your views here.

User = get_user_model()

class SystemRequirements():
    def __init__(self):
        self.departments = Department


    # def create_department(self):
    #     for department in self.departments:
    #         department.create_group()
    #     return "Department created successfully."

    def random_func(self, length):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range (length)])
    
    def Time(self):
        return timezone.datetime.now().year
    


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
    
    def get_all_department(request):
        depart = Department.objects
        return depart
    
    def get_logged_in_user(self, request):
        get_user = (request.user)
        return get_user
    
    def get_all_users(request):
        query = Q(is_superuser=False) & Q(is_staff=False)
        all_users = UserAccounts.objects.filter(query).values()
        return all_users

    def get_group_users(self, request):
        user = (request.user)
        get_user = Registration.objects.get(user=user)
        return get_user


    def get_all_groups(request):
        all_groups = Group.objects
        return all_groups

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
    year = object.Time()
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
    return object.render_view(request, view_file='fimswaat/index.html', capture_form_data=RegistrationForm(),year=year)


def login_view(request):
    year = object.Time()
    get_user = object.get_all_users().all()
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
    return object.render_view(request, view_file='fimswaat/auth.html',login_info=LoginForm(),year=year,get_user=get_user)

@staff_member_required(login_url=reverse_lazy('login_view'))
def admin_view(request):
    if not request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_superuser(request))
    
    return HttpResponseRedirect('/admin/')

@login_required(login_url=reverse_lazy('login_view'))
def manager_view(request):
    if request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_staff(request))
    all_depart = object.get_all_department().all()
    get_group = object.get_all_groups().all()
    year = object.Time()
    obtained_user = object.get_group_users(request)

    return object.render_view(request, view_file='fimswaat/manager.html',all_depart=all_depart,get_group=get_group,year=year,obtained_user=obtained_user)

@login_required(login_url=reverse_lazy('login_view'))
def enrollment_view(request, group_id):
    if request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_staff(request))
    
    try:
        user = object.get_logged_in_user(request)
        group = Group.objects.get(id=group_id)
        print(group)
        user.groups.add(group)
        user.save()
        return object.render_view(request, view_file='fimswaat/manager.html', success=True)
    except User.DoesNotExist:
        return object.render_view(request, view_file='fimswaat/manager.html', enrollment_error=True)
    except Group.DoesNotExist:
        return object.render_view(request, view_file='fimswaat/manager.html', enrollment_error=True)


@login_required(login_url=reverse_lazy('login_view'))
def manager_settings_view(request):
    if request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_staff)
    
    get_user = object.get_logged_in_user(request)
    print(get_user)
    year = object.Time()
    if request.method == 'POST':
        change_passcode = ChangePassword(request.POST) if request.method == 'POST' else None

        if change_passcode and change_passcode.is_valid():
            pwd = change_passcode.cleaned_data['pwd']
            pwd_rpt = change_passcode.cleaned_data['pwd_rpt']

            if pwd and pwd_rpt and pwd == pwd_rpt:
                get_user.set_password(pwd)
                get_user.save()
                return object.redirection_func(redirect_path='changed_view')
            else:
                return object.render_view(request, view_file='fimswaat/member_settings.html', ChangePassword=ChangePassword(), password_do_not_match=True,get_user=get_user)
        else:
            return object.render_view(request, view_file='fimswaat/member_settings.html', ChangePassword=ChangePassword(), error=True,get_user=get_user)
        
    return object.render_view(request, view_file='fimswaat/member_settings.html', ChangePassword=ChangePassword(),year=year)


def changed_view(request):
    if request.user.is_superuser:
        return object.redirection_func(redirect_path=object.not_staff)
    year = object.Time()
    
    return object.render_view(request, view_file='fimswaat/change_success.html',year=year)

def logout_view(request):
    logout(request)
    return object.redirection_func(redirect_path= 'login_view')


def location_list(request):
    locations = Location.objects.all()
    return render(request, 'location_list.html', {'locations': locations})

def location_detail(request, location_id):
    location = Location.objects.get(id=location_id)
    return render(request, 'location_detail.html', {'location': location})


def location_table_view(request):
    user = request.user
    department = user.department

    if department:
        # Fetch location table entries based on the department
        location_table_entries = Location.objects.filter(department=department)
    else:
        location_table_entries = []

    context = {
        'location_table_entries': location_table_entries
    }

    return render(request, 'location_table.html', context)


def product_details(request, barcode):
    product = Product.objects.get(barcode=barcode)
    return render(request, 'product_details.html', {'product': product})

def generate_report(request):
    products = Product.objects.all()
    return render(request, 'report.html', {'products': products})


