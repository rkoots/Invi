from django import forms
from .models import Supplier_details
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from transactions.models import Customer
from django import forms
from .models import Supplier_details

class UserRegistrationForm(UserCreationForm):
    is_staff = forms.ChoiceField(choices=[(1, 'Supplier'), (0, 'Buyer')], widget=forms.RadioSelect)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email','is_staff']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class SupplierDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['companyname'].initial = 'Default Company Name'
        self.fields['phone'].widget.attrs.update({'readonly': 'readonly'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Enter your address here'})
        if 'company_street' in self.fields:
            self.fields['company_street'].widget = forms.HiddenInput()
        user = kwargs.pop('user', None)
        print(user,kwargs)
    class Meta:
        model = Supplier_details
        fields = [
            'user', 'companyname', 'phone', 'address', 'city', 'state', 'country',
            'activity_type', 'company_street', 'company_postalcode', 'company_city',
            'company_url', 'production_area', 'manufacturing_competency1', 'manufacturing_competency2',
            'info_source', 'amount_of_employees', 'turnover_per_year', 'certificates'
        ]
        widgets = {
            'user': forms.HiddenInput(),  # Hide the supplier field if you set it programmatically
            'activity_type': forms.Select(choices=Supplier_details.ACTIVITY_TYPE_CHOICES),
            'manufacturing_competency1': forms.Select(choices=Supplier_details.MANUFACTURING_COMPETENCY_CHOICES),
            'manufacturing_competency2': forms.Select(choices=Supplier_details.MANUFACTURING_COMPETENCY_CHOICES),
            'info_source': forms.Select(choices=Supplier_details.INFO_SOURCE_CHOICES),
            'amount_of_employees': forms.Select(choices=Supplier_details.EMPLOYEES_CHOICES),
            'turnover_per_year': forms.Select(choices=Supplier_details.TURNOVER_CHOICES),
            'certificates': forms.Select(choices=Supplier_details.CERTIFICATES_CHOICES),
        }

class SelectCustomer(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(customer__isnull=True)
        self.fields['user'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['Name'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['type_of_business'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['Address'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['EORI_number'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['VAT_number'].widget.attrs.update({'class': 'form-control', 'required': 'true'})
        self.fields['is_deleted'].widget.attrs.update({'class': 'form-check-input'})

    class Meta:
        model = Customer
        fields = ['Name','type_of_business','Address','phone','email','EORI_number','VAT_number','is_deleted', 'user']