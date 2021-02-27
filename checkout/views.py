from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51IDVY9ERPaEV4cobcrnnmn9lh4yAnXS6KVUDP2t3X9VPuLbyv7saBAAOLzhM5H4RGmpn99UWIlrAMoGOvcj4sx9R00xKDPp6zI',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)