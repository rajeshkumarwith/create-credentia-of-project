# Generated by Django 3.2.10 on 2023-05-03 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchconsoledata',
            name='user',
        ),
    ]