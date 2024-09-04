from django.test import TestCase, Client
from ..models import Order, OrderItem, User, Address, Product
from website.models import Category
from vendors.models import Vendor


class TestOrderModel(TestCase):
    def test_create_order(self):
        user_obj = User.objects.create(email='navid@gmail.com', phone_number='09121234567',
                                       age=30, city='tehran', user_type='customer')
        addr_obj = Address.objects.create(user=user_obj,
                                          state='qazvin', city='falake aval', street='azadi')
        order = Order.objects.create(
            status='processing', user=user_obj, address=addr_obj)
        self.assertEqual(order.status, 'processing')
        self.assertEqual(order.user, user_obj)
        self.assertEqual(order.address, addr_obj)


class TestOrderItemModel(TestCase):
    def test_create_orderitem(self):
        user_obj = User.objects.create_user(email='navid@gmail.com', phone_number='09121234567',
                                       password='123', age=30, city='tehran', user_type='customer')
        addr_obj = Address.objects.create(user=user_obj,
                                          state='qazvin', city='falake aval', street='azadi')
        order_obj = Order.objects.create(
            status='processing', user=user_obj, address=addr_obj)
        category_obj = Category.objects.create(
            name='test cat', description='test cat desc')
        product_obj = Product.objects.create(name='test', quantity_in_stock=15, description='test dest',
                                             price=550, category=category_obj)
        vendor_obj = Vendor.objects.create(name='test vendor', phone='02188888888', email='test@gmail.com',
                                           status=True, address=addr_obj)
        vendor_obj.user.add(user_obj)
        product_obj.vendor.add(vendor_obj)
        orderitem = OrderItem.objects.create(quantity=10, item_total_price=1000.00, product=product_obj,
                                             order=order_obj)

        self.assertEqual(vendor_obj.user.get(pk=user_obj.pk), user_obj)
        self.assertEqual(product_obj.vendor.get(pk=vendor_obj.pk), vendor_obj)
        self.assertEqual(orderitem.quantity, 10)
        self.assertEqual(orderitem.item_total_price, 1000.00)
        self.assertEqual(orderitem.product, product_obj)
        self.assertEqual(orderitem.order, order_obj)
