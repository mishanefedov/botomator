# Generated by Django 2.2.20 on 2021-05-21 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post_first_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='running',
            field=models.BooleanField(default=False),
        ),
    ]