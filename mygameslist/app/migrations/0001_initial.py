# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('synopsis', models.TextField()),
                ('platform', models.CharField(max_length=10)),
                ('release_date', models.DateField(verbose_name='First release date')),
                ('score', models.DecimalField(null=True, verbose_name='Score', max_digits=4, decimal_places=2, blank=True)),
                ('developer', models.ManyToManyField(related_name='gameclaim_developers', verbose_name='Developer', to='app.Company')),
                ('publisher', models.ManyToManyField(related_name='gameclaim_publishers', verbose_name='publisher', to='app.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('score', models.IntegerField(verbose_name='Score')),
                ('review', models.TextField(verbose_name='Review')),
                ('game', models.ForeignKey(verbose_name='Game', to='app.Game')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
