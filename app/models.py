# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Customer(models.Model):
    Customer_name = models.CharField(max_length=250)
    Customer_email = models.EmailField()
    Customer_Status = models.BooleanField(default=False)
    Customer_mobile = models.CharField(blank=True, null=True, max_length=10)
    Customer_Address = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        verbose_name = 'customer'
        verbose_name_plural = 'customerss'

class employee(models.Model):
    employee_name = models.CharField(max_length=250)
    employee_mobile = models.CharField(blank=True, null=True, max_length=10)
    employee_email = models.EmailField()
    employee_Address = models.CharField(max_length=250)
    employee_Status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employee'

class Transaction(models.Model):
    bill_for = models.CharField(max_length=100)
    issue_date = models.DateField()
    due_date = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'

    @property
    def status_info(self):
        res = {'class': None}

        if self.status == "Paid":
            res['class'] = 'text-success'
        elif self.status == "Due":
            res['class'] = 'text-warning'
        elif self.status == "Canceled":
            res['class'] = 'text-danger'

        return res
