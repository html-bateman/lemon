# Generated by Django 4.2.10 on 2024-02-16 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="quantity",
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
