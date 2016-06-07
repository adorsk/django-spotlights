# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-07 15:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Display',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QueueItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='spotlights.Item')),
                ('title', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('spotlights.item',),
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='spotlights.Item')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('render_cfg', models.TextField(blank=True)),
                ('author', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slide_for_author', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slide_for_modifier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('spotlights.item',),
        ),
        migrations.AddField(
            model_name='queueitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='spotlights.Item'),
        ),
        migrations.AddField(
            model_name='queueitem',
            name='queue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='queue', to='spotlights.Queue'),
        ),
        migrations.AddField(
            model_name='queue',
            name='items',
            field=models.ManyToManyField(related_name='items', through='spotlights.QueueItem', to='spotlights.Item'),
        ),
        migrations.AddField(
            model_name='display',
            name='queue',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='spotlights.Queue'),
        ),
    ]
