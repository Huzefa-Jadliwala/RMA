# Generated by Django 4.2.1 on 2023-05-30 07:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_clientmodel_client_dl_clientmodel_client_gst_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasebill',
            name='purchase_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 30, 7, 22, 24, 920244, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellbill',
            name='sell_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 30, 7, 22, 24, 920244, tzinfo=datetime.timezone.utc)),
        ),
    ]
