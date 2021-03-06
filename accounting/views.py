from datetime import datetime, timedelta, date

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count, Prefetch
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect

from accounting import forms
from accounting.manage_data import purchases_by_categories
from accounting.models import Product, Purchase, Category, Sale


def dates_form_processor(request):
    """
    Use this function inside a view to process DateFromToForm data.
    Return from_date, to_date and an instance of DateFromToForm.

    THIS FUNCTION IS NOT A VIEW
    """
    # defaults from_date and to_date params
    # default period starts the last August 8 and ends today.
    to_date = datetime.now().date()
    if to_date.month >= 8:
        from_year = to_date.year
    else:
        from_year = to_date.year - 1

    from_date = date(from_year, 8, 1)

    if request.GET.get('from_date'):
        dates_form = forms.DateFromToForm(request.GET)
        if dates_form.is_valid():
            to_date = dates_form.cleaned_data['to_date']
            from_date = dates_form.cleaned_data['from_date']
    else:
        dates_form = forms.DateFromToForm()

    return from_date, to_date, dates_form


@login_required
def accounting_index(request):
    """
    Show user's incomes and investments from last year, or between from_date
    and to_date recived in POST params.
    """
    from_date, to_date, dates_form = dates_form_processor(request)

    # INVESTMENTS
    purchases = purchases_by_categories(request.user.pk, from_date, to_date)

    invested_money = 0

    direct_expenses_data = {}

    depreciation_purchases_data = {}

    for categ_purchase in purchases.values():
        invested_money += categ_purchase['amount']

        if categ_purchase['depreciation_period']:
            data_dict = depreciation_purchases_data
        else:
            data_dict = direct_expenses_data

        data_dict['invested_money'] = round(data_dict.get('invested_money', 0)
                                            + categ_purchase['amount'], 2)
        data_dict['products_count'] = round(data_dict.get('products_count', 0)
                                            + categ_purchase['products'])
        data_dict['purchases_count'] = round(data_dict.get('purchases_count', 0)
                                             + categ_purchase['total'])

    # INCOMES
    sales = Sale.objects.filter(
        user=request.user,
        date__range=(from_date, to_date)
    ).aggregate(
        total=Coalesce(Count('id'), 0),
        total_income=Coalesce(Sum('value'), 0),
        total_kg=Coalesce(Sum('amount'), 0)
    )


    result = round(sales['total_income'] - invested_money, 2)
    profit = result > 0

    return render(request, 'accounting/accounting_index.html', {
        'from_date': from_date,
        'to_date': to_date,
        'dates_form': dates_form,
        'invested_money': invested_money,
        'direct_expenses_data': direct_expenses_data,
        'depreciation_purchases_data': depreciation_purchases_data,
        'sales': sales,
        'result': result,
        'profit': profit,
        'datepicker_fields_ids': ['id_from_date', 'id_to_date'],
    })


@login_required
def purchase_list(request):
    from_date, to_date, dates_form = dates_form_processor(request)
    purchases = purchases_by_categories(request.user.pk, from_date, to_date)

    return render(request, 'accounting/purchases_list.html', {
        'purchases': purchases,
        'from_date': from_date,
        'to_date': to_date,
        'dates_form': dates_form,
        'datepicker_fields_ids': ['id_from_date', 'id_to_date'],
    })


def product_index(request):
    pass


@login_required
def product_edit(request, product_pk=None):
    """Create or edit a product."""
    def _next_page(product_object):
        """Define next page if form is valid."""
        next = request.GET.get('next', None)
        if next == 'purchase':
            return redirect('purchase_detail', product_pk=product_object.pk)
        else:
            return redirect('product_index')

    if product_pk:
        product_instance = get_object_or_404(Product, pk=product_pk, user=request.user)
    else:
        product_instance = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            product_form = forms.ProductForm(request.POST, instance=product_instance)

            if product_form.is_valid():
                new_product = product_form.save(commit=False)
                new_product.user = request.user
                new_product.save()

                return _next_page(new_product)

        else:
            product_form = forms.ProductForm(instance=product_instance)

        return render(request, 'accounting/product_edit.html', {
            'product_form': product_form,
            'instance': product_instance,
        })


@login_required
def purchase_product(request):
    """First purchase step.
    Select the product from historical purchases or load a new product.
    """
    products = Product.objects.filter(user=request.user)
    categories = Category.objects.prefetch_related(Prefetch('products', queryset=products))

    if products.exists():
        response = render(request, 'accounting/purchase_product.html', {
            'categories': categories,
        })
    else:
        # edit redirect response to use new product in a purchase
        response = redirect('product_new')
        response['Location'] += '?next=purchase'

    return response


@login_required
def purchase_detail(request, product_pk, purchase_pk=None):
    """Second purchase step.
    Ask user for purchase information.
    """
    product = get_object_or_404(Product, pk=product_pk, user=request.user)

    purchase_instance = None
    if purchase_pk:
        purchase_instance = get_object_or_404(Purchase, pk=purchase_pk, product=product)

    if request.method == 'POST':
        purchase_form = forms.PurchaseForm(request.POST, instance=purchase_instance)

        if purchase_form.is_valid():
            new_purchase = purchase_form.save(commit=False)
            new_purchase.user = request.user
            new_purchase.product = product
            new_purchase.save()

            return redirect('purchase_list')

    else:
        purchase_form = forms.PurchaseForm(instance=purchase_instance)

    return render(request, 'accounting/purchase_detail.html', {
        'purchase_form': purchase_form,
        'product': product,
        'purchase_instance': purchase_instance,
    })


@login_required
def purchase_delete(request, purchase_pk):
    purchase = get_object_or_404(Purchase, pk=purchase_pk)
    purchase.delete()
    return redirect('purchase_list')


@login_required
def sales_list(request):
    """Show user's sales list."""
    from_date, to_date, dates_form = dates_form_processor(request)
    sales = request.user.sales.filter(date__range=(from_date, to_date))

    return render(request, 'accounting/sales_list.html', {
        'sales': sales,
        'from_date': from_date,
        'to_date': to_date,
        'dates_form': dates_form,
        'datepicker_fields_ids': ['id_from_date', 'id_to_date'],
    })


@login_required
def sale_new(request, sale_pk=None):
    """Save a new sale on the database."""
    if sale_pk:
        sale_instance = get_object_or_404(Sale, pk=sale_pk)
    else:
        sale_instance = None

    if request.method == 'POST':
        sale_form = forms.SaleForm(request.POST, instance=sale_instance)

        if sale_form.is_valid():
            new_sale = sale_form.save(commit=False)
            new_sale.user = request.user
            new_sale.save()

            return redirect('sales_list')

    else:
        sale_form = forms.SaleForm(instance=sale_instance)

    return render(request, 'accounting/sale_new.html', {
        'sale_form': sale_form,
        'sale_instance': sale_instance,
    })


@login_required
def sale_delete(request, sale_pk):
    sale = get_object_or_404(Sale, pk=sale_pk)
    sale.delete()
    return redirect('sales_list')
