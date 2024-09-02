# from django.test import TestCase, Client
# from ..models import Address
# from accounts.models import CustomUser


# class AddressTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user_obj = CustomUser.objects.create_user(email='hasan@gmail.com', phone_number='09131234567',
#                                                   password='123', age=30, city='tehran', user_type='customer')

#     def test_create_address(self):
#         self.addr_obj = Address(state='tehran', city='tehran',
#                                 street='azadi', zipcode='0123456789', user=self.user_obj)
#         self.assertEqual(self.addr_obj.state, 'tehran')
#         self.assertEqual(self.addr_obj.city, 'tehran')
#         self.assertEqual(self.addr_obj.street, 'azadi')
#         self.assertEqual(self.addr_obj.zipcode, '0123456789')
#         self.assertEqual(self.addr_obj.user, self.user_obj)
