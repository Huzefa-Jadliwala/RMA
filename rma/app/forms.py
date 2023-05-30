from django import forms
from .models import Item, HSNCode, PurchaseBill, PurchaseItem, SellBill, SellItem, SupplierModel, ClientModel
from django.forms import formset_factory


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_name'].widget.attrs.update({'class': 'textinput form-control setprice item_name', 'required': 'true' , 'autocomplete': "off"})
        self.fields['item_detail'].widget.attrs.update({'class': 'textinput form-control setprice item_detail', 'required': 'true', 'autocomplete': "off"})
        self.fields['item_low_stock_alert'].widget.attrs.update({'class': 'textinput form-control setprice item_low_stock_alert', 'required': 'true', 'autocomplete': "off" })
        self.fields['item_packaging_type'].widget.attrs.update({'class': 'form-select form-control setprice item_packaging_type', 'required': 'true', 'autocomplete': "off"})
        self.fields['item_company'].widget.attrs.update({'class': 'textinput form-control setprice item_company', 'required': 'true', 'autocomplete': "off"})

    class Meta:
        model = Item
        fields = ['item_name', 'item_detail', 'item_low_stock_alert', 'item_packaging_type', "item_company"]

class SupplierForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier_name'].widget.attrs.update({'class': 'textinput form-control setprice supplier_name', 'required': 'true' , 'autocomplete': "off"})
        self.fields['supplier_location'].widget.attrs.update({'class': 'textinput form-control setprice supplier_location', 'required': 'true' , 'autocomplete': "off"})
        self.fields['supplier_gst'].widget.attrs.update({'class': 'textinput form-control setprice supplier_gst', 'autocomplete': "off"})
        self.fields['supplier_dl'].widget.attrs.update({'class': 'textinput form-control setprice supplier_dl', 'autocomplete': "off"})
    
    class Meta:
        model = SupplierModel
        fields = ['supplier_name', 'supplier_location', 'supplier_gst', 'supplier_dl' ] 

class ClientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_name'].widget.attrs.update({'class': 'textinput form-control setprice client_name', 'required': 'true' , 'autocomplete': "off"})
        self.fields['client_location'].widget.attrs.update({'class': 'textinput form-control setprice client_location', 'required': 'true' , 'autocomplete': "off"})
        self.fields['client_gst'].widget.attrs.update({'class': 'textinput form-control setprice client_gst', 'autocomplete': "off"})
        self.fields['client_dl'].widget.attrs.update({'class': 'textinput form-control setprice client_dl', 'autocomplete': "off"})
    
    class Meta:
        model = ClientModel
        fields = ['client_name', 'client_location', 'client_gst', 'client_dl' ] 

class HSNCodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hsncode_pk'].widget.attrs.update({'class': 'textinput form-control setprice hsncode_pk', 'required': 'true'})
        self.fields['in_stock'].widget.attrs.update({'class': 'number form-control setprice in_stock', 'required': 'true'})
        self.fields['purchase_price'].widget.attrs.update({'class': 'number form-control setprice purchase_price', 'required': 'true'})
        self.fields['sell_price'].widget.attrs.update({'class': 'number form-control setprice sell_price', 'required': 'true'})

    class Meta:
        model = HSNCode
        fields = ['hsncode_pk','in_stock', 'purchase_price', 'sell_price']

class PurchaseBillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_date'].widget.attrs.update({'class': 'textinput form-control setprice purchase_date', 'required': 'true'})
        self.fields['supplier'].widget.attrs.update({'class': 'textinput form-control setprice supplier', 'required': 'true'})
        self.fields['payment_status'].widget.attrs.update({'class': 'form-select form-control setprice payment_status', 'min': '0', 'required': 'true'})

    class Meta:
        model = PurchaseBill
        fields = ['purchase_bill_pk', 'purchase_date', 'supplier', 'payment_status']

class PurchaseItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()
        self.fields['item'].widget.attrs.update({'class': 'form-select form-control setprice item', 'required': 'true'})
        self.fields['hsncode'].widget.attrs.update({'class': 'textinput form-control setprice hsncode', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['pprice'].widget.attrs.update({'class': 'textinput form-control setprice pprice', 'min': '0', 'required': 'true'})
        self.fields['sprice'].widget.attrs.update({'class': 'textinput form-control setprice sprice', 'min': '0', 'required': 'true'})

    class Meta:
        model = PurchaseItem
        fields = ['item', 'hsncode', 'quantity', 'pprice', 'sprice']

PurchaseItemFormset = formset_factory(PurchaseItemForm, extra=1)


class SellBillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sell_date'].widget.attrs.update({'class': 'textinput form-control setprice sell_date', 'required': 'true'})
        self.fields['client'].widget.attrs.update({'class': 'textinput form-control setprice client', 'required': 'true'})
        self.fields['payment_status'].widget.attrs.update({'class': 'form-select form-control setprice payment_status', 'min': '0', 'required': 'true'})

    class Meta:
        model = SellBill
        fields = ['sell_bill_pk', 'sell_date', 'client', 'payment_status']


class SellItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.all()
        self.fields['item'].widget.attrs.update({'class': 'form-select form-control setprice item', 'required': 'true'})
        self.fields['hsncode'].queryset = HSNCode.objects.filter()
        self.fields['hsncode'].widget.attrs.update({'class': 'form-select form-control setprice hsncode', 'required': 'true'})
        self.fields['quantity'].widget.attrs.update({'class': 'textinput form-control setprice quantity', 'min': '0', 'required': 'true'})
        self.fields['sprice'].widget.attrs.update({'class': 'textinput form-control setprice sprice', 'min': '0', 'required': 'true'})

    class Meta:
        model = SellItem
        fields = ['item', 'hsncode', 'quantity', 'sprice']

SellItemFormset = formset_factory(SellItemForm, extra=1)


