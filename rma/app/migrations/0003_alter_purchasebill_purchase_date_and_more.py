# Generated by Django 4.2.1 on 2023-05-30 06:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_purchasebill_purchase_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasebill',
            name='purchase_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 30, 6, 9, 58, 753006, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellbill',
            name='sell_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 30, 6, 9, 58, 753006, tzinfo=datetime.timezone.utc)),
        ),
    ]
