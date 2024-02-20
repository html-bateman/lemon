from django.contrib import admin
from . import models
from .models import DrinksCategory,Booking,Reservation,Employees,Book

# Register your models here.
admin.site.register(models.Drinks)
admin.site.register(DrinksCategory)
admin.site.register(Booking)
admin.site.register(Reservation)
admin.site.register(Employees)
admin.site.register(Book)