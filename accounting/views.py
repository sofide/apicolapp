from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Count, Prefetch
from django.shortcuts import render, get_object_or_404, redirect

from accounting.manage_data import purchases_by_categories
from accounting.models import Product, Purchase, Category, Sale
from accounting.forms import ProductForm, PurchaseForm, SaleForm


@login_required
def accounting_index(request):
    '''
    Show user's incomes and investments.
    '''
    # INVESTMENTS
    purchases = Purchase.objects.filter(product__user=request.user).aggregate(
        invested_money=Sum('value'),
        total = Count('id'),
        products=Count('product', distinct=True)
    )

    sum_by_categories = Sum(
        'products__purchases__value',
        filter=Q(products__purchases__product__user=request.user)
    )
    purchases_detail = Category.objects.annotate(money=sum_by_categories)

    # INCOMES
    sales = Sale.objects.filter(user=request.user).aggregate(
        total=Count('id'),
        total_income=Sum('value'),
        total_kg=Sum('amount'),
    )


    result = sales['total_income'] - purchases['invested_money']
    profit = result > 0

    return render(request, 'accounting/accounting_index.html', {
        'purchases': purchases,
        'purchases_detail': purchases_detail,
        'sales': sales,
        'result': result,
        'profit': profit,
    })


@login_required
def purchase_list(request):
    purchases = purchases_by_categories(request.user.pk)

    return render(request, 'accounting/purchases_list.html', {
        'purchases': purchases,
    })


def product_index(request):
    pass


@login_required
def product_edit(request, product_pk=None):
    '''create or edit a product'''
    def _next_page(product_object):
        '''define next page if form is valid'''
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
            product_form = ProductForm(request.POST, instance=product_instance)

            if product_form.is_valid():
                new_product = product_form.save(commit=False)
                new_product.user = request.user
                new_product.save()

                return _next_page(new_product)

        else:
            product_form = ProductForm(instance=product_instance)

        return render(request, 'accounting/product_edit.html', {
            'product_form': product_form,
            'instance': product_instance,
        })


@login_required
def purchase_product(request):
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
    product = get_object_or_404(Product, pk=product_pk, user=request.user)

    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)

        if purchase_form.is_valid():
            new_purchase = purchase_form.save(commit=False)
            new_purchase.user = request.user
            new_purchase.product = product
            new_purchase.save()

            return redirect('accounting_index')

    else:
        purchase_form = PurchaseForm()

    return render(request, 'accounting/purchase_detail.html', {
        'purchase_form': purchase_form,
        'product': product,
    })


@login_required
def sales_list(request):
    """
    Show user's sales list.
    """
    sales = request.user.sales.all()

    return render(request, 'accounting/sales_list.html', {
        'sales': sales,
    })


@login_required
def sale_new(request):
    """
    Save a new sale on the database.
    """
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)

        if sale_form.is_valid():
            new_sale = sale_form.save(commit=False)
            new_sale.user = request.user
            new_sale.save()

            return redirect('sales_list')

    else:
        sale_form = SaleForm()

    return render(request, 'accounting/sale_new.html', {
        'sale_form': sale_form,
    })
