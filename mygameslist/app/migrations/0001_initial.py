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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='Title')),
                ('synopsis', models.TextField(verbose_name='Synopsis')),
                ('platform', models.CharField(max_length=10, verbose_name='Platform')),
                ('release_date', models.DateField(verbose_name='First release date')),
                ('score', models.DecimalField(max_digits=4, null=True, decimal_places=2, verbose_name='Score', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('developer', models.ManyToManyField(related_name='gameclaim_developers', to='app.Company', verbose_name='Developer')),
                ('publisher', models.ManyToManyField(related_name='gameclaim_publishers', to='app.Company', verbose_name='publisher')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameRecommendation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('game1', models.ForeignKey(related_name='gamerecommendation_game1', to='app.Game')),
                ('game2', models.ForeignKey(related_name='gamerecommendation_game2', to='app.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GameReview',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(to='app.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ListEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='Score')),
                ('game', models.ForeignKey(to='app.Game')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'list entries',
            },
            bases=(models.Model,),
        ),
    ]
