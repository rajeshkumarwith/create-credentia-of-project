# Generated by Django 3.2.10 on 2023-04-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('clicks', models.IntegerField()),
                ('impressions', models.IntegerField()),
                ('ctr', models.FloatField()),
                ('position', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SearchConsoleResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_url', models.CharField(max_length=255)),
                ('keyword', models.CharField(max_length=255)),
                ('response', models.JSONField()),
            ],
        ),
    ]
