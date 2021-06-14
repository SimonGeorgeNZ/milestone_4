from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    product = Product.objects.all()
    delivery = 0
    FDT = settings.FREE_DELIVERY_THRESHOLD


    for item_id, item_data in bag.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += item_data * product.price
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'size': size,
            })

        for product in bag.items():
            product = get_object_or_404(Product, pk=item_id)
        if product.is_membership:
            delivery_cost = Decimal(0)
            FDT = 75
            if total > FDT:
                print("member and more")
            else:
                print("member and less")
        else:
            delivery_cost = Decimal(product.price * settings.STANDARD_DELIVERY_PERCENTAGE / 100)
            if total < FDT:
                print("not member and less")
            else:
                print("not member and more")
        print(delivery_cost)

        delivery += delivery_cost

    print(FDT)
    print(delivery)


    
    #grand_total = delivery + total
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_threshold': FDT,
        'grand_total': grand_total,
    }


    return context