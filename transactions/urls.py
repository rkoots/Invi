from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('suppliers/new', views.SupplierCreateUpdateView.as_view(), name='new-supplier'),
    path('suppliers/<pk>/edit', views.SupplierCreateUpdateView.as_view(), name='edit-supplier'),
    path('suppliers/<pk>/delete', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('suppliers/<name>', views.SupplierView.as_view(), name='supplier'),

    path('purchases/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('purchases/new', views.SelectSupplierView.as_view(), name='select-supplier'), 
    path('purchases/new/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
    path('purchases/<pk>/delete', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    
    path('sales/', views.SaleView.as_view(), name='sales-list'),
    path('sales/new', views.SaleCreateView.as_view(), name='new-sale'),
    path('sales/<pk>/delete', views.SaleDeleteView.as_view(), name='delete-sale'),

    path("purchases/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path("sales/<billno>", views.SaleBillView.as_view(), name="sale-bill"),

    path('customers/', views.CustomerListView.as_view(), name='customers-list'),
    path('customers/new', views.CustomerCreateView.as_view(), name='new-customer'),
    path('customers/<pk>/edit', views.CustomerUpdateView.as_view(), name='edit-customer'),
    path('customers/<pk>/delete', views.CustomerDeleteView.as_view(), name='delete-customer'),
    path('customers/<name>', views.CustomerView.as_view(), name='customer'),

    path('demand/', views.DemandListView.as_view(), name='demand-list'),
    path('demand/new', views.DemandCreateView.as_view(), name='new-demand'),
    path('demand/<pk>/edit', views.DemandUpdateView.as_view(), name='edit-demand'),
    path('demand/<pk>/delete', views.DemandDeleteView.as_view(), name='delete-demand'),
    path('demand/<pk>', views.DemandView.as_view(), name='demand'),

    path('demand_to_quote/', views.DemandQuoteListView.as_view(), name='demand-quote-list'),
    path('quote/', views.QuoteListView.as_view(), name='quote-list'),
    path('quote/new', views.QuoteCreateView.as_view(), name='new-quote'),
    path('quote/<pk>/edit', views.QuoteUpdateView.as_view(), name='edit-quote'),
    path('quote/<pk>/delete', views.QuoteDeleteView.as_view(), name='delete-quote'),
    path('quote/<pk>', views.QuoteView.as_view(), name='quote'),
    path('quote/<int:pk>/update-status/<str:status>/', views.QuoteStatusUpdateView.as_view(), name='quote-update-status'),


]