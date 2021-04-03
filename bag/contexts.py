from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    delivery = 0
    product = Product.objects.all()
    free_delivery_delta = 0
    delivery_cost = []
    data = ()


    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            if product.is_membership:
                delivery_cost = total * Decimal(settings.MEMBERSHIP_DELIVERY_PERCENTAGE / 100)
            else:
                delivery_cost = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                delivery = sum(delivery_price)
                product_count += quantity
                if product.is_membership:
                    delivery_cost = total * Decimal(settings.MEMBERSHIP_DELIVERY_PERCENTAGE / 100)
                else:
                    delivery_cost = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
                bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'size': size,
            })

        data = list(map(Decimal,[delivery_cost])) 

    print("Sum: ", sum(data))

    delivery = sum(data)
                
    grand_total = delivery + total

    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context