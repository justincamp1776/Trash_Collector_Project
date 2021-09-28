
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Employee
from datetime import date
from datetime import datetime


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function

    today2 = determine_day()

    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today
        }

        Customer = apps.get_model('customers.Customer')
        todays_pickups = Customer.objects.filter(
            zip_code=logged_in_employee.zip_code).filter(weekly_pickup=today2).exclude(suspend_start__lte=today, suspend_end__gte=today)
        

        # today_pickups = customers_in_zip.objects.filter(weekly_pickup=today2)
        one_time_pickups = Customer.objects.filter(
            zip_code=logged_in_employee.zip_code).filter(one_time_pickup=today).exclude(suspend_start__lte=today, suspend_end__gte=today)
        
        context = {
            'todays_pickups': todays_pickups,
            'one_time_pickups' : one_time_pickups
        }

        

        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))




def determine_day():
    today2 = date.today()
    today = today2.weekday()
    if today == 0:
        return "Monday"
    elif today == 1:
        return "Tuesday"
    elif today == 2:
        return "Wednsday"
    elif today == 3:
        return "Thursday"
    elif today == 4:
        return "Friday"
    elif today == 5:
        return "Saturday"
    elif today == 6:
        return "Sunday"

def confirm_pickup(request):
     Customer = apps.get_model('customers.Customer')
    

@login_required
def create(request):
    logged_in_user = request.user
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        new_employee = Employee(name=name_from_form, user=logged_in_user,
                                address=address_from_form, zip_code=zip_from_form)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')


@login_required
def edit_profile(request):
    logged_in_user = request.user
    logged_in_employee = Employee.objects.get(user=logged_in_user)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        logged_in_employee.name = name_from_form
        logged_in_employee.address = address_from_form
        logged_in_employee.zip_code = zip_from_form
        logged_in_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        context = {
            'logged_in_employee': logged_in_employee
        }
        return render(request, 'employees/edit_profile.html', context)
