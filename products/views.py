from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from .models import Product, Category, City
from .forms import ProductForm, CityForm


def all_products(request):
    """A view to show all products indluding sorting and search excluding tickets"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    city = None


    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.filter(is_searchable__in=products)
            products = products.order_by(sortkey)


    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

    if request.GET: 
        if 'city' in request.GET:
            city = request.GET['city'].split(',')
            products = products.filter(city__name__in=city)
            city = City.objects.filter(name__in=city)
        

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))


            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(is_searchable__in=products)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'current_city': city,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """Show a singular product"""

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Successfully added product")
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid')

    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_city(request):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form_city = CityForm(request.POST, request.FILES)
        if form_city.is_valid():
            city = form_city.save()
            messages.success(request, "Successfully added city")
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add city. Please ensure the form is valid')

    else:
        form_city = CityForm()

    template = 'products/add_city.html'
    context = {
        'form_city': form_city,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated this product')
            return redirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product has been deleted')
    return redirect(reverse('products'))


def membership(request):
    """A view to show find tickets"""
    
    products = Product.objects.all()
    categories = None


    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)


    context = {
        'products': products,
        'current_categories': categories,
    }

    template = 'products/membership.html'

    return render(request, template, context)


def member_detail(request, product_id):
    """Show a singular product"""

    product = get_object_or_404(Product, pk=product_id)

    bag = request.session.get('bag', {})

    member = Product.objects.get(id=product_id)

    for item in bag:
        if item == str(member.id):
            member = True


    context = {
        'product': product,
        'bag': bag,
        'member': member,
    }


    return render(request, 'products/member_detail.html', context)
