# Generated by Django 4.2.1 on 2023-05-21 12:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_rename_price_purchaseitem_pprice_purchaseitem_sprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasebill',
            name='purchase_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 21, 12, 41, 46, 772551, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellbill',
            name='sell_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 21, 12, 41, 46, 772551, tzinfo=datetime.timezone.utc)),
        ),
    ]