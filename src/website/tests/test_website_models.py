# from django.test import TestCase
# from ..models import Product, ProductImage, Comment, Rating, Category, User, Vendor


# class TestCategoryModel(TestCase):
#     def test_create_category(self):
#         category = Category.objects.create(name='test', description='test desc', image='media/default.jpg',
#                                            )
#         sub_category = Category.objects.create(name='test1', description='test desc1', image='media/default.jpg',
#                                                parent=category)

#         self.assertEqual(sub_category.name, 'test1')
#         self.assertEqual(sub_category.description, 'test desc1')
#         self.assertEqual(sub_category.image, 'media/default.jpg')
#         self.assertEqual(sub_category.parent, category)


# class TestProductModel(TestCase):
#     def test_create_product(self):
#         user_obj = User.objects.create(email='navid@gmail.com', phone_number='09121234567',
#                                        age=30, city='tehran', user_type='customer')
#         category_obj = Category.objects.create(
#             name='test cat', description='test cat desc')
#         vendor_obj = Vendor.objects.create(name='test vendor', phone='02188888888', email='test@gmail.com',
#                                            status=True, address='azadi street')
#         vendor_obj.user.add(user_obj)

#         product = Product.objects.create(name='test', quantity_in_stock=15, description='test desc',
#                                          price=550, category=category_obj)
#         product.vendor.add(vendor_obj)

#         self.assertEqual(product.vendor.get(pk=vendor_obj.pk), vendor_obj)
#         self.assertEqual(product.category, category_obj)
#         self.assertEqual(product.name, 'test')
#         self.assertEqual(product.quantity_in_stock, 15)
#         self.assertEqual(product.description, 'test desc')
#         self.assertEqual(product.price, 550)


# class TestCommentModel(TestCase):
#     def test_create_product(self):
#         user_obj = User.objects.create_user(email='navid@gmail.com', phone_number='09121234567',
#                                        password='123', age=30, city='tehran', user_type='customer')
#         category_obj = Category.objects.create(
#             name='test cat', description='test cat desc')
#         vendor_obj = Vendor.objects.create(name='test vendor', phone='02188888888', email='test@gmail.com',
#                                            status=True, address='azadi street')
#         vendor_obj.user.add(user_obj)

#         product_obj = Product.objects.create(name='test', quantity_in_stock=15, description='test desc',
#                                              price=550, category=category_obj)
#         product_obj.vendor.add(vendor_obj)
#         comment = Comment.objects.create(title='test', description='test desc', user=user_obj,
#                                          product=product_obj, comment_type='pending')

#         self.assertEqual(comment.title, 'test')
#         self.assertEqual(comment.comment_type, 'pending')
