from django.shortcuts import render, redirect
from .forms import SupplierDetailsForm, UserRegistrationForm, SelectCustomer
from .models import Supplier_details
from transactions.models import Customer
from django.views.generic import (
    View,
    CreateView,
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin

class CreateSupplier(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Supplier_details                                                                       # setting 'Stock' model as model
    form_class = SupplierDetailsForm                                                              # setting 'StockForm' form as form
    template_name = "register_supplier.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Account has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["session_user_id"] = self.request.session.get('session_user_id')
        context["session_username"] = self.request.session.get('session_username')
        context["session_first_name"] = self.request.session.get('session_first_name')
        context["session_last_name"] = self.request.session.get('session_last_name')
        context["session_email"] = self.request.session.get('session_email')
        context["session_is_staff"] = self.request.session.get('session_is_staff')
        return context


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['session_user_id'] = user.id
            request.session['session_username'] = user.username
            request.session['session_first_name'] = user.first_name
            request.session['session_last_name'] = user.last_name
            request.session['session_is_staff'] = user.is_staff
            request.session['session_email'] = user.email
            if user.is_staff:
                return redirect('register-supplier')
            else:
                return redirect('register-customer')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_first.html', {'form': form})



class CreateCustomer(SuccessMessageMixin, CreateView):
    model = Customer
    form_class = SelectCustomer
    success_url = '/'
    success_message = "Customer has been created successfully"
    template_name = "register_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session_user_id"] = self.request.session.get('session_user_id')
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context


def ViewProfileDetails(request):
    context = {}
    print(request.user.is_staff)
    if request.user.is_staff:
        supplier = Supplier_details.objects.filter(user=request.user).first()
        print(supplier)
        if supplier:
            context['supplier'] = supplier
    else:
        customer = Customer.objects.filter(user=request.user).first()
        print(customer)
        if customer:
            context['customer'] = customer
    return render(request, 'profile.html', context)