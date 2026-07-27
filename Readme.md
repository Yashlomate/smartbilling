# 🧾 Smart Billing Application

A full-stack invoice and billing management system built with Django. Handles customers, invoices, and dynamic line items with automatic tax/discount calculations, a REST API, and an AI-assisted description helper — built as a technical evaluation project focused on clean architecture and sound engineering practices over feature count.

---

## ✨ Features

- **Customer Management** — add and view customers directly from the app (no admin panel required)
- **Dynamic Invoice Creation** — add multiple line items in a single form using Django formsets, no page reloads
- **Automatic Calculations** — subtotal, tax, discount, and grand total are computed live from line items, never stale
- **Invoice Status Tracking** — Draft → Sent → Paid → Overdue, with color-coded badges
- **REST API** — full CRUD for customers, invoices, and items via Django REST Framework
- **AI-Assisted Descriptions** — a "✨ Enhance" button expands rough item text into professional invoice language
- **Admin Dashboard** — Django admin with inline item editing for backend management
- **Responsive UI** — Bootstrap 5, works cleanly on mobile and desktop
- **Tested Business Logic** — unit tests cover all calculation paths, including edge cases

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2 |
| API | Django REST Framework |
| Frontend | Django Templates + Bootstrap 5 |
| Database | SQLite |
| AI Layer | Rule-based smart suggestion engine (LLM-ready architecture) |

---

## 🏗️ Architecture & Key Decisions

**Computed properties over stored totals**
`subtotal`, `tax_amount`, `discount_amount`, and `grand_total` are Python `@property` methods on the `Invoice` model rather than stored database columns. This guarantees the total is always correct even if a line item is edited later — there's no "stale total" bug to worry about.

**Formsets over custom JavaScript**
Invoice line items use Django's `inlineformset_factory` to manage a variable number of items in one submission. This avoids hand-rolled JS for adding/removing rows and leans on a well-tested Django feature instead.

**Atomic transactions on create**
Invoice creation wraps the invoice + its items in a single `transaction.atomic()` block, so a failure partway through (e.g. invalid item data) rolls back cleanly instead of leaving an orphaned invoice with zero items.

**AI integration with a reliability fallback**
The description-enhancement feature was originally built against an external LLM API. Since production features shouldn't hard-depend on a third-party service's uptime or quota, it now runs on a rule-based keyword-matching engine by default, with the LLM integration path still in place in `ai_utils.py` for future use. Every AI call is wrapped in a `try/except` that falls back to the original input if anything fails.

**Money as Decimal, never Float**
All currency fields use `DecimalField`, never `FloatField` — floating-point rounding errors are unacceptable in billing calculations.

---

## 🚀 Setup Instructions

**1. Clone the repository**
```bash
git clone https://github.com/Yashlomate/smartbilling.git
cd smartbilling
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
Create a `.env` file in the project root (see `.env.example`):
**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create a superuser** (for admin access)
```bash
python manage.py createsuperuser
```

**7. Run the development server**
```bash
python manage.py runserver
```

**8. Open the app**
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- API root: http://127.0.0.1:8000/api/

---

## ✅ Running Tests

```bash
python manage.py test billing
```

Covers subtotal, tax, discount, grand total, and empty-invoice edge cases.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/customers/` | List / create customers |
| GET/PUT/DELETE | `/api/customers/<id>/` | Retrieve / update / delete a customer |
| GET/POST | `/api/invoices/` | List / create invoices |
| GET/PUT/DELETE | `/api/invoices/<id>/` | Retrieve / update / delete an invoice |
| GET/POST | `/api/items/` | List / create invoice items |

---

## 📁 Project Structure
smartbilling/
├── billing/
│ ├── models.py # Customer, Invoice, InvoiceItem
│ ├── views.py # Frontend + API views
│ ├── forms.py # InvoiceForm, CustomerForm, InvoiceItemFormSet
│ ├── serializers.py # DRF serializers
│ ├── ai_utils.py # AI-assisted description suggestions
│ ├── urls.py # Frontend URL routes
│ ├── api_urls.py # REST API routes
│ ├── admin.py # Admin panel configuration
│ └── tests.py # Unit tests for calculation logic
├── templates/
│ ├── base.html
│ └── billing/
│ ├── invoice_list.html
│ ├── invoice_detail.html
│ ├── invoice_form.html
│ └── customer_form.html
├── smartbilling/
│ ├── settings.py
│ └── urls.py
├── requirements.txt
└── manage.py
---

## 🔮 Future Improvements

- Payment gateway integration (Razorpay) for real online payments
- Email invoices directly to customers
- Scheduled task to auto-mark invoices as "Overdue" past due date
- PDF export/download for invoices
- User authentication and per-user invoice scoping
- Full LLM integration re-enabled once API reliability is confirmed

---

## 👤 Author

Built by **Yash Lomate** as part of a technical evaluation assignment.