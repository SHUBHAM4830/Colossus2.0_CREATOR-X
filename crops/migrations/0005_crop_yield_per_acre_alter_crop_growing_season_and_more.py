# Generated by Django 5.2 on 2025-04-11 20:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crops', '0004_alter_crop_image_alter_crop_market_preference_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='yield_per_acre',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Yield per Acre (tons)'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='growing_season',
            field=models.CharField(choices=[('kharif', 'Kharif (Monsoon)'), ('rabi', 'Rabi (Winter)'), ('zaid', 'Zaid (Summer)'), ('year_round', 'Year Round')], default='all', max_length=20, verbose_name='Growing Season'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='irrigation_method',
            field=models.CharField(choices=[('drip', 'Drip Irrigation'), ('sprinkler', 'Sprinkler'), ('flood', 'Flood Irrigation'), ('furrow', 'Furrow Irrigation')], default='rainfed', max_length=20, verbose_name='Irrigation Method'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='market_preference',
            field=models.CharField(choices=[('local', 'Local Market'), ('export', 'Export Market'), ('processing', 'Processing Industry')], default='both', max_length=20, verbose_name='Market Preference'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='soil_type',
            field=models.CharField(choices=[('clay', 'Clay'), ('sandy', 'Sandy'), ('loamy', 'Loamy'), ('black', 'Black'), ('red', 'Red')], default='loamy', max_length=20, verbose_name='Soil Type'),
        ),
        migrations.CreateModel(
            name='CropRecommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('soil_type', models.CharField(choices=[('clay', 'Clay'), ('sandy', 'Sandy'), ('loamy', 'Loamy'), ('black', 'Black'), ('red', 'Red')], max_length=20)),
                ('climate_zone', models.CharField(choices=[('tropical', 'Tropical'), ('subtropical', 'Subtropical'), ('temperate', 'Temperate'), ('arid', 'Arid')], max_length=20)),
                ('field_area', models.FloatField()),
                ('soil_ph', models.FloatField()),
                ('rainfall', models.IntegerField()),
                ('irrigation_method', models.CharField(choices=[('drip', 'Drip Irrigation'), ('sprinkler', 'Sprinkler'), ('flood', 'Flood Irrigation'), ('furrow', 'Furrow Irrigation')], max_length=20)),
                ('growing_season', models.CharField(choices=[('kharif', 'Kharif (Monsoon)'), ('rabi', 'Rabi (Winter)'), ('zaid', 'Zaid (Summer)'), ('year_round', 'Year Round')], max_length=20)),
                ('market_preference', models.CharField(choices=[('local', 'Local Market'), ('export', 'Export Market'), ('processing', 'Processing Industry')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recommendations', models.JSONField(default=list)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
