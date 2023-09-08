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
from app.forms import CustomerForm
from app.models import Customer
from app.forms import employeeForm
from app.models import employee
from app.utils import set_pagination
from app.heyoo import WhatsApp
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.customers_views import CustomerView
from app.employee_views import employeeView

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        print("Data received from Webhook is: ", request.body)
        return HttpResponse("Webhook received!")
    if request.method == 'GET':
         mode = request.GET.get('hub.mode')
         token = request.GET.get('hub.verify_token')
         challenge = request.GET.get('hub.challenge')
         print("Mode data: ", mode)
         print("Token data: ", token)
         print("Challenge data: ", challenge)
    if mode == 'subscribe' and token == '12345': 
        print("WEBHOOK_VERIFIED")
        return HttpResponse(challenge)
    


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('index.html')
    messenger = WhatsApp('EAAO4IhAooskBO9i05maqLh4t71Q9lNVNqSiURK9iDIfB6hLfkIRt5B3pcM1Td08JSgA7VnyZBPDoTR3WciWWuC4wXQGdiuZBYrewyrR2MWHQVuL9e5DXrCBnevJEBlP6zReTnyIvR8q5BUBTuMOLw4Mm2Vm2z3XcF18wdZCX6yvvFd7ANBCZC8BcfP2mxBMnLxez7meYTRgQO1RVHsg6',  phone_number_id='101528516342241')
    messenger.send_message('Welcome to Ramc website ', '+91 7200956757')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


class TransactionView(View):
    context = {'segment': 'transactions'}

    def get(self, request, pk=None, action=None):
        if request.is_ajax():
            if pk and action == 'edit':
                edit_row = self.edit_row(pk)
                return JsonResponse({'edit_row': edit_row})
            elif pk and not action:
                edit_row = self.get_row_item(pk)
                return JsonResponse({'edit_row': edit_row})

        if pk and action == 'edit':
            print("Sorry 3")
            context, template = self.edit(request, pk)
        elif action == 'add':
            print("Sorry 4")
            print("add request")
            context, template = self.add(request)
            

        else:
            print("Sorry 5")
            context, template = self.list(request)

        if not context:
            print("Sorry 6")
            html_template = loader.get_template('page-500.html')
            return HttpResponse(html_template.render(self.context, request))

        return render(request, template, context)

    def post(self, request, pk=None, action=None):
        print("adding new data Ramssss")
        print(request.POST)
        """ self.update_instance(request, pk)
        return redirect('transactions') """
    
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction saved successfully')
        return redirect('transactions')


    def put(self, request, pk, action=None):
        print("This is step 1")
        print("put request body")
        print(request.body)
        print(pk)
        is_done, message = self.update_instance(request, pk, True)
        edit_row = self.get_row_item(pk)
        print("Final output")
        print(edit_row)
        return JsonResponse({'valid': 'success' if is_done else 'warning', 'message': message, 'edit_row': edit_row})

    def delete(self, request, pk, action=None):
        transaction = self.get_object(pk)
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

        transactions = Transaction.objects.filter(filter_params) if filter_params else Transaction.objects.all()
        print("This is output data")
        print(transactions)
        self.context['transactions'], self.context['info'] = set_pagination(request, transactions)
        if not self.context['transactions']:
            return False, self.context['info']

        return self.context, 'app/transactions/list.html'

    def edit(self, request, pk):
        print("Ram its editing")
        transaction = self.get_object(pk)
        self.context['transaction'] = transaction
        self.context['form'] = TransactionForm(instance=transaction)

        return self.context, 'app/transactions/edit.html'
    
    def add(self, request): 
        if request.method == "POST":
            form = TransactionForm(request.POST)
            if form.is_valid():
                form.save()
                
        else:
            self.context['form'] = TransactionForm()
            return self.context, 'app/transactions/add.html'

    """ Get Ajax pages """

    def edit_row(self, pk):
        transaction = self.get_object(pk)
        print(transaction)
        form = TransactionForm(instance=transaction)
        context = {'instance': transaction, 'form': form}
        return render_to_string('app/transactions/edit_row.html', context)

    """ Common methods """

    def get_object(self, pk):
        transaction = get_object_or_404(Transaction, id=pk)
        return transaction

    def get_row_item(self, pk):
        transaction = self.get_object(pk)
        edit_row = render_to_string('app/transactions/edit_row.html', {'instance': transaction})
        return edit_row

    def update_instance(self, request, pk, is_urlencode=False):
        transaction = self.get_object(pk)
        form_data = QueryDict(request.body) if is_urlencode else request.POST
        form = TransactionForm(form_data, instance=transaction)
        if form.is_valid():
            form.save()
            print("i am sucess")
            if not is_urlencode:
                messages.success(request, 'Transaction saved successfully')

            return True, 'Transaction saved successfully'

        if not is_urlencode:
            messages.warning(request, 'Error Occurred. Please try again.')
        return False, 'Error Occurred. Please try again.'


