# Generated by Django 3.2.10 on 2023-05-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_googletoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleSearchConsoleTokenData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
            ],
        ),
    ]