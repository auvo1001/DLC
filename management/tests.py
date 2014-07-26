from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.test.client import RequestFactory
from management.models import Package, Sender, Receiver, Store, Tinh
from django.core.urlresolvers import reverse


class AddSenderTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_sender_access(self):
        c = Client()
        c.login(username='test', password='test')
        c.user = self.user
        added_sender = Sender.objects.create(fname="Jack", lname="Sparrow", address1="9550 Bolsa Ave", address2 = "DLXXx", city ="Westminster", state_province ="CA", zip="94049", phone="7142323232", email = "deluxe@cargo.com")
        added_id = "/management/sender/%s/" % (added_sender.phone,)
        response = c.get(added_id)
        self.assertEqual(response.status_code, 200)

class AddReceiverTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_receiver_access(self):
        c = Client()
        c.login(username='test', password='test')
        c.user = self.user
        addded_tinh = Tinh.objects.create(name="Sai Gon", region ="Nam", price_type = 3)
        added_sender = Sender.objects.create(fname="Jack", lname="Sparrow", address1="9550 Bolsa Ave", address2 = "DLXXx", city ="Westminster", state_province ="CA", zip="94049", phone="7142323232", email = "deluxe@cargo.com")
        added_receiver = Receiver.objects.create(fname="Jack", lname="Sparrow", address1="9550 Bolsa Ave", address2 = "DLXXx", quan_huyen ="Westminster", tinh_thanhpho_id =1   , phone1="7142323232", phone2="7142323232", email = "deluxe@cargo.com")
        added_id = "/management/sender/%s/receiver/%s/" % (added_sender.phone,added_receiver.phone1)
        response = c.get(added_id)
        self.assertEqual(response.status_code, 200)

class AddPackageTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_package_2lbs(self):
        c = Client()
        c.login(username='test', password='test')
        c.user = self.user
        addded_tinh = Tinh.objects.create(
            name="Sai Gon",
            region ="Nam",
            price_type = 3
        )
        added_sender = Sender.objects.create(
            fname="Jack",
            lname="Sparrow",
            address1="9550 Bolsa Ave",
            address2 = "DLXXx",
            city ="Westminster",
            state_province ="CA",
            zip="94049",
            phone="7142323232",
            email = "deluxe@cargo.com"
                                        )
        added_receiver = Receiver.objects.create(
            fname="Jack",
            lname="Sparrow",
            address1="9550 Bolsa Ave",
            address2 = "DLXXx",
            quan_huyen ="Westminster",
            tinh_thanhpho_id =1   ,
            phone1="7142323232",
            phone2="7142323232",
            email = "deluxe@cargo.com"
        )
        added_package = Package.objects.create(
            sender_id=1,
            receiver_id=1,
            weight = 2,
            piece = 1,
            content = "stuff",
            value = 100,
            insurance = 0,
            tax = 0,
            extra_charge = 0,
            type = "Door To Door",
        )
        added_id = "/management/sender/%s/receiver/%s/package/%s/" % (added_sender.phone,added_receiver.phone1, added_package.id)
        response = c.get(added_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(added_package.subtotal(),15 )

    def test_package_20lbs(self):
        c = Client()
        c.login(username='test', password='test')
        c.user = self.user
        addded_tinh = Tinh.objects.create(
            name="Sai Gon",
            region ="Nam",
            price_type = 3
        )
        added_sender = Sender.objects.create(
            fname="Jack",
            lname="Sparrow",
            address1="9550 Bolsa Ave",
            address2 = "DLXXx",
            city ="Westminster",
            state_province ="CA",
            zip="94049",
            phone="7142323232",
            email = "deluxe@cargo.com"
                                        )
        added_receiver = Receiver.objects.create(
            fname="Jack",
            lname="Sparrow",
            address1="9550 Bolsa Ave",
            address2 = "DLXXx",
            quan_huyen ="Westminster",
            tinh_thanhpho_id =1   ,
            phone1="7142323232",
            phone2="7142323232",
            email = "deluxe@cargo.com"
        )
        added_package = Package.objects.create(
            sender_id=1,
            receiver_id=1,
            weight = 20,
            piece = 1,
            content = "stuff",
            value = 100,
            insurance = 0,
            tax = 0,
            extra_charge = 0,
            type = "Door To Door",
        )
        added_id = "/management/sender/%s/receiver/%s/package/%s/" % (added_sender.phone,added_receiver.phone1, added_package.id)
        response = c.get(added_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(added_package.subtotal(),55 )

    def test_package_40lbs(self):
        c = Client()
        c.login(username='test', password='test')
        c.user = self.user
        addded_tinh = Tinh.objects.create(
            name="Sai Gon",
            region ="Nam",
            price_type = 3
        )
        added_sender = Sender.objects.create(
            fname="Jack",
            lname="Sparrow",
            address1="9550 Bolsa Ave",
            address2 = "DLXXx",
            city ="Westminster",
            state_province ="CA",
            zip="94049",
            phone="7142323232",
            email = "deluxe@cargo.com"
                                        )
        added_receiver = Receiver.objects.create(
            fname="Jack",
            lname="Sparrow",
            address1="9550 Bolsa Ave",
            address2 = "DLXXx",
            quan_huyen ="Westminster",
            tinh_thanhpho_id =1   ,
            phone1="7142323232",
            phone2="7142323232",
            email = "deluxe@cargo.com"
        )
        added_package = Package.objects.create(
            sender_id=1,
            receiver_id=1,
            weight = 40,
            piece = 5,
            content = "stuff",
            value = 100,
            insurance = 5,
            tax = 5,
            extra_charge = 10,
            type = "Door To Door",
        )
        added_id = "/management/sender/%s/receiver/%s/package/%s/" % (added_sender.phone,added_receiver.phone1, added_package.id)
        response = c.get(added_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(added_package.subtotal(),120 )