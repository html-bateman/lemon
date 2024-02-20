# Generated by Django 4.2.10 on 2024-02-20 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0002_menu_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation",
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
                ("first_name", models.CharField(max_length=200)),
                ("reservation_date", models.DateField()),
                ("reservation_slot", models.SmallIntegerField(default=10)),
            ],
        ),
    ]
