"""
Manipulate accounting data to be used in views.
"""
from collections import defaultdict

from django.db.models import Q, Sum
from django.utils.text import slugify

from accounting.models import Category, Product, Purchase


def purchases_by_categories(user_id, from_date, to_date):
    """
    Group purchases by categories. Returns a dict with the following structure:
    {
        'category_name': {
            'slug': 'category_label_slug',
            'desciption': 'category_description',
            'amount': amount_of_money_spended_in_category,
            'purchases': [purchases_list]
            }
        }
    }
    """
    purchases = Purchase.objects.filter(
        product__user__pk=user_id,
        date__range=(from_date, to_date)
    )
    category_amount = Sum(
        'products__purchases__value',
        filter=Q(
            products__user__pk=user_id,
            products__purchases__date__range=(from_date, to_date)
        )
    )
    categories = Category.objects.all().annotate(amount=category_amount)

    grouped_purchases = {}

    for category in categories:
        grouped_purchases[category.label] = {
            'slug': slugify(category.label),
            'description': category.description,
            'amount': category.amount,
            'purchases': []
        }

    for purchase in purchases:
        category = purchase.product.category.label
        grouped_purchases[category]['purchases'].append(purchase)

    return grouped_purchases
