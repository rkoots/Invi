import os,sys
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PurchaseBill, 
    Supplier, 
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,  
    SaleItem,
    SaleBillDetails,
    Customer,
    Demand,
    Quote,
    DemandParts
)
from accounts.models import (
    Supplier_details
)

from .forms import (
    SelectSupplierForm, 
    PurchaseItemFormset,
    PurchaseDetailsForm, 
    SupplierForm, 
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm,
    SelectCustomer,
    SelectDemand,
    SelectQuote,
    DemandPartsForm
)
from inventory.models import Stock
from django.db.models import Count
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.forms import formset_factory
from django.utils import timezone

class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter()
    paginate_by = 10

class SupplierCreateUpdateView(SuccessMessageMixin, CreateView, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    template_name = "suppliers/edit_supplier.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if we are in edit mode
        if 'pk' in self.kwargs:
            context["title"] = 'Edit Supplier'
            context["savebtn"] = 'Save Changes'
            context["delbtn"] = 'Delete Supplier'
            self.success_message = "Manufacturer details have been updated successfully"
        else:
            context["title"] = 'New Manufacturer'
            context["savebtn"] = 'Add Manufacturer'
            self.success_message = "Manufacturer has been created successfully"
        # Add session data to context
        context["session_user_id"] = self.request.session.get('session_user_id')
        context["session_username"] = self.request.session.get('session_username')
        context["session_first_name"] = self.request.session.get('session_first_name')
        context["session_last_name"] = self.request.session.get('session_last_name')
        context["session_email"] = self.request.session.get('session_email')
        context["session_is_staff"] = self.request.session.get('session_is_staff')
        return context

    def get_object(self, queryset=None):
        # Return the object for updating if pk is present
        if 'pk' in self.kwargs:
            return get_object_or_404(Supplier, pk=self.kwargs['pk'])
        return None  # For create view

    def form_valid(self, form):
        response = super().form_valid(form)
        # Clear the session data after successful form submission
        for key in ['session_user_id', 'session_username', 'session_first_name', 'session_last_name', 'session_is_staff']:
            if key in self.request.session:
                del self.request.session[key]
        return response


# used to delete a supplier
class SupplierDeleteView(View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Manufacturer has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()                                               
        messages.success(request, self.success_message)
        return redirect('suppliers-list')

# used to view a supplier's profile
class SupplierView(View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier'  : supplierobj,
            'bills'     : bills
        }
        return render(request, 'suppliers/supplier.html', context)

    # shows the list of bills of all purchases
class PurchaseView(ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10

# used to select the supplier
class SelectSupplierView(View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})

# used to generate a bill object and save items
class PurchaseCreateView(View):                                                 
    template_name = 'purchases/new_purchase.html'

    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)                      # renders an empty formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)                             # recieves a post method for the formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        if formset.is_valid():
            # saves bill
            billobj = formset.save(commit=False)
            billobj.save()

            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()


            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)       # gets the item
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity += billitem.quantity                             # updates quantity
                billdetailsobj.total += billitem.totalprice
                # saves bill item and stock
                stock.save()
                billitem.save()

            billdetailsobj.save()
            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj
        }
        return render(request, self.template_name, context)

# used to delete a bill object
class PurchaseDeleteView(SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Purchase bill has been deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)

# shows the list of bills of all sales 
class SaleView(ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10

# used to generate a bill object and save items
class SaleCreateView(View):                                                      
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)                          # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)                                 # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            try:
                billobj = form.save(commit=False)
                billobj.save()

            except Exception as exc:
                print('Exception error! ',exc)
                context = {
                    'form'      : form,
                    'formset'   : formset,
                }
                return render(request, self.template_name, context)
            
            try:
                # create bill details object
                billdetailsobj = SaleBillDetails(billno=billobj)
                billdetailsobj.save()

            except Exception as exc:
                print('Exception error! ',exc)
                # Removing purchase transaction to keep transaction data clean
                billobj.delete()
                context = {
                    'form'      : form,
                    'formset'   : formset,
                }
                return render(request, self.template_name, context)

            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)      
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.quantity
                # updates quantity in stock db
                stock.quantity -= billitem.quantity
                billdetailsobj.total += billitem.totalprice 
                # saves bill item and stock
                stock.save()
                billitem.save()

            billdetailsobj.save()
            messages.success(request, "Sold items have been registered successfully")
            return redirect('sale-bill', billno=billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)

# used to delete a bill object
class SaleDeleteView(SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Sale bill has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)

# used to display the purchase bill object
class PurchaseBillView(View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    def get(self, request, billno):
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = PurchaseDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = PurchaseBillDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : PurchaseBill.objects.get(billno=billno),
            'items'         : PurchaseItem.objects.filter(billno=billno),
            'billdetails'   : PurchaseBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

# used to display the sale bill object
class SaleBillView(View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html"
    
    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)

    def post(self, request, billno):
        form = SaleDetailsForm(request.POST)
        if form.is_valid():
            billdetailsobj = SaleBillDetails.objects.get(billno=billno)
            
            billdetailsobj.eway = request.POST.get("eway")    
            billdetailsobj.veh = request.POST.get("veh")
            billdetailsobj.destination = request.POST.get("destination")
            billdetailsobj.po = request.POST.get("po")
            billdetailsobj.cgst = request.POST.get("cgst")
            billdetailsobj.sgst = request.POST.get("sgst")
            billdetailsobj.igst = request.POST.get("igst")
            billdetailsobj.cess = request.POST.get("cess")
            billdetailsobj.tcs = request.POST.get("tcs")
            billdetailsobj.total = request.POST.get("total")

            billdetailsobj.save()
            messages.success(request, "Bill details have been modified successfully")
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }
        return render(request, self.template_name, context)



