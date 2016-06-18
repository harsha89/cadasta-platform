# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-17 19:46
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSpatialUnit',
            fields=[
                ('id', models.CharField(db_index=True, max_length=24)),
                ('name', models.CharField(max_length=200)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326)),
                ('type', models.CharField(choices=[('PA', 'Parcel'), ('CB', 'Community boundary'), ('BU', 'Building'), ('AP', 'Apartment'), ('PX', 'Project extent'), ('RW', 'Right-of-way'), ('UC', 'Utility corridor'), ('NP', 'National park boundary'), ('MI', 'Miscellaneous')], default='PA', max_length=2)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='organization.Project')),
            ],
            options={
                'verbose_name': 'historical spatial unit',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalSpatialUnitRelationship',
            fields=[
                ('id', models.CharField(db_index=True, max_length=24)),
                ('type', models.CharField(choices=[('C', 'is-contained-in'), ('S', 'is-split-of'), ('M', 'is-merge-of')], max_length=1)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='organization.Project')),
            ],
            options={
                'verbose_name': 'historical spatial unit relationship',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='SpatialUnit',
            fields=[
                ('id', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326)),
                ('type', models.CharField(choices=[('PA', 'Parcel'), ('CB', 'Community boundary'), ('BU', 'Building'), ('AP', 'Apartment'), ('PX', 'Project extent'), ('RW', 'Right-of-way'), ('UC', 'Utility corridor'), ('NP', 'National park boundary'), ('MI', 'Miscellaneous')], default='PA', max_length=2)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spatial_units', to='organization.Project')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='SpatialUnitRelationship',
            fields=[
                ('id', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('C', 'is-contained-in'), ('S', 'is-split-of'), ('M', 'is-merge-of')], max_length=1)),
                ('attributes', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Project')),
                ('su1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spatial_unit_one', to='spatial.SpatialUnit')),
                ('su2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spatial_unit_two', to='spatial.SpatialUnit')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='spatialunit',
            name='relationships',
            field=models.ManyToManyField(related_name='relationships_set', through='spatial.SpatialUnitRelationship', to='spatial.SpatialUnit'),
        ),
        migrations.AddField(
            model_name='historicalspatialunitrelationship',
            name='su1',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='spatial.SpatialUnit'),
        ),
        migrations.AddField(
            model_name='historicalspatialunitrelationship',
            name='su2',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='spatial.SpatialUnit'),
        ),
    ]
