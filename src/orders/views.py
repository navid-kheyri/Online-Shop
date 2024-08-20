from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from customers.models import Address
from website.models import Product
from .froms import AddressModelForm
from .cart import Cart

# Create your views here.


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        total = cart.get_total_price()
        my_cart = cart.session.get('session_key')
        product_ids = list(my_cart.keys())
        products = []
        for prod_id in product_ids:
            product = get_object_or_404(Product, pk=int(prod_id))
            quantity = my_cart[prod_id]['quantity']
            product_total_price = float(my_cart[prod_id]['price']) * quantity
            products.append({'product': product, 'quantity': quantity,
                            'product_total_price': product_total_price})
        return render(request, 'orders/cart-detail.html', {'total': total, 'products': products})


class NewAddressCreateView(CreateView):
    model = Address
    template_name = 'orders/add-address.html'
    form_class = AddressModelForm
    success_url = reverse_lazy("orders:cart-detail")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
