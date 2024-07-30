from django.shortcuts import render, redirect, get_object_or_404
from .forms import SupplierDetailsForm, UserRegistrationForm, SelectCustomer
from .models import Supplier_details
from transactions.models import Customer
from django.views.generic import (
    View,
    CreateView,
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin

class CreateSupplier(SuccessMessageMixin, CreateView):
    model = Supplier_details
    form_class = SupplierDetailsForm
    template_name = "register_supplier.html"
    success_url = '/'  # Redirects to home page after submitting the form
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