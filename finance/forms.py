from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Subscription, Transaction


class BaseStyledForm(forms.ModelForm):
    """Añade clases y placeholders rápidos a los inputs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "input"})


class TransactionForm(BaseStyledForm):
    class Meta:
        model = Transaction
        fields = ["amount", "currency", "payment_method", "date", "category", "description", "is_recurring"]
        labels = {
            "amount": "Monto",
            "currency": "Moneda",
            "payment_method": "Medio de pago",
            "date": "Fecha",
            "category": "Categoría",
            "description": "Descripción",
            "is_recurring": "¿Recurrente?",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.TextInput(attrs={"placeholder": "Descripción breve"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["currency"].initial = "PEN"
        self.fields["payment_method"].initial = "YAPE"
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)


class SubscriptionForm(BaseStyledForm):
    class Meta:
        model = Subscription
        fields = ["name", "amount", "billing_cycle", "next_billing_date", "category", "auto_renew", "notes"]
        labels = {
            "name": "Nombre",
            "amount": "Monto",
            "billing_cycle": "Frecuencia",
            "next_billing_date": "Próximo cobro",
            "category": "Categoría",
            "auto_renew": "Renovación automática",
            "notes": "Notas",
        }
        widgets = {
            "next_billing_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.TextInput(attrs={"placeholder": "Notas o recordatorio"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["category"].queryset = Category.objects.filter(user=user)


class CategoryForm(BaseStyledForm):
    class Meta:
        model = Category
        fields = ["name", "type", "color"]
        labels = {
            "name": "Nombre",
            "type": "Tipo",
            "color": "Color",
        }
        widgets = {
            "color": forms.TextInput(attrs={"type": "color"}),
            "name": forms.TextInput(attrs={"placeholder": "Ej. Alquiler, Comida"}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "input"})
        self.fields["username"].label = "Usuario"
        self.fields["email"].label = "Correo"
        self.fields["first_name"].label = "Nombre"
        self.fields["last_name"].label = "Apellidos"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"
