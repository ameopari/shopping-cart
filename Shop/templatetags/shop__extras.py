from django import template
from Shop.models import CartItem

register = template.Library()

@register.filter()
def get_cart_qty(product,user):
         print(user,'============kwargs')
         try:
            item = CartItem.objects.get(product = product, cart__user = user)
            return item.quantity
         except CartItem.DoesNotExist:
             return 0
