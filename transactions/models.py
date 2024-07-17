from django.db import models
from inventory.models import Stock

# Contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchasesupplier')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Bill no: " + str(self.billno)
    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)
    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = sum(item.totalprice for item in purchaseitems)
        return total

# Contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchasebillno')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='purchaseitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

# Contains the other details in the purchases bill
class PurchaseBillDetails(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete=models.CASCADE, related_name='purchasedetailsbillno')
    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno)

# Contains the sale bills made
class SaleBill(models.Model):
    billno = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)

    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = sum(item.totalprice for item in saleitems)
        return total

# Contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='saleitem')
    quantity = models.IntegerField(default=1)
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

# Contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete=models.CASCADE, related_name='saledetailsbillno')
    eway = models.CharField(max_length=50, blank=True, null=True)
    veh = models.CharField(max_length=50, blank=True, null=True)
    destination = models.CharField(max_length=50, blank=True, null=True)
    po = models.CharField(max_length=50, blank=True, null=True)
    cgst = models.CharField(max_length=50, blank=True, null=True)
    sgst = models.CharField(max_length=50, blank=True, null=True)
    igst = models.CharField(max_length=50, blank=True, null=True)
    cess = models.CharField(max_length=50, blank=True, null=True)
    tcs = models.CharField(max_length=50, blank=True, null=True)
    total = models.IntegerField(default=0)

    def __str__(self):
        return "Bill no: " + str(self.billno.billno)


# Contains customers
class Customer(models.Model):
    BUSINESS_TYPES = [
        ('electronics', 'Electronics'),
        ('infrastructure', 'Infrastructure'),
        ('custom_machinery', 'Custom Machinery'),
        ('Others', 'Others'),
    ]
    id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=75, blank=False, null=False)
    type_of_business = models.CharField(max_length=50, choices=BUSINESS_TYPES)
    Address = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    EORI_number = models.CharField(max_length=50, unique=True)
    VAT_number = models.CharField(max_length=50, unique=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} - {self.Name}"

# Contains demands
class Demand(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    part_name = models.CharField(max_length=30, verbose_name='Name')
    Part_desc = models.CharField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='demand_files/', blank=True, null=True)
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demand #{self.id} - {self.customer.Name}"

class Quote(models.Model):
    QUOTE_STATUS = [
        ('Approved', 'Approved'),
        ('Hold', 'Hold'),
        ('Rejected', 'Rejected'),
    ]
    id = models.AutoField(primary_key=True)
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='demand_supplier')
    quote_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    note = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True ,choices=QUOTE_STATUS)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demand #{self.id} - {self.demand.part_name}"

