# Generated by Django 4.2.10 on 2024-02-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0003_reservation"),
    ]

    operations = [
        migrations.CreateModel(
            name="CapstoneBooking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=200)),
                ("No_of_guests", models.SmallIntegerField()),
                ("BookingDate", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="CapstoneMenu",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Title", models.CharField(max_length=200)),
                ("Price", models.DecimalField(decimal_places=2, max_digits=6)),
                ("Inventory", models.SmallIntegerField()),
            ],
        ),
    ]