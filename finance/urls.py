from django.urls import path

from .views import SpanishLoginView, add_category, add_income, add_subscription, add_transaction, dashboard, register

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", SpanishLoginView.as_view(), name="login"),
    path("registro/", register, name="register"),
    path("transaccion/nueva/", add_transaction, name="add_transaction"),
    path("ingreso/nuevo/", add_income, name="add_income"),
    path("suscripcion/nueva/", add_subscription, name="add_subscription"),
    path("categoria/nueva/", add_category, name="add_category"),
]
