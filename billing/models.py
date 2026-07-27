from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    date_created = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def tax_amount(self):
        return sum(item.tax_amount for item in self.items.all())

    @property
    def discount_amount(self):
        return (self.subtotal * self.discount_percent) / 100

    @property
    def grand_total(self):
        return self.subtotal + self.tax_amount - self.discount_amount


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.description} (x{self.quantity})"

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    @property
    def tax_amount(self):
        return (self.total_price * self.tax_percent) / 100