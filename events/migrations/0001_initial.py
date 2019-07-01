# Generated by Django 2.0.7 on 2019-06-21 23:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('datetime', models.DateTimeField()),
                ('city', models.CharField(max_length=64)),
                ('city_district', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=64)),
                ('location_name', models.CharField(max_length=64)),
                ('price', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(max_length=2048)),
                ('is_active', models.BooleanField(default=False)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_hidden', models.BooleanField(default=False)),
                ('red', models.PositiveIntegerField(default=255)),
                ('green', models.PositiveIntegerField(default=255)),
                ('blue', models.PositiveIntegerField(default=255)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Artist')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_text', models.CharField(max_length=128)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('telephone', models.CharField(max_length=64)),
                ('is_success', models.BooleanField(default=False)),
                ('is_removed', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
