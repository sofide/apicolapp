"""
Manipulate accounting data to be used in views.
"""
from collections import defaultdict

from accounting.models import Category, Product, Purchase


def purchases_by_categories(user_id):
    """
    Group purchases by categories. Returns a dict with the following structure:
    {
        'category_name': {
            'desciption': 'category_description',
            'amount': amount_of_money_spended_in_category,
            'products': {
                'name': 'roduct_name',
                'amount': amount_of_money_spended_in_product,
                'purchases': [purchase_list]
            }
        }
    }
    """
    purchases = Purchase.objects.filter(product__user__pk=user_id)
    categories = Category.objects.all()

    grouped_purchases = {}

    for category in categories:
        grouped_purchases[category.label] = {
            'description': category.description,
            'products': defaultdict(list)
        }

    for purchase in purchases:
        product = purchase.product.name
        category = purchase.product.category.label
        grouped_purchases[category]['products'][product].append(purchase)

    return grouped_purchases
