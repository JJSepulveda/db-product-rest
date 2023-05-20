from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Producto
from .serializers import ProductoSerializer
from rest_framework_api_key.models import APIKey


class ProductListCreateTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("product_api:product-list")
        self.product_data = {"nombre": "Product 1", "costo": 10.99, "codigo": "abc"}  # Datos de ejemplo para crear un producto
        _, api_key = APIKey.objects.create_key(name="my-remote-service")
        self.headers = {'Authorization': f'Api-Key {api_key}'}  # Agregar el API Key

    def test_create_product(self):
        # Verificar que se crea un producto válido
        response = self.client.post(self.url, self.product_data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 1)
        self.assertEqual(Producto.objects.get().nombre, self.product_data["nombre"])

    def test_create_product_invalid_data(self):
        # Verificar que no se puede crear un producto con datos inválidos
        invalid_data = {"name": "Product 1"}  # Falta el campo 'price'
        response = self.client.post(self.url, invalid_data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Producto.objects.count(), 0)

    def test_list_products(self):
        # Verificar que se obtiene una lista de productos
        Producto.objects.create(nombre="Product 1", costo=10.99, codigo="abc")
        Producto.objects.create(nombre="Product 2", costo=20.99, codigo="def")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]["nombre"], "Product 1")
        self.assertEqual(response.data['results'][1]["nombre"], "Product 2")

    def test_list_products_empty(self):
        # Verificar que se obtiene una lista vacía de productos
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
