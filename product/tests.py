from django.test import TestCase
from product.models import Producto  # Ajusta el import según tu aplicación y modelo
from .views import (
    create_new_products_from_csv,
    update_products,
    try_convert
)

import pandas as pd
import os
from decimal import Decimal


class TuTest(TestCase):
    def test_create_new_products_from_csv(self):
        # Obtiene la ruta del directorio actual de la prueba
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Concatena el nombre del archivo CSV al directorio actual
        csv_file_path = os.path.join(current_directory, "articulos_test.csv")

        # Cargar el DataFrame desde el archivo CSV
        test_data_frame = pd.read_csv(csv_file_path, na_values=["NaN", "N/A", "", "nan"])
        
        product_list = create_new_products_from_csv(["AOC14"], test_data_frame)

        # Verifica que la lista de productos no esté vacía
        self.assertGreater(len(product_list), 0)

        # Verifica que los productos creados tengan los valores correctos
        for product in product_list:
            if product.codigo == "AOC14":
                data = test_data_frame[test_data_frame["codigo"] == "AOC14"].iloc[0]
                self.assertEqual(product.codigo, str(data["codigo"]))
                self.assertEqual(product.nombre, str(data["nombre"]))
                self.assertEqual(product.marca, str(data["marca"]))
                self.assertEqual(product.linea, str(data["linea"]))
                self.assertEqual(product.sublinea, str(data["sublinea"]))
                self.assertEqual(product.departamento, str(data["departamento"]))
                self.assertEqual(product.costo, Decimal(str(data["costo"])))
                self.assertEqual(product.precio1, Decimal(str(data["precio1"])))
                self.assertEqual(product.ptje1, Decimal(str(data["ptje1"])))
                self.assertEqual(product.ptjeReal, Decimal(str(data["ptjeReal"])))
                self.assertEqual(product.precioCalculado, Decimal(str(data["precioCalculado"])))
                self.assertEqual(product.maximo, Decimal(str(data["maximo"])))
                self.assertEqual(product.minimo, Decimal(str(data["minimo"])))
                self.assertEqual(product.estatus, int(str(data["estatus"])))
                self.assertEqual(product.nombreStatus, str(data["nombreStatus"]))
                self.assertEqual(product.tipoProd, int(str(data["tipoProd"])))
                self.assertEqual(product.tipoProdDesc, str(data["tipoProdDesc"]))
                self.assertEqual(product.codigosAlternos, str(data["codigosAlternos"]))
                self.assertEqual(product.activo, bool(str(data["activo"])))
                self.assertEqual(product.prov, str(data["prov"]))
                self.assertEqual(product.nombreProveedor, str(data["nombreProveedor"]))
                self.assertEqual(product.unidad, str(data["unidad"]))
                self.assertEqual(product.codigoSat, str(data["codigoSat"]))
                self.assertEqual(product.nomCodSat, str(data["nomCodSat"]))
                self.assertEqual(product.unidadSat, str(data["unidadSat"]))
                self.assertEqual(product.nomUniSat, str(data["nomUniSat"]))
    
    def test_update_products_from_csv(self):
        # Obtiene la ruta del directorio actual de la prueba
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Concatena el nombre del archivo CSV al directorio actual
        csv_file_path = os.path.join(current_directory, "articulos_test.csv")

        # Cargar el DataFrame desde el archivo CSV
        test_data_frame = pd.read_csv(csv_file_path, na_values=["NaN", "N/A", "", "nan"])

        codigos_productos = test_data_frame['codigo'].tolist()
        # Primero creamos los productos
        products = create_new_products_from_csv(codigos_productos, test_data_frame)
        Producto.objects.bulk_create(products)
        # Ahora vamos a intentar actualizarlos
        product_list = update_products(codigos_productos, test_data_frame)

        # Verifica que la lista de productos no esté vacía
        self.assertGreater(len(product_list), 0)

        # Verifica que los productos creados tengan los valores correctos
        for product in product_list:
            data = test_data_frame[test_data_frame["codigo"] == product.codigo].iloc[0]
            self.assertEqual(product.codigo, str(data["codigo"]))
            self.assertEqual(product.nombre, str(data["nombre"]))
            self.assertEqual(product.marca, try_convert(data, 'marca', str))
            self.assertEqual(product.linea, try_convert(data, 'linea', str))
            self.assertEqual(product.sublinea, try_convert(data, 'sublinea', str))
            self.assertEqual(product.departamento, try_convert(data, 'departamento', str))
            self.assertEqual(product.costo, try_convert(data, 'costo', Decimal))
            self.assertEqual(product.precio1, try_convert(data, 'precio1', Decimal))
            self.assertEqual(product.ptje1, try_convert(data, 'ptje1', Decimal))
            self.assertEqual(product.ptjeReal, try_convert(data, 'ptjeReal', Decimal))
            self.assertEqual(product.precioCalculado, try_convert(data, 'precioCalculado', Decimal))
            self.assertEqual(product.maximo, try_convert(data, 'maximo', int))
            self.assertEqual(product.minimo, try_convert(data, 'minimo', int))
            self.assertEqual(product.estatus, try_convert(data, 'estatus', int))
            self.assertEqual(product.nombreStatus, try_convert(data, 'nombreStatus', str))
            self.assertEqual(product.tipoProd, try_convert(data, 'tipoProd', int))
            self.assertEqual(product.tipoProdDesc, try_convert(data, 'tipoProdDesc', str))
            self.assertEqual(product.codigosAlternos, try_convert(data, 'codigosAlternos', str))
            self.assertEqual(product.activo, try_convert(data, 'activo', bool))
            self.assertEqual(product.prov, try_convert(data, 'prov', str))
            self.assertEqual(product.nombreProveedor, try_convert(data, 'nombreProveedor', str))
            self.assertEqual(product.unidad, try_convert(data, 'unidad', str))
            self.assertEqual(product.codigoSat, try_convert(data, 'codigoSat', str))
            self.assertEqual(product.nomCodSat, try_convert(data, 'nomCodSat', str))
            self.assertEqual(product.unidadSat, try_convert(data, 'unidadSat', str))
            self.assertEqual(product.nomUniSat, try_convert(data, 'nomUniSat', str))
    
    def test_create_new_product_from_incomplete_csv(self):
        producto = {
            "codigo": "AOC14",
            "nombre": 'ABRAZ OMG CB01  1/4"  4PZ',
            "marca": "BARNETT",
            "ptjeReal": 302.2988506,
            "precioCalculado": "14",
            "unidad": "PZA",
            "codigoSat": "27112132",
            "nomCodSat": "Abrazaderas de fijación",
            "unidadSat": "XPK",
            "nomUniSat": "PAQUETE",
        }

        # Obtiene la ruta del directorio actual de la prueba
        current_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Concatena el nombre del archivo CSV al directorio actual
        csv_file_path = os.path.join(current_directory, "articulos_test copy.csv")

        # Cargar el DataFrame desde el archivo CSV
        test_data_frame = pd.read_csv(csv_file_path, na_values=["NaN", "N/A", "", "nan"])
        
        product_list = create_new_products_from_csv(["AOC14"], test_data_frame)

        # Verifica que la lista de productos no esté vacía
        self.assertGreater(len(product_list), 0)

        # Verifica que los productos creados tengan los valores correctos
        for product in product_list:
            if product.codigo == producto['codigo']:
                self.assertEqual(product.codigo, producto["codigo"])
                self.assertEqual(product.nombre, producto["nombre"])
                self.assertEqual(product.marca, producto["marca"])
                self.assertEqual(product.ptjeReal, Decimal(str(producto["ptjeReal"])))
                self.assertEqual(product.precioCalculado, Decimal(producto["precioCalculado"]))
                self.assertEqual(product.unidad, producto["unidad"])
                self.assertEqual(product.codigoSat, producto["codigoSat"])
                self.assertEqual(product.nomCodSat, producto["nomCodSat"])
                self.assertEqual(product.unidadSat, producto["unidadSat"])
                self.assertEqual(product.nomUniSat, producto["nomUniSat"])
    