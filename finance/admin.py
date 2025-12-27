from django.contrib import admin

from .models import Category, Subscription, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user", "color", "created_at")
    list_filter = ("type", "user")
    search_fields = ("name", "user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "currency", "payment_method", "category", "user", "date", "is_recurring")
    list_filter = ("is_recurring", "date", "currency", "payment_method")
    search_fields = ("description", "category__name", "user__username")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "billing_cycle", "next_billing_date", "is_active", "user")
    list_filter = ("billing_cycle", "is_active")
    search_fields = ("name", "user__username")
