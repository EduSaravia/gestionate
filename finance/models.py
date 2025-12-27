from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    TYPE_CHOICES = (
        ("INCOME", "Ingreso"),
        ("EXPENSE", "Gasto"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default="EXPENSE")
    color = models.CharField(max_length=7, default="#10b981")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "name", "type")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Transaction(models.Model):
    CURRENCY_CHOICES = (
        ("PEN", "Soles (PEN)"),
        ("USD", "Dólares (USD)"),
    )
    PAYMENT_METHOD_CHOICES = (
        ("YAPE", "Yape"),
        ("PLIN", "Plin"),
        ("EFECTIVO", "Efectivo"),
        ("TARJETA", "Tarjeta"),
        ("TRANSFERENCIA", "Transferencia"),
        ("OTRO", "Otro"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    description = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="PEN")
    payment_method = models.CharField(max_length=14, choices=PAYMENT_METHOD_CHOICES, default="YAPE")
    date = models.DateField(default=timezone.now)
    is_recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.amount} - {self.description or 'Movimiento'}"

    @property
    def type(self):
        if self.category:
            return self.category.type
        return "EXPENSE"


class Subscription(models.Model):
    PERIOD_CHOICES = (
        ("WEEKLY", "Semanal"),
        ("MONTHLY", "Mensual"),
        ("YEARLY", "Anual"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    billing_cycle = models.CharField(max_length=10, choices=PERIOD_CHOICES, default="MONTHLY")
    next_billing_date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="subscriptions")
    notes = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["next_billing_date"]
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"

    def __str__(self):
        return f"{self.name} ({self.amount})"

    @property
    def is_overdue(self):
        return self.is_active and self.next_billing_date < timezone.now().date()
