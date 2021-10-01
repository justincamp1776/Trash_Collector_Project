from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the user stories, add a path for each in urlpatterns

app_name = "employees"
urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('customer_details/<int:customer_id>/', views.customer_details, name="customer_details"),
    path('view_schedule/<str:week_day>',
         views.view_schedule, name="view_schedule"),
    path('profile/', views.view_profile, name="profile"),
    path('customers/', views.view_customers, name="customers"),
    path('update_customer/<int:customer_id>', views.update_customer, name="update_customer"),

]
