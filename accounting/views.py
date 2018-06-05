from django.shortcuts import render, get_object_or_404, redirect

from accounting.models import Product, Purchase
from accounting.forms import ProductForm, PurchaseForm


def accounting_index(request):
    purchases = Purchase.objects.all()

    return render(request, 'accounting/accounting_index.html', {
        'purchases': purchases,
    })



def product_index(request):
    pass


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
        product_instance = get_object_or_404(Product, pk=product_pk)
    else:
        product_instance = None

    if request.user.is_authenticated:
        if request.method == 'POST':
            product_form = ProductForm(request.POST, instance=product_instance)

            if product_form.is_valid():
                new_product = product_form.save(commit=False)
                new_product.owner = request.user
                new_product.save()

                return _next_page(new_product)

        else:
            product_form = ProductForm(instance=product_instance)

        return render(request, 'accounting/product_edit.html', {
            'product_form': product_form,
            'instance': product_instance,
        })


def purchase_product(request):
    products = Product.objects.all()

    if products.exists():
        return render(request, 'accounting/purchase_product.html', {
            'products': products,
        })
    else:
        # edit redirect response to use new product in a purchase
        response = redirect('product_edit')
        response['Location'] += '?next=purchase'
        return response


def purchase_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)

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
