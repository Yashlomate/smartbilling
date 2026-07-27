from django import forms
from .models import Invoice, InvoiceItem


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'invoice_number', 'status', 'due_date', 'discount_percent']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'invoice_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control'}),
        }


InvoiceItemFormSet = forms.inlineformset_factory(
    Invoice,
    InvoiceItem,
    fields=['description', 'quantity', 'unit_price', 'tax_percent'],
    extra=3,
    can_delete=True,
    widgets={
        'description': forms.TextInput(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
        'tax_percent': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }