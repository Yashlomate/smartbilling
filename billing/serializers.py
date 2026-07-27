from rest_framework import serializers
from .models import Customer, Invoice, InvoiceItem


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    tax_amount = serializers.ReadOnlyField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'invoice', 'description', 'quantity', 'unit_price', 'tax_percent', 'total_price', 'tax_amount']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    subtotal = serializers.ReadOnlyField()
    tax_amount = serializers.ReadOnlyField()
    discount_amount = serializers.ReadOnlyField()
    grand_total = serializers.ReadOnlyField()

    class Meta:
        model = Invoice
        fields = [
            'id', 'customer', 'customer_name', 'invoice_number', 'status',
            'date_created', 'due_date', 'discount_percent',
            'items', 'subtotal', 'tax_amount', 'discount_amount', 'grand_total'
        ]