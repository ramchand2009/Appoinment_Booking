# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin

from app.models import Transaction
from app.models import Customer
from import_export import resources
from import_export.admin import ImportMixin


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        fields = ['id', 'bill_for', 'issue_date', 'due_date', 'total', 'status', 'created_time']


@admin.register(Transaction)
class TransactionAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['id', 'bill_for', 'issue_date', 'due_date', 'total', 'status', 'created_time']
    resource_class = TransactionResource

  
class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        fields = ['id', 'Customer_name', 'Customer_email', 'Customer_mobile', 'Customer_Address',  'created_at','updated_at']


@admin.register(Customer)
class CustomerAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['id', 'Customer_name', 'Customer_email', 'Customer_mobile', 'Customer_Address',  'created_at','updated_at']
    resource_class = CustomerResource