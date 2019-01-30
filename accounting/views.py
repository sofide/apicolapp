from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count, Prefetch
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect

from accounting import forms
from accounting.manage_data import purchases_by_categories
from accounting.models import Product, Purchase, Category, Sale, DepreciationInfo


def dates_form_processor(request):
    """
    Use this function inside a view to process DateFromToForm data.
    Return from_date, to_date and an instance of DateFromToForm.

    THIS FUNCTION IS NOT A VIEW
    """
    # defaults from_date and to_date params
    to_date = datetime.now().date()
    one_year = timedelta(days=365)
    from_date = to_date - one_year

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
    purchases = Purchase.objects.filter(
        product__user=request.user,
        date__range=(from_date, to_date)
    ).aggregate(
        invested_money=Coalesce(Sum('value'), 0),
        total=Coalesce(Count('id'), 0),
        products=Coalesce(Count('product', distinct=True), 0)
    )

    sum_by_categories = Sum(
        'products__purchases__value',
        filter=Q(
            products__purchases__product__user=request.user,
            products__purchases__date__range=(from_date, to_date)
        )
    )
    purchases_detail = Category.objects.annotate(money=sum_by_categories)

    # INCOMES
    sales = Sale.objects.filter(
        user=request.user,
        date__range=(from_date, to_date)
    ).aggregate(
        total=Coalesce(Count('id'), 0),
        total_income=Coalesce(Sum('value'), 0),
        total_kg=Coalesce(Sum('amount'), 0)
    )


    result = sales['total_income'] - purchases['invested_money']
    profit = result > 0

    return render(request, 'accounting/accounting_index.html', {
        'from_date': from_date,
        'to_date': to_date,
        'dates_form': dates_form,
        'purchases': purchases,
        'purchases_detail': purchases_detail,
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
def purchase_detail(request, product_pk):
    """Second purchase step.
    Ask user for purchase information.
    If the product belongs to a category with depreciation, user must add the year of the model.
    """
    product = get_object_or_404(Product, pk=product_pk, user=request.user)
    if product.category.depreciation_period:
        ViewForm = forms.PurchaseDepreciationForm
    else:
        ViewForm = forms.PurchaseForm

    if request.method == 'POST':
        purchase_form = ViewForm(request.POST)

        if purchase_form.is_valid():
            new_purchase = purchase_form.save(commit=False)
            new_purchase.user = request.user
            new_purchase.product = product
            new_purchase.save()

            # save depreciation info if applicable
            if purchase_form.data.get('model_year'):
                DepreciationInfo.objects.create(
                    purchase=new_purchase,
                    model_year=purchase_form.data.get('model_year')
                )

            return redirect('accounting_index')

    else:
        purchase_form = ViewForm()

    return render(request, 'accounting/purchase_detail.html', {
        'purchase_form': purchase_form,
        'product': product,
    })


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
