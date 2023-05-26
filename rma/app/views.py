from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from .models import Item, HSNCode, PurchaseItem, PurchaseBill, SellItem, SellBill
from .forms import ItemForm, HSNCodeForm, PurchaseItemForm, PurchaseBillForm, SellBillForm, SellItemForm, SellItemForm, PurchaseItemFormset, SellItemFormset
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from datetime import date, timedelta
from django.views import View
from django.forms import formset_factory
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.forms import inlineformset_factory

# Create your views here.
class Dashboard(View):
    def get(self, request, *args, **kwargs):
        total_purchase = PurchaseBill.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Calculate total sell amount
        total_sell = SellBill.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Calculate total profit
        total_profit = SellBill.objects.aggregate(Sum('total_profit'))['total_profit__sum'] or 0

        # Calculate daily purchase amount
        today = date.today()
        daily_total_purchase = PurchaseBill.objects.filter(purchase_date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Calculate daily sell amount
        daily_total_sell = SellBill.objects.filter(sell_date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # Calculate daily profit
        daily_total_profit = SellBill.objects.filter(sell_date=today).aggregate(Sum('total_profit'))['total_profit__sum'] or 0

        items = Item.objects.all()
        total_purchase_value = total_sell_value = 0
        for item in items:
            hsncodes = item.hsncodes.all()
            total_purchase_value += sum((hsncode.purchase_price*hsncode.in_stock) for hsncode in hsncodes)
            total_sell_value += sum((hsncode.sell_price*hsncode.in_stock) for hsncode in hsncodes)
        total_profit_value = total_sell_value - total_purchase_value
        
        context = {
            'daily_total_purchase': daily_total_purchase,
            'daily_total_sell': daily_total_sell,
            'daily_total_profit': daily_total_profit,
            'total_purchase': total_purchase,
            'total_sell': total_sell,
            'total_profit': total_profit,
            'total_purchase_value': total_purchase_value,
            'total_sell_value': total_sell_value,
            'total_profit_value': total_profit_value,
        }
        return render(request, 'app/dashboard.html', context=context)

class Purchase(APIView):
    def get(self, request, *args, **kwargs):
        purchase_bills = PurchaseBill.objects.all().order_by('-purchase_date', "-purchase_bill_pk")
        total_bills = purchase_bills.count()
        total_payments = pending_payments = paid_payments = paid_bills = pending_bills = 0
        for val in purchase_bills:
            total_payments += val.total_amount 
            if val.payment_status == 'Pending':
                pending_bills += 1
                pending_payments += val.total_amount
            else:
                paid_bills += 1
                paid_payments += val.total_amount

        context={
            'purchase_bills': purchase_bills,
            'total_bills': total_bills,
            'pending_bills': pending_bills,
            'paid_bills': paid_bills,
            'total_payments': total_payments,
            'pending_payments': pending_payments,
            'paid_payments': paid_payments,

        }

        return render(request, 'app/purchase.html', context=context)
    
class Sell(APIView):
    def get(self, request, *args, **kwargs):
        sell_bills = SellBill.objects.all().order_by('-sell_date', "-sell_bill_pk")
        total_bills = sell_bills.count()
        total_payments = pending_payments = paid_payments = total_profits = pending_profits = paid_profits = pending_bills = paid_bills = 0
        for val in sell_bills:
            total_payments += val.total_amount 
            if val.payment_status == 'Pending':
                pending_bills += 1
                pending_payments += val.total_amount
            else:
                paid_bills += 1
                paid_payments += val.total_amount
        
        for val in sell_bills:
            total_profits += val.total_profit 
            if val.payment_status == 'Pending':
                pending_profits += val.total_profit
            else:
                paid_profits += val.total_profit


        context={
            'sell_bills': sell_bills,
            'total_bills': total_bills,
            'paid_bills': paid_bills,
            'pending_bills': pending_bills,
            'total_payments': total_payments,
            'pending_payments': pending_payments,
            'paid_payments': paid_payments,
            'total_profits': total_profits,
            'pending_profits': pending_profits,
            'paid_profits': paid_profits,

        }

        return render(request, 'app/sell.html', context=context)
    
class ItemMaster(APIView):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        item_data = []
        total_purchase_value = total_sell_value = 0
        for item in items:
            hsncodes = item.hsncodes.all()
            stock_in = sum(hsncode.in_stock for hsncode in hsncodes)
            stock_value = sum(hsncode.stock_value for hsncode in hsncodes)
            total_purchase_value += sum((hsncode.purchase_price*hsncode.in_stock) for hsncode in hsncodes)
            total_sell_value += sum((hsncode.sell_price*hsncode.in_stock) for hsncode in hsncodes)
            item_data.append({
                'item_pk': item.item_pk,
                'item_name': item.item_name,
                'item_packaging_type': item.item_packaging_type,
                'stock_in': stock_in,
                'stock_value': stock_value,
            })
        total_profit = total_sell_value - total_purchase_value
        context={
            'item_data': item_data,
            'total_purchase_value': total_purchase_value,
            'total_sell_value': total_sell_value,
            'total_profit': total_profit,
        }

        return render(request, 'app/item_master.html', context=context)
    
class CreateItem(APIView):
    def get(self, request, *args, **kwargs):
        item_form = ItemForm()
        hsncode_form = HSNCodeForm()
        
        context={
            'item_form': item_form, 
            'hsncode_form': hsncode_form
        }
    
        return render(request, 'app/create_item.html', context=context)

    def post(self, request, *args, **kwargs):
        item_form = ItemForm(request.POST)
        hsncode_form = HSNCodeForm(request.POST)
        if item_form.is_valid() and hsncode_form.is_valid():
            item = item_form.save(commit=False)
            hsncode = hsncode_form.save(commit=False)
            hsncode.cal_stock_val()
            item.save()
            hsncode.save()
            item.hsncodes.set([hsncode])
            return redirect('item-master')
        
class UpdateItem(View):
    def get(self, request, item_pk, *args, **kwargs):
        product_form = ItemForm(instance=Item.objects.filter(item_pk = item_pk).first())
        context = {
            'item_pk': item_pk,
            'product_form': product_form,
        }
        return render(request, 'app/update_item.html', context = context)
    def post(self, request, item_pk, *args, **kwargs):
        product_form = ItemForm(request.POST)
        if product_form.is_valid():
            item_name = request.POST.get('item_name')
            item_low_stock_alert = request.POST.get('item_low_stock_alert')
            item_packaging_type = request.POST.get('item_packaging_type')
            item = Item.objects.get(item_pk = item_pk)
            item.item_name = item_name
            item.item_low_stock_alert = item_low_stock_alert
            item.item_packaging_type = item_packaging_type
            item.save()
            
            return redirect('item-master')
        else:
            product_form = ItemForm(instance=Item.objects.filter(item_pk = item_pk).first())
            context = {
                'item_pk': item_pk,
                'product_form': product_form,
            }
            return render(request, 'app/update_item.html', context = context)


class UpdateStock(View):
    def get(self, request, item_pk, hsncode_pk, purchase_price, *args, **kwargs):
        hsncode_form = HSNCodeForm(instance=HSNCode.objects.filter(hsncode_pk=hsncode_pk, purchase_price = purchase_price).first())
        context = {
            'item_pk': item_pk,
            'hsncode_form': hsncode_form,
        }
        return render(request, 'app/update_stock.html', context = context)
    def post(self, request, item_pk, *args, **kwargs):
        hsncode_form = HSNCodeForm(request.POST)
        if hsncode_form.is_valid():
            hsncode_pk = request.POST.get('hsncode_pk')
            in_stock = request.POST.get('in_stock')
            purchase_price = request.POST.get('purchase_price')
            sell_price = request.POST.get('sell_price')
            hsncode = HSNCode.objects.get(hsncode_pk = hsncode_pk)
            hsncode.hsncode_pk = hsncode_pk
            hsncode.in_stock = in_stock
            hsncode.purchase_price = purchase_price
            hsncode.sell_price = sell_price
            hsncode.stock_value = (int(in_stock)*int(purchase_price))
            hsncode.save()
            
            return redirect('item-master')
        else:
            hsncode_form = HSNCodeForm(instance=HSNCode.objects.filter(hsncode_pk=hsncode_pk, purchase_price = purchase_price).first())
            context = {
                'item_pk': item_pk,
                'hsncode_form': hsncode_form,
            }
            return render(request, 'app/update_stock.html', context = context)
class DeleteItem(View):
    def get(self, request, item_pk, *args, **kwargs):
        item = Item.objects.get(item_pk=item_pk)
        for hsncode in item.hsncodes.all():
            hsncode_obj = HSNCode.objects.filter(hsncode_pk=hsncode.hsncode_pk).first()
            hsncode_obj.delete()
        item.delete()
        
        return redirect('item-master')
class DeleteStock(View):
    def get(self, request, item_pk, hsncode_pk, purchase_price, *args, **kwargs):
        hsncode = HSNCode.objects.filter(hsncode_pk=hsncode_pk, purchase_price = purchase_price).first()
        hsncode.delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class ItemDetails(APIView):
    def get(self, request, pk, *args, **kwargs):
        item = Item.objects.get(item_pk=pk)
        
        context={
            'item': item
            }
        
        return render(request, 'app/item_details.html',context=context)
    
class AddStock(APIView):
    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        hsncode_form = HSNCodeForm()
        
        context={
            'items': items, 
            'hsncode_form': hsncode_form
        }
    
        return render(request, 'app/add_stock.html', context=context)
    def post(self, request, *args, **kwargs):
        item_pk = request.POST.get('product')
        item = Item.objects.get(item_pk=item_pk)
        hsncode_form = HSNCodeForm(request.POST)
        if hsncode_form.is_valid():
            hsncode = hsncode_form.save(commit=False)
            hsncode.cal_stock_val()
            hsncode.save()
            hsncodes = []
            for hsncode_value in item.hsncodes.all():
                hsncodes.append(hsncode_value)
            hsncodes.append(hsncode)
            item.hsncodes.set(hsncodes)
            return redirect('item-master')
        return HttpResponse("Hello world post")
    

class ViewPurchaseBill(APIView):
    def get(self, request, pk, *args, **kwargs):
        purchase_bill = get_object_or_404(PurchaseBill, pk=pk)
        bill_items_raw = PurchaseItem.objects.filter(purchase_bill=purchase_bill)
        bill_items = []
        for item in bill_items_raw:
            bill_items.append({
                'item': item.item,
                'hsncode': item.hsncode,
                'quantity': item.quantity,
                'pprice': item.pprice,
                'sprice': item.sprice
            })
        context = {
            'purchase_bill': purchase_bill,
            'bill_items': bill_items,
        }
        return render(request, 'app/bill_details.html', context=context)
    

class CreateSellBill(APIView):

    def get(self, request, *args, **kwargs):
        sell_form = SellBillForm()
        sell_item_form = SellItemForm(prefix='sell_item')
        context = {
            'sell_form': sell_form,
            'sell_item_form': sell_item_form,
        }
        return render(request, 'app/create_sell_bill.html', context=context)

    def post(self, request, *args, **kwargs):
        sell_form = SellBillForm(request.POST)
        sell_item_form = SellItemForm(request.POST, prefix='sell_item')
        if sell_form.is_valid():
            sell_bill = sell_form.save()
            sell_items = sell_item_form.save(commit=False)

            for form in sell_items:
                form.sell_bill = sell_bill
                form.save()

            return redirect('sell')
        else:
            print(sell_item_form.errors)

        context = {
            'sell_form': sell_form,
            'sell_item_form': sell_item_form
        }
        return render(request, 'app/create_sell_bill.html', context=context)
    

class ViewSellBill(APIView):
    def get(self, request, pk, *args, **kwargs):
        sell_bill = get_object_or_404(SellBill, pk=pk)
        bill_items_raw = SellItem.objects.filter(sell_bill=sell_bill)
        bill_items = []
        for item in bill_items_raw:
            bill_items.append({
                'item': item.item,
                'hsncode': item.hsncode,
                'quantity': item.quantity,
                'sprice': item.sprice,
                'profit': item.profit,
            })
        context = {
            'sell_bill': sell_bill,
            'bill_items': bill_items,
        }
        return render(request, 'app/sell_bill_details.html', context=context)
    
class CreatePurchaseBillView(View):
    def get(self, request, *args, **kwargs):
        purchase_bill_form = PurchaseBillForm()
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'purchase_bill_form': purchase_bill_form,
            'formset': formset
        }
        return render(request, 'app/create_purchase_bill.html', context)
    def post(self, request, *args, **kwargs):
        purchase_bill_form = PurchaseBillForm(request.POST)
        formset = PurchaseItemFormset(request.POST)
        total_amount = 0
        print(formset)
        if purchase_bill_form.is_valid() and formset.is_valid():
            purchase_bill = purchase_bill_form.save()

            for form in formset: 
                item = form.cleaned_data['item']
                hsncode = form.cleaned_data['hsncode']
                quantity = form.cleaned_data['quantity']
                pprice = form.cleaned_data['pprice']
                sprice = form.cleaned_data['sprice']
                total_amount += (quantity*pprice)
                purchase_item = PurchaseItem.objects.create(purchase_bill=purchase_bill, item=item, hsncode=hsncode, quantity=quantity, pprice=pprice, sprice=sprice)
                purchase_item.save()

                
                try:
                    item_obj = Item.objects.get(item_name=item)
                except Item.DoesNotExist:
                    item_obj = Item.objects.create(item_name=item)
                hsncode_obj = HSNCode.objects.filter(hsncode_pk=hsncode).first()

                if hsncode_obj is None:
                    hsncode_obj = HSNCode.objects.create(hsncode_pk=hsncode, in_stock=quantity, purchase_price=pprice, sell_price=sprice)
                else:
                    if hsncode_obj.purchase_price == pprice and hsncode_obj.sell_price == sprice:
                        hsncode_obj.in_stock += quantity
                        hsncode_obj.save()
                    else:
                        new_hsncode_obj = HSNCode.objects.create(hsncode_pk=hsncode, in_stock=quantity, purchase_price=pprice, sell_price=sprice)
                        item_obj.hsncodes.add(new_hsncode_obj)
                        
                hsncode_present = item_obj.hsncodes.filter(hsncode_pk=hsncode).exists()
                if hsncode_present:
                    pass
                else:
                    item_obj.hsncodes.add(hsncode_obj)
            
            purchase_bill.total_amount = total_amount
            purchase_bill.save()
            
            return redirect('purchase')
        
        context = {
            'purchase_bill_form': purchase_bill_form,
            'formset': formset,
        }

        return render(request, 'app/create_purchase_bill.html', context)
    

class CreateSellBillView(View):

    def get(self, request, *args, **kwargs):
        sell_bill_form = SellBillForm()
        formset = SellItemFormset(request.GET or None)
        context = {
            'sell_bill_form': sell_bill_form,
            'formset': formset
        }
        return render(request, 'app/create_sell_bill.html', context)
    
    def post(self, request, *args, **kwargs):
        sell_bill_form = SellBillForm(request.POST)
        formset = SellItemFormset(request.POST)
        total_amount = total_profit = 0
        if sell_bill_form.is_valid() and formset.is_valid():
            sell_bill = sell_bill_form.save()
            for form in formset: 
                item = form.cleaned_data['item']
                hsncode_instance = form.cleaned_data['hsncode']
                hsncode = str(form.cleaned_data['hsncode'])[:5]
                quantity = form.cleaned_data['quantity']
                sprice = form.cleaned_data['sprice']
                total_amount += (quantity*sprice)
                pprice = int(HSNCode.objects.filter(hsncode_pk = hsncode).values_list('purchase_price', flat=True).first())
                total_profit += (sprice-pprice)*quantity
                sell_item = SellItem.objects.create(sell_bill=sell_bill, item=item, hsncode=hsncode_instance, quantity=quantity, sprice=sprice)
                sell_item.profit = (sprice-pprice)*quantity
                sell_item.save()

                hsncode_obj = HSNCode.objects.filter(hsncode_pk=hsncode).first()
                hsncode_obj.in_stock -= quantity
                hsncode_obj.cal_stock_val()
                hsncode_obj.save()
                    
            sell_bill.total_amount = total_amount
            sell_bill.total_profit = total_profit
            sell_bill.save()
            
            return redirect('sell')
        
        context = {
            'sell_bill_form': sell_bill_form,
            'formset': formset,
        }

        return render(request, 'app/create_sell_bill.html', context)
    

class DeletePurchaseBillView(View):
    def get(self, request, pk, *args, **kwargs):
        purchase_bill = PurchaseBill.objects.get(purchase_bill_pk = pk)
        purchase_items = PurchaseItem.objects.filter(purchase_bill=purchase_bill)
        for purchase_item in purchase_items:
            hsncode = HSNCode.objects.filter(hsncode_pk = purchase_item.hsncode, purchase_price = purchase_item.pprice, sell_price = purchase_item.sprice).first()
            hsncode.in_stock -= purchase_item.quantity 
            hsncode.cal_stock_val()
            hsncode.save()
        purchase_bill.delete()
        
        return redirect('purchase')
    
class UpdateSellBillView(View):
    def get(self, request, pk, *args, **kwargs):
        return redirect('sell')

class DeleteSellBillView(View):
    def get(self, request, pk, *args, **kwargs):
        sell_bill = SellBill.objects.get(sell_bill_pk = pk)
        sell_items = SellItem.objects.filter(sell_bill=sell_bill)
        for sell_item in sell_items:
            hsncode = HSNCode.objects.filter(hsncode_pk = sell_item.hsncode.hsncode_pk).first()
            hsncode.in_stock += sell_item.quantity 
            hsncode.cal_stock_val()
            hsncode.save()
        sell_bill.delete()
        return redirect('sell')
    

#Plotting line graph to show the sells of the month
@method_decorator(never_cache, name='dispatch')
class LineChartJSONView(BaseLineChartView):
    today = date.today()

    day_of_month = today.replace(day=1)
    first_day = today.replace(day=1)
    last_day = today.replace(day=1, month=today.month % 12 + 1) - timedelta(days=1)

    dates = []
    purchase_value_on_date = []
    sell_value_on_date = []

    sell_bills = SellBill.objects.filter(sell_date__range=[first_day, last_day]).values('sell_date').annotate(total_sell_value=Sum('total_amount')).order_by('sell_date')
    purchase_bills = PurchaseBill.objects.filter(purchase_date__range=[first_day, last_day]).values('purchase_date').annotate(total_purchase_value=Sum('total_amount')).order_by('purchase_date')

    for i in range(1, 30):
        dates.append(str(day_of_month))
        for sell_bill in sell_bills:
            if str(sell_bill['sell_date']) == str(day_of_month):
                val = int(sell_bill['total_sell_value'])
                break
            else:
                val = 0
        sell_value_on_date.append(val)

        for purchase_bill in purchase_bills:
            if str(purchase_bill['purchase_date']) == str(day_of_month):
                val = int(purchase_bill['total_purchase_value'])
                break
            else:
                val = 0
        purchase_value_on_date.append(val)

        day_of_month = day_of_month.replace(day=(i+1))

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return self.dates

    def get_providers(self):
        """Return names of datasets."""
        return ["Purchase", "Sell"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [self.purchase_value_on_date, self.sell_value_on_date]
    
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    


@never_cache
def pie_chart_json(request):
    # Retrieve all sell items
    sell_items = SellItem.objects.all()

    # Calculate the total quantity sold for each item
    items_list = {}
    for sell_item in sell_items:
        item_name = sell_item.item.item_name
        quantity = sell_item.quantity
        items_list[item_name] = items_list.get(item_name, 0) + quantity

    # Sort the items based on the total quantity sold
    sorted_items = sorted(items_list.items(), key=lambda x: x[1], reverse=True)

    # Select the top ten sold items
    top_items = sorted_items[:10]

    # Prepare data for the chart
    labels = [item[0] for item in top_items]
    quantities = [item[1] for item in top_items]

    # Create a dictionary containing the chart data
    data = {
        'labels': labels,
        'datasets': [{
            'data': quantities,
            'backgroundColor': [
                '#FF6384',
                '#36A2EB',
                '#FFCE56',
                '#8E5EA2',
                '#3cba9f',
                '#e8c3b9',
                '#c45850',
                '#d9e8f3',
                '#cdcec6',
                '#b6d7a8'
            ],
        }]
    }

    # Return the JSON response with cache control headers
    response = JsonResponse(data)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


class UpdatePurchaseBillView(View):
    def get(self, request, pk, *args, **kwargs):
        purchase_bill = PurchaseBill.objects.get(pk=pk)
        item_ids = purchase_bill.purchaseitem_set.values_list('item_id', flat=True)
        print(item_ids)
        for item_id in item_ids:
            purchase_bill.items.add(item_id)
        print(purchase_bill.items)
        purchase_bill_form = PurchaseBillForm(instance=purchase_bill)
        PurchaseItemFormset = inlineformset_factory(PurchaseBill, PurchaseItem, form=PurchaseItemForm, extra=0)
        formset = PurchaseItemFormset(instance=purchase_bill)
        context = {
            'purchase_bill': purchase_bill,
            'purchase_bill_form': purchase_bill_form,
            'formset': formset
        }
        return render(request, 'app/update_purchase_bill.html', context)

    def post(self, request, pk, *args, **kwargs):
        purchase_bill = get_object_or_404(PurchaseBill, purchase_bill_pk=pk)
        purchase_bill_form = PurchaseBillForm(request.POST, instance=purchase_bill)
        PurchaseItemFormset = inlineformset_factory(PurchaseBill, PurchaseItem, form=PurchaseItemForm, extra=0)
        formset = PurchaseItemFormset(request.POST, instance=purchase_bill)
        
        total_amount = 0
        #print(purchase_bill_form.is_valid(), formset.is_valid())
        #print(formset)
        #print(formset.errors)

        if purchase_bill_form.is_valid() and formset.is_valid():
            updated_purchase_bill = purchase_bill_form.save()

            for form in formset:
                item = form.cleaned_data['item']
                hsncode = form.cleaned_data['hsncode']
                quantity = form.cleaned_data['quantity']
                pprice = form.cleaned_data['pprice']
                sprice = form.cleaned_data['sprice']
                total_amount += (quantity * pprice)

                purchase_item, created = PurchaseItem.objects.get_or_create(purchase_bill=updated_purchase_bill, item=item, hsncode=hsncode)
                purchase_item.quantity = quantity
                purchase_item.pprice = pprice
                purchase_item.sprice = sprice
                purchase_item.save()

                # Update HSNCode and Item if necessary
                item_obj, created = Item.objects.get_or_create(item_name=item)
                hsncode_obj, created = HSNCode.objects.get_or_create(hsncode_pk=hsncode)
                hsncode_obj.in_stock += quantity
                hsncode_obj.purchase_price = pprice
                hsncode_obj.sell_price = sprice
                hsncode_obj.save()

                if not item_obj.hsncodes.filter(hsncode_pk=hsncode).exists():
                    item_obj.hsncodes.add(hsncode_obj)

            updated_purchase_bill.total_amount = total_amount
            updated_purchase_bill.save()

            return redirect('purchase')

        context = {
            'purchase_bill': purchase_bill,
            'purchase_bill_form': purchase_bill_form,
            'formset': formset,
        }
        return render(request, 'app/update_purchase_bill.html', context)