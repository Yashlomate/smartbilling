from django.test import TestCase
from decimal import Decimal
from .models import Customer, Invoice, InvoiceItem


class InvoiceCalculationTests(TestCase):

    def setUp(self):
        """Runs before every test — sets up common test data."""
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        self.invoice = Invoice.objects.create(
            customer=self.customer,
            invoice_number="TEST-001",
            due_date="2026-08-01",
            discount_percent=Decimal('10.00')
        )

    def test_subtotal_calculation(self):
        """Subtotal should equal sum of (quantity * unit_price) across items."""
        InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Item A",
            quantity=2,
            unit_price=Decimal('500.00'),
            tax_percent=Decimal('0')
        )
        InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Item B",
            quantity=1,
            unit_price=Decimal('300.00'),
            tax_percent=Decimal('0')
        )
        self.assertEqual(self.invoice.subtotal, Decimal('1300.00'))

    def test_tax_amount_calculation(self):
        """Tax amount should be correctly calculated per item and summed."""
        InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Taxed Item",
            quantity=1,
            unit_price=Decimal('1000.00'),
            tax_percent=Decimal('18.00')
        )
        self.assertEqual(self.invoice.tax_amount, Decimal('180.00'))

    def test_grand_total_with_discount(self):
        """Grand total should be subtotal + tax - discount."""
        InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Item",
            quantity=1,
            unit_price=Decimal('1000.00'),
            tax_percent=Decimal('18.00')
        )
        # subtotal = 1000, tax = 180, discount = 10% of 1000 = 100
        # grand_total = 1000 + 180 - 100 = 1080
        self.assertEqual(self.invoice.grand_total, Decimal('1080.00'))

    def test_empty_invoice_has_zero_subtotal(self):
        """An invoice with no items should have subtotal of zero, not crash."""
        self.assertEqual(self.invoice.subtotal, 0)
