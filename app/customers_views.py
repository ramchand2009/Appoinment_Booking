# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse, QueryDict
from django import template
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.contrib import messages

from app.forms import TransactionForm
from app.models import Transaction
from app.models import Customer
from app.forms import CustomerForm
from app.utils import set_pagination
from app.heyoo import WhatsApp
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


class CustomerView(View):
    context = {'segment': 'customers'}

    def get(self, request, pk=None, action=None):
        print("Get function")
        if request.is_ajax():
            if pk and action == 'edit':
                print("Sorry 1")
                edit_row = self.edit_row(pk)
                print("Edit row function done-----------------------") #-----------------------------
                print(edit_row)
                return JsonResponse({'edit_row': edit_row})
            elif pk and not action:
                print("sorry 2")
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            print("sorry 3")
            context, template = self.edit(request, pk)
        elif action == 'add':
            print("sorry 4")
            print("add request")
            context, template = self.add(request)
            

        else:
            print("sorry 5")
            context, template = self.list(request)

        if not context:
            print("sorry 6")
            print("sorry no content")
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))
            

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        print("adding new data Ramssss")
        print(request.POST)
        """ self.update_instance(request, pk)
        return redirect('transactions') """
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction saved successfully')
        return redirect('customers')


    def put(self, request, pk, action=None):
        print("This is step 1")
        print("put request body")
        print(request.body)
        print(pk)
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        print(edit_row)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        transaction = self.get_object(pk)
        print("trying to delete")
        print(transaction)
        transaction.delete()

        redirect_url = None
        if action == 'single':
            messages.success(request, 'Item deleted successfully')
            redirect_url = reverse('transactions')

        response = {'valid': 'success', 'message': 'Item deleted successfully', 'redirect_url': redirect_url}
        return JsonResponse(response)

    """ Get pages """

    def list(self, request):
        filter_params = None

        search = request.GET.get('search')
        if search:
            filter_params = None
            for key in search.split():
                if key.strip():
                    if not filter_params:
                        filter_params = Q(bill_for__icontains=key.strip())
                    else:
                        filter_params |= Q(bill_for__icontains=key.strip())

        transactions = Customer.objects.filter(filter_params) if filter_params else Customer.objects.all()
        data = Customer.objects.all()
        print("Ram this is output from database")
        print(data)
        self.context['transactions'], self.context['info'] = set_pagination(request, transactions)
        if not self.context['transactions']:
            return False, self.context['info']

        return self.context, 'app/customers/list.html'

    def edit(self, request, pk):
        print("Ram its editing")
        transaction = self.get_object(pk)
        self.context['customer'] = transaction
        self.context['form'] = CustomerForm(instance=transaction)
        return self.context, 'app/customers/edit.html'
    
    def add(self, request): 
        if request.method == "POST":
            form = CustomerForm(request.POST)
            if form.is_valid():
                form.save()
                
        else:
            self.context['form'] = CustomerForm()
            return self.context, 'app/customers/add.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        transaction = self.get_object(pk)
        print("Edit Row FUncation")
        form = CustomerForm(instance=transaction)
        context = {'instance': transaction, 'form': form}
        return render_to_string('app/customers/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        transaction = get_object_or_404(Customer, id=pk)
        return transaction

    def get_row_item(self, pk):
        transaction = self.get_object(pk)
        edit_row = render_to_string('app/customers/edit_row.html', {'instance': transaction})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        transaction = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = CustomerForm(form_data, instance=transaction)
        if form.is_valid():
            form.save()
            print("Sucess")
            if not is_urlencode:
                messages.success(request, 'Transaction saved successfully')

            return True, 'Transaction saved successfully'

        if not is_urlencode:
            messages.warning(request, 'Error Occurred. Please try again.')
            print("finaly faileer")
        return False, 'Error Occurred. Please try again.'
