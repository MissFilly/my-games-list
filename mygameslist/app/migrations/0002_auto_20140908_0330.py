# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRecommendation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(to='app.ListEntry')),
                ('game1', models.ForeignKey(to='app.Game', related_name='gamerecommendation_game1')),
                ('game2', models.ForeignKey(to='app.Game', related_name='gamerecommendation_game2')),
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
                ('entry', models.ForeignKey(to='app.ListEntry')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='listentry',
            name='review',
        ),
        migrations.AlterField(
            model_name='game',
            name='platform',
            field=models.CharField(verbose_name='Platform', max_length=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='synopsis',
            field=models.TextField(verbose_name='Synopsis'),
        ),
        migrations.AlterField(
            model_name='listentry',
            name='game',
            field=models.ForeignKey(to='app.Game'),
        ),
        migrations.AlterField(
            model_name='listentry',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
