# Generated by Django 4.2.1 on 2023-05-27 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_otp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Otp',
        ),
    ]
