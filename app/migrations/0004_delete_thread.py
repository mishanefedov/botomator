# Generated by Django 3.2.4 on 2021-06-13 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_thread'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Thread',
        ),
    ]