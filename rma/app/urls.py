from django.contrib import admin
from django.urls import path, include
from .views import Dashboard, Purchase, Sell, ItemMaster, CreateItem, UpdateItem, UpdateClient, DeleteClient, UpdateSupplier, DeleteSupplier, SellBillList, CreateSupplier, CreateClient, PurchaseBillList, Supplier, Client, UpdateStock,ItemDetails,ItemInventory, AddStock, CreatePurchaseBillView, ViewPurchaseBill, CreateSellBillView, ViewSellBill, DeleteItem, DeleteStock, UpdateSellBillView, DeleteSellBillView, UpdatePurchaseBillView, DeletePurchaseBillView
from .views import LineChartJSONView, pie_chart_json, backup_database
urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('item-master', ItemMaster.as_view(), name='item-master'),
    path('item-inventory', ItemInventory.as_view(), name='item-inventory'),


    path('item-master/create', CreateItem.as_view(), name='create-item'),
    path('add-stock', AddStock.as_view(), name='add-stock'),

    path('item-master/item-detail/<int:item_pk>/update', UpdateItem.as_view(), name='update-item'),
    path('item-master/item-detail/<int:item_pk>/update/<str:hsncode_pk>/<int:purchase_price>/', UpdateStock.as_view(), name='update-stock'),

    path('item-master/item-detail/<int:item_pk>/delete', DeleteItem.as_view(), name='delete-item'),
    path('item-master/item-detail/<int:item_pk>/delete/<str:hsncode_pk>/<int:purchase_price>/', DeleteStock.as_view(), name='delete-stock'),

    path('item-master/item-detail/<int:pk>/', ItemDetails.as_view(), name='item-details'),

    path('sell', Sell.as_view(), name='sell'),
    path('sell-list', SellBillList.as_view(), name='sell-bill-list'),
    path('sell/create', CreateSellBillView.as_view(),name="create-sell-bill"),
    path('sell/update/<int:pk>/', UpdateSellBillView.as_view(),name="update-sell-bill"),
    path('sell/delete/<int:pk>/', DeleteSellBillView.as_view(),name="delete-sell-bill"),
    path('sell/create/<int:pk>/', ViewSellBill.as_view(),name="sell-bill-details"),
    

    path('purchase', Purchase.as_view(), name='purchase'),
    path('purchase-list', PurchaseBillList.as_view(), name='purchase-bill-list'),
    path('purchase/create', CreatePurchaseBillView.as_view(),name="create-purchase-bill"),
    path('purchase/update/<int:pk>/', UpdatePurchaseBillView.as_view(),name="update-purchase-bill"),
    path('purchase/delete/<int:pk>/', DeletePurchaseBillView.as_view(),name="delete-purchase-bill"),
    path('purchase/create/<int:pk>/', ViewPurchaseBill.as_view(),name="purchase-bill-details"),


    path('chartJSON', LineChartJSONView.as_view(), name='line_chart_json'),
    path('chart/pie', pie_chart_json, name='pie_chart_json'),

    path('backup_database/', backup_database, name='backup_database'),

    path('supplier/', Supplier.as_view(), name='supplier'),
    path('supplier/create', CreateSupplier.as_view(), name='create-supplier'),
    path('supplier/update/<int:supplier_id>/', UpdateSupplier.as_view(), name='update-supplier'),
    path('supplier/delete/<int:supplier_id>/', DeleteSupplier.as_view(), name='delete-supplier'),


    
    path('client/', Client.as_view(), name='client'),
    path('client/create', CreateClient.as_view(), name='create-client'),
    path('update-client/<int:client_id>/', UpdateClient.as_view(), name='update-client'),
    path('delete-client/<int:client_id>/', DeleteClient.as_view(), name='delete-client'),



]
