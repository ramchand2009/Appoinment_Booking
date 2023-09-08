from django import forms

from app.models import Transaction
from app.models import Customer
from app.models import employee

class ChangeInputsStyle(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            # get current classes from Meta
            input_type = self.fields[field].widget.input_type
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += " form-check-input" if input_type == "checkbox" else " form-control  flatpickr-input"
            else:
                classes = " form-check-input" if input_type == "checkbox" else " form-control flatpickr-input"
            self.fields[field].widget.attrs.update({
                'class': classes
            })

class TransactionForm(forms.ModelForm):
    bill_for = forms.CharField(label="Bill For", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    issue_date = forms.DateField(label="Issue Date", widget=forms.DateInput(
        attrs={'class': 'form-control datepicker_input transaction', 'placeholder': 'yyyy-mm-dd'}))

    due_date = forms.DateField(label="Due Date", widget=forms.DateInput(
        attrs={'class': 'form-control datepicker_input transaction', 'placeholder': 'yyyy-mm-dd'}))

    total = forms.DecimalField(label="Total", max_digits=10, decimal_places=2,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control transaction', 'placeholder': '...'}))

    status = forms.CharField(label="Status", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    class Meta:
        model = Transaction
        fields = ['bill_for', 'issue_date', 'due_date', 'total', 'status']


class CustomerForm(forms.ModelForm):
    Customer_name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    Customer_email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    Customer_mobile = forms.CharField(label="Mobile",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control transaction'}))
    
    Customer_Address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    Customer_Status = forms.BooleanField(label="Status",widget=forms.CheckboxInput(attrs={'class': 'form-check-input transaction'}),required=False)
    
    class Meta:
        model = Customer
        fields = ['Customer_name','Customer_email','Customer_mobile','Customer_Address','Customer_Status']


class employeeForm(forms.ModelForm):
    employee_name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    employee_email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    employee_mobile = forms.CharField(label="Mobile",max_length=10, widget=forms.TextInput(attrs={'class': 'form-control transaction'}))
    
    employee_Address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'class': 'form-control transaction'}))

    employee_Status = forms.BooleanField(label="Status",widget=forms.CheckboxInput(attrs={'class': 'form-check-input transaction'}),required=False)
    
    class Meta:
        model = employee
        fields = ['employee_name','employee_email','employee_mobile','employee_Address','employee_Status']
    
    