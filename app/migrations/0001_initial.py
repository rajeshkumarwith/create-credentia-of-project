# Generated by Django 3.2.19 on 2023-05-16 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DomainVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=255)),
                ('verification_code', models.CharField(blank=True, max_length=255, null=True)),
                ('verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleSearchConsoleToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('access_token', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleSearchConsoleTokenData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.TextField(blank=True, null=True)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
                ('refresh_token', models.CharField(blank=True, max_length=255, null=True)),
                ('token_uri', models.URLField()),
                ('client_id', models.CharField(max_length=200)),
                ('client_secret', models.CharField(max_length=200)),
                ('scopes', models.URLField(max_length=255)),
                ('expiry', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='GoogleToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('lastname', models.CharField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(null=True, verbose_name='date published')),
                ('author', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=100)),
                ('keyword', models.CharField(max_length=150)),
                ('clicks', models.IntegerField()),
                ('ctr', models.IntegerField()),
                ('impressions', models.IntegerField()),
                ('position', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SearchConsoleData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(blank=True, max_length=255, null=True)),
                ('keyword', models.CharField(max_length=255)),
                ('clicks', models.IntegerField()),
                ('ctr', models.FloatField()),
                ('impressions', models.IntegerField()),
                ('position', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=100)),
                ('clicks', models.IntegerField()),
                ('ctr', models.FloatField()),
                ('impressions', models.IntegerField()),
                ('position', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
            ],
        ),
    ]
