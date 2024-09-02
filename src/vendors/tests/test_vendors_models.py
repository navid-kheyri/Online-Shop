# from django.test import TestCase, Client
# from ..models import Vendor, VendorImage, VendorRating, User


# class TestVendorModel(TestCase):
#     def test_create_vendor(self):
#         user_obj = User.objects.create(email='navid@gmail.com', phone_number='09121234567',
#                                        password='123', age=30, city='tehran', user_type='customer')

#         vendor = Vendor.objects.create(name='test vendor', phone='02188888888', email='test@gmail.com',
#                                        status=True, address='azadi meydoon')
#         vendor.user.add(user_obj)

#         self.assertEqual(vendor.user.get(pk=user_obj.pk), user_obj)
#         self.assertEqual(vendor.name, 'test vendor')
#         self.assertEqual(vendor.phone, '02188888888')
#         self.assertEqual(vendor.email, 'test@gmail.com')
#         self.assertTrue(vendor.status)
#         self.assertEqual(vendor.address, 'azadi meydoon')


# class TestVendorImage(TestCase):
#     def test_create_vendor_iamge(self):
#         user_obj = User.objects.create_user(email='navid@gmail.com', phone_number='09121234567',
#                                        password='123', age=30, city='tehran', user_type='customer')

#         vendor_obj = Vendor.objects.create(name='test vendor', phone='02188888888', email='test@gmail.com',
#                                            status=True, address='azadi meydoon')
#         vendor_obj.user.add(user_obj)

#         vendor_image = VendorImage.objects.create(
#             title='test', image='media/default.jpg', vendor=vendor_obj)

#         self.assertEqual(vendor_obj.user.get(pk=user_obj.pk), user_obj)
#         self.assertEqual(vendor_image.title, 'test')
#         self.assertEqual(vendor_image.image, 'media/default.jpg')


# class TestVendorRating(TestCase):
#     def test_create_vendor_rating(self):
#         user_obj = User.objects.create_user(email='navid@gmail.com', phone_number='09121234567',
#                                        password='123', age=30, city='tehran', user_type='customer')

#         vendor_obj = Vendor.objects.create(name='test vendor', phone='02188888888', email='test@gmail.com',
#                                            status=True, address='azadi meydoon')
#         vendor_obj.user.add(user_obj)

#         vendor_rating=VendorRating.objects.create(rating=4,user=user_obj,vendor=vendor_obj)
#         self.assertEqual(vendor_obj.user.get(pk=user_obj.pk), user_obj)
#         self.assertEqual(vendor_rating.rating , 4)
#         self.assertEqual(vendor_rating.user , user_obj)
#         self.assertEqual(vendor_rating.vendor , vendor_obj)