class CustomerListView(ListView):
    model = Customer
    template_name = "customer/customer_list.html"
    queryset = Customer.objects.filter(is_deleted=False)
    paginate_by = 10

class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = SelectCustomer
    success_url = '/transactions/customers'
    success_message = "Customer has been created successfully"
    template_name = "customer/edit_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context

class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = SelectCustomer
    success_url = '/transactions/customers'
    success_message = "Customer details has been updated successfully"
    template_name = "customer/edit_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Customer'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Customer'
        return context

class CustomerDeleteView(View):
    template_name = "customer/delete_customer.html"
    success_message = "Customer Record has been deleted successfully"

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, self.template_name, {'object' : customer})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.is_deleted = True
        customer.save()
        messages.success(request, self.success_message)
        return redirect('customers-list')

class CustomerView(View):
    def get(self, request, name):
        customer = get_object_or_404(Customer, Name=name)
        return render(request, 'customer/customer.html', {'customer' : customer})




class DemandListView(LoginRequiredMixin, ListView):
    model = Demand
    template_name = "demand/demand_list.html"
    paginate_by = 10
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Demand.objects.filter(end_date__gte=timezone.now(), quote_id=0, is_deleted=False)
        else:
            return Demand.objects.filter(user=user, is_deleted=False)





class DemandCreateView(SuccessMessageMixin, CreateView):
    model = Demand
    form_class = SelectDemand
    template_name = "demand/edit_demand.html"
    success_url = '/transactions/demand'
    success_message = "RFQ has been created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New RFQ'
        context["savebtn"] = 'Add RFQ'
        PartFormSet = formset_factory(DemandPartsForm, extra=1)
        context["formset"] = PartFormSet()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Save the Demand instance
            demand = form.save()

            # Handle the DemandParts forms
            num_parts = int(request.POST.get('parts', 0))
            print("hererere == ",num_parts)
            PartFormSet = formset_factory(DemandPartsForm, extra=num_parts)
            print(PartFormSet)
            parts_formset = PartFormSet(request.POST, request.FILES)
            print(parts_formset)
            if parts_formset.is_valid():
                for part_form in parts_formset:
                    if part_form.cleaned_data:
                        part = part_form.save(commit=False)
                        part.demand = demand
                        part.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)



class DemandUpdateView(SuccessMessageMixin, UpdateView):
    model = Demand
    form_class = SelectDemand
    success_url = '/transactions/demand'
    success_message = "RFQ details has been updated successfully"
    template_name = "demand/edit_demand.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Demand'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Demand'
        return context

class DemandDeleteView(View):
    template_name = "demand/delete_demand.html"
    success_message = "Demand Record has been deleted successfully"
    def get(self, request, pk):
        demand = get_object_or_404(Demand, pk=pk)
        return render(request, self.template_name, {'object' : demand})

    def post(self, request, pk):
        demand = get_object_or_404(Demand, pk=pk)
        demand.is_deleted = True
        demand.save()
        messages.success(request, self.success_message)
        return redirect('demand-list')

class DemandView(View):
    def get(self, request, pk):
        demand = get_object_or_404(Demand, pk=pk)
        #demanddetails = DemandParts.objects.filter(demand=demand).all()
        quote = Quote.objects.filter(demand=demand)
        btn_class = 'ghost-blue'
        return render(request, 'demand/demand.html', {'demand' : demand, 'quotes' : quote, 'btn_class' : btn_class})

class QuoteListView(ListView):
    model = Quote
    template_name = "quote/quote_list.html"
    queryset = Quote.objects.filter(is_deleted=False)
    paginate_by = 10

class QuoteCreateView(SuccessMessageMixin, CreateView):
    model = Quote
    form_class = SelectQuote
    success_url = '/transactions/quote'
    success_message = "Quatation has been created successfully"
    template_name = "quote/edit_quote.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Quote'
        context["savebtn"] = 'Add Quote'
        return context

class QuoteUpdateView(SuccessMessageMixin, UpdateView):
    model = Quote
    form_class = SelectQuote
    success_url = '/transactions/quote'
    success_message = "Qutation details has been updated successfully"
    template_name = "quote/edit_quote.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Quote'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Quote'
        return context

class QuoteDeleteView(View):
    template_name = "quote/delete_quote.html"
    success_message = "Quotation has been deleted successfully"
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        return render(request, self.template_name, {'object' : quote})

    def post(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        #quote.is_deleted = True
        quote.save()
        messages.success(request, self.success_message)
        return redirect('quote-list')

class QuoteView(View):
    def get(self, request, pk):
        quote = get_object_or_404(Quote, pk=pk)
        return render(request, 'quote/quote.html', {'quote': quote})

class DemandQuoteListView(ListView):
    model = Demand
    template_name = "demand/demand_list.html"
    queryset = Demand.objects.annotate(quote_count=Count('quote')).filter(quote_count__gt=0)
    paginate_by = 10

class QuoteStatusUpdateView(ListView):
    def get(self, request, pk, status):
        quote = get_object_or_404(Quote, pk=pk)
        btn_class = 'ghost-green'
        if status == 'Approved':
            quote.status = 'Approved'
        elif status == 'Rejected':
            quote.status = 'Rejected'
            btn_class = 'ghost-red'
        quote.save()
        context = {
            'demand': quote.demand,  # Assuming demand is related to Quote
            'quote': quote,
            'btn_class' : btn_class,
        }
        return render(request, 'demand/demand.html', context)

