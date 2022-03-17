import json
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.contrib.auth import get_user_model

from apps.product.models import Product
from apps.order.models import Order, OrderDetail

User = get_user_model()


class CommonTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.create_access_token()

    @classmethod
    def create_access_token(cls):
        username = 'test_user'
        password = 'test_password'
        cls.user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=False,

        )
        data = json.dumps({
            "username": username,
            "password": password
        })
        factory = APIRequestFactory()
        url = 'api/admin/login/'
        request = factory.post(
            url, data=data, content_type="application/json"
        )

        auth_view = TokenObtainPairView.as_view()
        response = auth_view(request)
        cls.access_token = response.data.get('access')

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f'JWT {self.access_token}',
            HTTP_ORIGIN='http://localhost:3000'
        )

        self.product1 = Product.objects.create(
            name='Product 1', price=5.5, stock=35)
        self.product2 = Product.objects.create(
            name='Product 2', price=15, stock=15)
        self.product3 = Product.objects.create(
            name='Product 3', price=75, stock=100)

        self.order1 = Order.objects.create()
        self.order2 = Order.objects.create()

        self.orderdetail1 = OrderDetail.objects.create(
            order=self.order1, cuantity=10, product=self.product1)
        self.orderdetail2 = OrderDetail.objects.create(
            order=self.order1, cuantity=5, product=self.product2)

        self.orderdetail3 = OrderDetail.objects.create(
            order=self.order2, cuantity=30, product=self.product3)
