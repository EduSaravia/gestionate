from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import CategoryForm, SignUpForm, SubscriptionForm, TransactionForm
from .models import Category, Subscription, Transaction


class SpanishLoginView(LoginView):
    authentication_form = AuthenticationForm
    template_name = "registration/login.html"


def _ensure_default_categories(user):
    defaults = [
        {"name": "Salario", "type": "INCOME", "color": "#22c55e"},
        {"name": "Extra", "type": "INCOME", "color": "#0ea5e9"},
        {"name": "Empleo", "type": "INCOME", "color": "#14b8a6"},
        {"name": "Freelance", "type": "INCOME", "color": "#06b6d4"},
        {"name": "Propinas", "type": "INCOME", "color": "#a855f7"},
        {"name": "Vivienda", "type": "EXPENSE", "color": "#f97316"},
        {"name": "Comida", "type": "EXPENSE", "color": "#f43f5e"},
        {"name": "Transporte", "type": "EXPENSE", "color": "#6366f1"},
    ]
    for item in defaults:
        Category.objects.get_or_create(user=user, name=item["name"], type=item["type"], defaults={"color": item["color"]})


@login_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    transactions = Transaction.objects.filter(user=request.user).select_related("category")
    subs = Subscription.objects.filter(user=request.user, is_active=True).select_related("category")

    income_total = transactions.filter(category__type="INCOME").aggregate(total=Sum("amount"))["total"] or Decimal("0")
    expense_total = transactions.filter(category__type="EXPENSE").aggregate(total=Sum("amount"))["total"] or Decimal("0")

    month_expenses_qs = transactions.filter(category__type="EXPENSE", date__gte=month_start)
    month_expense = month_expenses_qs.aggregate(total=Sum("amount"))["total"] or Decimal("0")

    totals_by_currency = {
        row["currency"]: row["total"] or Decimal("0")
        for row in month_expenses_qs.values("currency").annotate(total=Sum("amount"))
    }

    category_totals_raw = month_expenses_qs.values("category__name", "category__color", "currency").annotate(
        total=Sum("amount")
    ).order_by("-total")

    monthly_category_totals = []
    for entry in category_totals_raw:
        currency_total = totals_by_currency.get(entry["currency"]) or Decimal("0")
        percent = int((entry["total"] / currency_total) * 100) if currency_total else 0
        monthly_category_totals.append(
            {
                "name": entry["category__name"] or "Sin categoria",
                "color": entry["category__color"] or "#64748b",
                "currency": entry["currency"],
                "total": entry["total"],
                "percent": percent,
            }
        )
    flow_total = income_total + expense_total
    expense_ratio = int((expense_total / flow_total) * 100) if flow_total else 50
    income_ratio = 100 - expense_ratio

    upcoming_subs = subs.filter(next_billing_date__gte=today).order_by("next_billing_date")[:5]
    overdue_subs = subs.filter(next_billing_date__lt=today).order_by("next_billing_date")[:3]
    recent_transactions = transactions.order_by("-date", "-created_at")[:6]

    context = {
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": income_total - expense_total,
        "month_expense": month_expense,
        "expense_ratio": expense_ratio,
        "income_ratio": income_ratio,
        "monthly_category_totals": monthly_category_totals,
        "upcoming_subs": upcoming_subs,
        "overdue_subs": overdue_subs,
        "recent_transactions": recent_transactions,
    }
    return render(request, "finance/dashboard.html", context)


@login_required
def add_transaction(request):
    _ensure_default_categories(request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            messages.success(request, "Movimiento guardado.")
            return redirect("dashboard")
    else:
        form = TransactionForm(user=request.user)
    return render(request, "finance/transaction_form.html", {"form": form})


@login_required
def add_income(request):
    _ensure_default_categories(request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user, restrict_type="INCOME")
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            messages.success(request, "Ingreso guardado.")
            return redirect("dashboard")
    else:
        form = TransactionForm(user=request.user, restrict_type="INCOME")
    return render(request, "finance/transaction_form.html", {"form": form, "is_income": True})


@login_required
def add_subscription(request):
    _ensure_default_categories(request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            messages.success(request, "Suscripcion guardada.")
            return redirect("dashboard")
    else:
        form = SubscriptionForm(user=request.user)
    return render(request, "finance/subscription_form.html", {"form": form})


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "Categoria creada.")
            return redirect("dashboard")
    else:
        form = CategoryForm()
    return render(request, "finance/category_form.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            _ensure_default_categories(user)
            login(request, user)
            messages.success(request, "Cuenta creada. Bienvenido/a!")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
