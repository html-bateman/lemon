from django.db import models


# Create your models here.
class Booking(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    guest_number = models.IntegerField()
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class CapstoneBooking(models.Model):
    Name = models.CharField(max_length=200)
    No_of_guests = models.SmallIntegerField()
    BookingDate = models.DateTimeField()

    def __str__(self) -> str:
        return self.Name


class Reservation(models.Model):
    first_name = models.CharField(max_length=200)
    reservation_date = models.DateField()
    reservation_slot = models.SmallIntegerField(default=10)

    def __str__(self) -> str:
        return self.first_name

# Add code to create Menu model


class Menu(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(max_length=1000, default='')

    def __str__(self):
        return self.name


class CapstoneMenu(models.Model):
    Title = models.CharField(max_length=200)
    Price = models.DecimalField(max_digits=6, decimal_places=2)
    Inventory = models.SmallIntegerField()

    def __str__(self):
        return f'{self.Title}:{str(self.Price)}'
