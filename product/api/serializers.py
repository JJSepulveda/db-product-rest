from rest_framework import serializers
from product.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre"]
        