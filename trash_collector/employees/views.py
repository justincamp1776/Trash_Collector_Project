
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Employee
from datetime import date
from datetime import datetime





@login_required
def index(request):
    # The following line will get the logged-in user (if there is one) within any view function
    today2 = determine_day()

    logged_in_user = request.user
    try:
        # This line will return the customer record of the logged-in user if one exists
        logged_in_employee = Employee.objects.get(user=logged_in_user)

        today = date.today()

        Customer = apps.get_model('customers.Customer')
        todays_pickups = Customer.objects.filter(
            zip_code=logged_in_employee.zip_code).filter(weekly_pickup=today2).exclude(suspend_start__lte=today, suspend_end__gte=today).exclude(
            date_of_last_pickup = today)

        # today_pickups = customers_in_zip.objects.filter(weekly_pickup=today2)
        one_time_pickups = Customer.objects.filter(
            zip_code=logged_in_employee.zip_code).filter(one_time_pickup=today).exclude(suspend_start__lte=today, suspend_end__gte=today).exclude(
            date_of_last_pickup = today)

        context = {
            'logged_in_employee': logged_in_employee,
            'today': today,
            'todays_pickups': todays_pickups,
            'one_time_pickups': one_time_pickups
        }
        return render(request, 'employees/index.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:create'))

# displays selected fields from the employee table on the logged in user/employee
@login_required
def view_profile(request):
    try:
        logged_in_user = request.user
        logged_in_employee = Employee.objects.get(user=logged_in_user)
        context = {
            'logged_in_employee' : logged_in_employee
        }
        return render(request, 'employees/profile.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))


 #returns all customers from the database
@login_required
def view_customers(request):
        Customer = apps.get_model('customers.Customer')
        customers = Customer.objects.all()
        context = {
            'customers' : customers
        }
        return render(request, 'employees/customers.html', context)


# allows employee to edit customer information
@login_required
def update_customer(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer_to_update = Customer.objects.get(id=customer_id)
    if request.method == "POST":
        name_from_form = request.POST.get('name')
        address_from_form = request.POST.get('address')
        zip_from_form = request.POST.get('zip_code')
        weekly_pickup_from_form = request.POST.get("weekly_pickup")
        balance_from_form = request.POST.get("balance")
        customer_to_update.name = name_from_form
        customer_to_update.address = address_from_form
        customer_to_update.zip_code = zip_from_form
        customer_to_update.weekly_pickup = weekly_pickup_from_form
        customer_to_update.balance = balance_from_form
        customer_to_update.save()
        return HttpResponseRedirect(reverse('employees:customers'))
    else:
        context = {
            'customer_to_update': customer_to_update
        }
        return render(request, 'employees/update_customer.html', context)


# converts the day as an integer into a day as a string
def determine_day():
    today2 = date.today()
    today = today2.weekday()
    if today == 0:
        return "Monday"
    elif today == 1:
        return "Tuesday"
    elif today == 2:
        return "Wednesday"
    elif today == 3:
        return "Thursday"
    elif today == 4:
        return "Friday"
    elif today == 5:
        return "Saturday"
    elif today == 6:
        return "Sunday"


# confirms pickup and increases customer balance by $20
def confirm_pickup(request, customer_id):
    try:
        Customer = apps.get_model('customers.Customer')
        customer_to_update = Customer.objects.get(id=customer_id)
        customer_to_update.balance += 20
        customer_to_update.date_of_last_pickup = date.today()
        customer_to_update.save()

        return render(request, 'employees/index.html')

    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))


# displays the pickups on each day of the week
def view_schedule(request, week_day):
    try:
        Customer = apps.get_model('customers.Customer')
        future_pickups = Customer.objects.filter(weekly_pickup = week_day)


        context = {
            'future_pickups': future_pickups,
            'week_day' : week_day

        }
        return render(request, 'employees/view_schedule.html', context)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('employees:index'))



# allows create their proifile
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

# allows employees to edit their profile
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
