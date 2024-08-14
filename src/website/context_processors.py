from .models import Category, Product

def product_and_category(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return {'categories': categories,'products': products}
