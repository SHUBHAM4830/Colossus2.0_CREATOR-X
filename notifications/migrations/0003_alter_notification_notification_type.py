# Generated by Django 5.2 on 2025-04-11 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_related_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('bid', 'Bid'), ('bid_accepted', 'Bid Accepted'), ('bid_rejected', 'Bid Rejected'), ('demand', 'Demand'), ('response', 'Demand Response'), ('system', 'System')], default='system', max_length=20, verbose_name='Type'),
        ),
    ]
