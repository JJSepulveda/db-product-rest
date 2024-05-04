from rest_framework import serializers
from product.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            "id",
            "codigo",
            "nombre",
            "marca",
            "linea",
            "sublinea",
            "departamento",
            "costo",
            "precio1",
            "ptje1",
            "ptjeReal",
            "precioCalculado",
            "maximo",
            "minimo",
            "estatus",
            "nombreStatus",
            "tipoProd",
            "tipoProdDesc",
            "codigosAlternos",
            "activo",
            "prov",
            "nombreProveedor",
            "unidad",
            "codigoSat",
            "nomCodSat",
            "unidadSat",
            "nomUniSat",
            "existencia",
        ]


class ProductoSerializerV2(serializers.ModelSerializer):
    warehouses = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = [
            "id",
            "codigo",
            "nombre",
            "marca",
            "precioCalculado",
            "codigoSat",
            "nomCodSat",
            "unidadSat",
            "nomUniSat",
            "warehouses",
        ]

    def get_warehouses(self, obj):
        warehouse_fields = [
            "existencia",
            "existenciaPiso",
            "existenciaProd",
            "existenciaTubos",
            "existenciaTanques",
            "existenciaDistr",
            "existenciaMakita",
            "existenciaStaRosa",
            "existenciaTotal",
        ]
        warehouses_data = {field: getattr(obj, field) for field in warehouse_fields}
        return warehouses_data


class ProductoStockSerializer(serializers.ModelSerializer):
    warehouses = serializers.SerializerMethodField()
    class Meta:
        model = Producto
        fields = [
            "id",
            "codigo",
            "nombre",
            "onlinePrice",
            "warehouses"
        ]

    def get_warehouses(self, obj):
        warehouse_fields = [
            "existencia",
            "existenciaPiso",
            "existenciaProd",
            "existenciaTubos",
            "existenciaTanques",
            "existenciaDistr",
            "existenciaMakita",
            "existenciaStaRosa",
            "existenciaTotal",
        ]
        warehouses_data = {field: getattr(obj, field) for field in warehouse_fields}
        return warehouses_data
