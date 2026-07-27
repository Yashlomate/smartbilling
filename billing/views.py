from rest_framework import viewsets
from .models import Customer, Invoice, InvoiceItem
from .serializers import CustomerSerializer, InvoiceSerializer, InvoiceItemSerializer
from django.db import transaction


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice, Customer, InvoiceItem


def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-date_created')
    return render(request, 'billing/invoice_list.html', {'invoices': invoices})


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'billing/invoice_detail.html', {'invoice': invoice}) 
from .forms import InvoiceForm, InvoiceItemFormSet


def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                invoice = form.save(commit=False)
                formset = InvoiceItemFormSet(request.POST, instance=invoice)
                invoice.save()
                if formset.is_valid():
                    formset.save()
                    return redirect('invoice_detail', pk=invoice.pk)
                else:
                    invoice.delete()  # rollback if items are invalid
            except Exception as e:
                print(f"Error creating invoice: {e}")
        formset = InvoiceItemFormSet(request.POST)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, 'billing/invoice_form.html', {'form': form, 'formset': formset})
from .forms import CustomerForm

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_create')
    else:
        form = CustomerForm()
    return render(request, 'billing/customer_form.html', {'form': form}) 
from django.http import JsonResponse
from .ai_utils import generate_item_description

def ai_enhance_description(request):
    if request.method == 'POST':
        rough_text = request.POST.get('text', '')
        enhanced = generate_item_description(rough_text)
        return JsonResponse({'description': enhanced})
    return JsonResponse({'error': 'Invalid request'}, status=400)

from django.db import transaction

def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    invoice = form.save(commit=False)
                    invoice.save()
                    formset = InvoiceItemFormSet(request.POST, instance=invoice)
                    if not formset.is_valid():
                        raise ValueError("Invalid invoice items")
                    formset.save()
                return redirect('invoice_detail', pk=invoice.pk)
            except Exception as e:
                print(f"Error creating invoice: {e}")
        formset = InvoiceItemFormSet(request.POST)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()
    return render(request, 'billing/invoice_form.html', {'form': form, 'formset': formset})
def mark_as_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.status = 'paid'
    invoice.save()
    return redirect('invoice_detail', pk=invoice.pk)
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            try:
                with transaction.atomic():
                    invoice = form.save()
                    formset = InvoiceItemFormSet(request.POST, instance=invoice)
                    if not formset.is_valid():
                        raise ValueError("Invalid invoice items")
                    formset.save()
                return redirect('invoice_detail', pk=invoice.pk)
            except Exception as e:
                print(f"Error updating invoice: {e}")
        formset = InvoiceItemFormSet(request.POST, instance=invoice)
    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceItemFormSet(instance=invoice)

    return render(request, 'billing/invoice_form.html', {'form': form, 'formset': formset, 'editing': True})
