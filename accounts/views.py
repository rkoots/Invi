from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import SupplierDetailsForm, UserRegistrationForm, SelectCustomer
from .models import Supplier_details, Customer
from django.views.generic import (View, ListView, CreateView, UpdateView, DeleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django_filters.views import FilterView
from .filters import CustomerFilter
from django.conf import settings
from django.apps import apps

model_str = settings.AUTH_USER_MODEL
app_label, model_name = model_str.split('.')
User = apps.get_model(app_label, model_name)



class CreateSupplier(SuccessMessageMixin, CreateView):
    model = Supplier_details
    form_class = SupplierDetailsForm
    template_name = "register_supplier.html"
    success_url = '/#login'  # Redirects to home page after submitting the form
    success_message = "Manufacturer account has been created successfully"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session_user_id"] = self.request.session.get('session_user_id')
        context["session_username"] = self.request.session.get('session_username')
        context["session_first_name"] = self.request.session.get('session_first_name')
        context["session_last_name"] = self.request.session.get('session_last_name')
        context["session_email"] = self.request.session.get('session_email')
        context["session_is_staff"] = self.request.session.get('session_is_staff')
        print(context)
        return context
    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        is_staff = request.POST.get('is_staff')
        if Customer.objects.filter(email=email).exists() \
            or Supplier_details.objects.filter(email=email).exists():
                form = UserRegistrationForm(request.POST)
        else:
            if User.objects.filter(email=email).exists():
                if is_staff=='1':
                    return redirect('register-supplier')
                else:
                    return redirect('register-customer')
            else:
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
    success_url = '/#login'
    success_message = "Customer has been created successfully"
    template_name = "register_customer.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session_user_id"] = self.request.session.get('session_user_id')
        context["session_username"] = self.request.session.get('session_username')
        context["session_first_name"] = self.request.session.get('session_first_name')
        context["session_last_name"] = self.request.session.get('session_last_name')
        context["session_email"] = self.request.session.get('session_email')
        context["session_is_staff"] = self.request.session.get('session_is_staff')
        context["title"] = 'New Customer'
        context["savebtn"] = 'Add Customer'
        return context



def ViewProfileDetails(request):
    context = {}
    print(request.user.is_staff)
    if request.user.is_staff:
        supplier = Supplier_details.objects.filter(user=request.user).first()
        if supplier:
            context['supplier'] = supplier
    else:
        customer = Customer.objects.filter(user=request.user.id).first()
        if customer:
            context['customer'] = customer
    return render(request, 'profile.html', context)




class CustomerListView(ListView,FilterView):
    model = Customer
    filterset_class = CustomerFilter
    template_name = "customer/customer_list.html"
    queryset = Customer.objects.filter(is_deleted=False)
    paginate_by = 5

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
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, 'customer/customer.html', {'customer' : customer})
