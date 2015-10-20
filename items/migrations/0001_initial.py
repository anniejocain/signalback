# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SBUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name=b'email address', db_index=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=45, blank=True)),
                ('last_name', models.CharField(max_length=45, blank=True)),
                ('confirmation_code', models.CharField(max_length=45, blank=True)),
            ],
            options={
                'verbose_name': 'User',
            },
        ),
        migrations.CreateModel(
            name='BookmarkletKey',
            fields=[
                ('key', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('display_name', models.CharField(max_length=400, null=True, blank=True)),
                ('profile_pic', models.ImageField(default=b'/static/img/anon.jpg', upload_to=b'profile-pics')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=400)),
                ('description', models.CharField(max_length=117, null=True, blank=True)),
                ('link', models.URLField(max_length=2000, null=True, blank=True)),
                ('contributor', models.CharField(max_length=400, null=True, blank=True)),
                ('contributed_date', models.DateTimeField(auto_now=True)),
                ('bookmarklet_key', models.ForeignKey(to='items.BookmarkletKey')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=400)),
                ('slug', models.SlugField(unique=True)),
                ('public_link', models.URLField(max_length=2000, null=True, blank=True)),
                ('public_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='bookmarkletkey',
            name='organization',
            field=models.ForeignKey(to='items.Organization'),
        ),
    ]
