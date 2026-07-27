from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, InvoiceViewSet, InvoiceItemViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'items', InvoiceItemViewSet)

urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, InvoiceViewSet, InvoiceItemViewSet, invoice_list, invoice_detail

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'items', InvoiceItemViewSet)

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
] + router.urls

from django.urls import path
from .views import invoice_list, invoice_detail

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
]
from .views import invoice_list, invoice_detail, invoice_create

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('invoice/new/', invoice_create, name='invoice_create'),
]
from .views import invoice_list, invoice_detail, invoice_create, customer_create

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('invoice/new/', invoice_create, name='invoice_create'),
    path('customer/new/', customer_create, name='customer_create'),
]
from .views import invoice_list, invoice_detail, invoice_create, customer_create, ai_enhance_description

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('invoice/new/', invoice_create, name='invoice_create'),
    path('customer/new/', customer_create, name='customer_create'),
    path('ai/enhance/', ai_enhance_description, name='ai_enhance_description'),
]
from .views import invoice_list, invoice_detail, invoice_create, customer_create, ai_enhance_description, mark_as_paid

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('invoice/new/', invoice_create, name='invoice_create'),
    path('customer/new/', customer_create, name='customer_create'),
    path('ai/enhance/', ai_enhance_description, name='ai_enhance_description'),
    path('invoice/<int:pk>/mark-paid/', mark_as_paid, name='mark_as_paid'),
]
from .views import invoice_list, invoice_detail, invoice_create, invoice_edit, customer_create, ai_enhance_description, mark_as_paid

urlpatterns = [
    path('', invoice_list, name='invoice_list'),
    path('invoice/<int:pk>/', invoice_detail, name='invoice_detail'),
    path('invoice/new/', invoice_create, name='invoice_create'),
    path('invoice/<int:pk>/edit/', invoice_edit, name='invoice_edit'),
    path('customer/new/', customer_create, name='customer_create'),
    path('ai/enhance/', ai_enhance_description, name='ai_enhance_description'),
    path('invoice/<int:pk>/mark-paid/', mark_as_paid, name='mark_as_paid'),
]