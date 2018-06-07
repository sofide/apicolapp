from django.db.models import Sum

from accounting.models import Purchase, Inventary, InventaryProduct


def theorical_stock(initial_inventary, final_date):
    '''stock from initial_inventary plus purchases'''
    initial_date = initial_inventary.date

    initial_inventary_products = InventaryProduct.objects.select_related('product').filter(
        inventary=initial_inventary
    )

    purchases = Purchase.objects.select_related('product').filter(
        date__range=(initial_date, final_date)
    )

    # [product, initial_stock, purchases_sum, theorical_stock]
    products = []
    for product_in_inventary in initial_inventary_products:
        product = product_in_inventary.product
        initial_stock = product_in_inventary.amount
        # purchases =
        # theorical_stock =
        # INCOMPLETE


