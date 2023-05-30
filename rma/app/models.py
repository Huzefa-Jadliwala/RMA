from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

payment_status_choices = [
    ("Pending", "Payment is yet to be done"),
    ("Paid", "Payment is done")
]

class HSNCode(models.Model):
    hsncode_pk = models.CharField(max_length=10, blank=False)
    in_stock = models.IntegerField(default=0)
    purchase_price = models.IntegerField(default=0)
    sell_price = models.IntegerField(default=0)
    stock_value = models.IntegerField(default=0)
    
    def cal_stock_val(self, *args, **kwargs):
        self.stock_value = self.in_stock * self.purchase_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.hsncode_pk} - In Stock: {self.in_stock}, Purchase Price: {self.purchase_price}, Sales Price: {self.sell_price}"
    
class Item(models.Model):
    item_pk = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length = 180)
    item_detail = models.TextField(max_length=200)
    item_low_stock_alert = models.IntegerField(default=0)
    item_packaging_type =  models.CharField(max_length=50)
    item_company = models.CharField(max_length=50)
    hsncodes = models.ManyToManyField(HSNCode, blank=True, related_name='item', related_query_name='item')

    def __str__(self):
        return self.item_name
    
class SupplierModel(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length = 50)
    supplier_location = models.CharField(max_length = 100)
    pending_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier_gst = models.CharField(max_length = 15, blank=True, null=True)
    supplier_dl= models.CharField(max_length = 50, blank=True, null=True)


    def __str__(self):
        return self.supplier_name
    
class ClientModel(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length = 50)
    client_location = models.CharField(max_length = 100)
    pending_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    client_gst = models.CharField(max_length = 15, blank=True, null=True)
    client_dl= models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return self.client_name


class PurchaseBill(models.Model):
    purchase_bill_pk = models.AutoField(primary_key=True)
    purchase_date = models.DateField(default=timezone.now())
    supplier = models.ForeignKey(SupplierModel, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=25, choices=payment_status_choices, default="Pending")
    items = models.ManyToManyField(Item, through='PurchaseItem')

    def cal_total_amount(self, bill_total_amount, *args, **kwargs):
        self.total_amount = bill_total_amount
        super().save(*args, **kwargs)

class PurchaseItem(models.Model):
    purchase_bill = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    hsncode = models.CharField(max_length=10)
    quantity = models.IntegerField()
    pprice = models.DecimalField(max_digits=10, decimal_places=2)
    sprice = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class SellBill(models.Model):
    sell_bill_pk = models.AutoField(primary_key=True)
    sell_date = models.DateField(default=timezone.now())
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=25, choices=payment_status_choices, default="Pending")
    items = models.ManyToManyField(Item, through='SellItem')

    def cal_total_amount(self, bill_total_amount, *args, **kwargs):
        self.total_amount = bill_total_amount
        super().save(*args, **kwargs)

    def cal_total_profit(self, bill_total_profit, *args, **kwargs):
        self.total_profit = bill_total_profit
        super().save(*args, **kwargs)

class SellItem(models.Model):
    sell_bill = models.ForeignKey(SellBill, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    hsncode = models.ForeignKey(HSNCode, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sprice = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def cal_profit(self, item_profit, *args, **kwargs):
        self.profit = item_profit
        super().save(*args, **kwargs)