# Generated by Django 5.2 on 2025-04-11 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bidding', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='bid',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Status'),
        ),
    ]
