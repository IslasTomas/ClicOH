from sys import breakpointhook
from common.tests import CommonTestCase
from rest_framework import status
from rest_framework.reverse import reverse

from ..models import Product


class ProductTest(CommonTestCase):
    def test_get(self):
        url = reverse('product:product-detail',
                      kwargs={'pk': self.product1.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], str(self.product1.id))
        self.assertEqual(response.data['name'], self.product1.name)
        self.assertEqual(response.data['stock'], self.product1.stock)
        self.assertEqual(response.data['price'], self.product1.price)

    def test_get_badrequest(self):
        url = reverse('product:product-detail', kwargs={'pk': 1111111})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list(self):
        url = reverse('product:product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Product.objects.count())

        id_product = response.data[0]['id']
        product = Product.objects.get(id=id_product)

        self.assertEqual(response.data[0]['name'], product.name)
        self.assertEqual(response.data[0]['stock'], product.stock)
        self.assertEqual(response.data[0]['price'], product.price)

    def test_create(self):
        url = reverse('product:product-list')

        data = {
            'name': 'new product',
            'price': 7.5,
            'stock': 45

        }
        total_product_pre_create = Product.objects.count()
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), total_product_pre_create+1)

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['stock'], data['stock'])
        self.assertEqual(response.data['price'], data['price'])

        id_product = response.data['id']
        product = Product.objects.get(id=id_product)

        self.assertEqual(product.name, data['name'])
        self.assertEqual(product.stock, data['stock'])
        self.assertEqual(product.price, data['price'])

    def test_create_without_price(self):
        url = reverse('product:product-list')

        data = {
            'name': 'new product',
            'stock': 123
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_validate_name(self):
        url = reverse('product:product-list')

        data = {
            'name': 'Product 1',
            'stock': 123,
            'price': 12
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_stock(self):
        url = reverse('product:product-update-stock',
                      kwargs={'pk': self.product1.id})

        stock_pre_update = self.product1.stock
        data = {'stock': 200}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product1 = Product.objects.get(name=self.product1.name)
        self.assertNotEqual(product1.stock,
                            stock_pre_update)
        self.assertEqual(response.data['stock'], product1.stock)
        self.assertEqual(product1.stock, data['stock'])
