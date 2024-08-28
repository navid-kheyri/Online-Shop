from .models import Category, Product
from vendors.models import Vendor


def product_and_category(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    vendors = Vendor.objects.all()
    return {'categories': categories, 'products': products, 'vendors': vendors}
