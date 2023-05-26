# Generated by Django 4.2.1 on 2023-05-14 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_sellbill_alter_purchasebill_purchase_date_sellitem_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hsncode',
            old_name='sales_price',
            new_name='sell_price',
        ),
        migrations.AlterField(
            model_name='purchasebill',
            name='purchase_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 14, 6, 58, 24, 718529, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='sellbill',
            name='sell_date',
            field=models.DateField(default=datetime.datetime(2023, 5, 14, 6, 58, 24, 718529, tzinfo=datetime.timezone.utc)),
        ),
    ]