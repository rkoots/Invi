from django.contrib import admin
from .models import (
    Supplier, 
    PurchaseBill, 
    PurchaseItem,
    PurchaseBillDetails, 
    SaleBill, 
    SaleItem,
    SaleBillDetails,
    Demand,
    Customer,
    Quote,
    Supplier_details,
    DemandParts

)

admin.site.register(Supplier)
admin.site.register(Supplier_details)
admin.site.register(DemandParts)
admin.site.register(PurchaseBill)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseBillDetails)
admin.site.register(SaleBill)
admin.site.register(SaleItem)
admin.site.register(SaleBillDetails)
admin.site.register(Demand)
admin.site.register(Customer)
admin.site.register(Quote)
