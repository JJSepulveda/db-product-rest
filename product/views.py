from django.db.utils import IntegrityError
from django.shortcuts import render
from django.contrib import messages

import pandas as pd
import numpy as np
from decimal import Decimal

from .models import Producto
# Create your views here.

def index(request):
    return render(request, "product/index.html")


def load_data(request):
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo = request.FILES['archivo_csv']
        data_frame = pd.read_csv(archivo, na_values=['NaN', 'N/A', '', 'nan'])

        for index, row in data_frame.iterrows():
            try:
                producto, created = Producto.objects.update_or_create(
                    codigo=row['codigo'],
                    defaults= {
                        "nombre": None if pd.isnull(row['nombre']) else row['nombre'],
                        "marca": None if pd.isnull(row['marca']) else row['marca'],
                        "linea": None if pd.isnull(row['linea']) else row['linea'],
                        "sublinea": None if pd.isnull(row['sublinea']) else row['sublinea'],
                        "departamento": None if pd.isnull(row['departamento']) else row['departamento'],
                        "costo": None if pd.isnull(row['costo']) else row['costo'],
                        "precio1": None if pd.isnull(row['precio1']) else row['precio1'],
                        "ptje1": None if pd.isnull(row['ptje1']) else row['ptje1'],
                        "ptjeReal": None if pd.isnull(row['ptjeReal']) else row['ptjeReal'],
                        "precioCalculado": None if pd.isnull(row['precioCalculado']) else row['precioCalculado'],
                        "maximo": None if pd.isnull(row['maximo']) else row['maximo'],
                        "minimo": None if pd.isnull(row['minimo']) else row['minimo'],
                        "estatus": None if pd.isnull(row['estatus']) else row['estatus'],
                        "nombreStatus": None if pd.isnull(row['nombreStatus']) else row['nombreStatus'],
                        "tipoProd": None if pd.isnull(row['tipoProd']) else row['tipoProd'],
                        "tipoProdDesc": None if pd.isnull(row['tipoProdDesc']) else row['tipoProdDesc'],
                        "codigosAlternos": None if pd.isnull(row['codigosAlternos']) else row['codigosAlternos'],
                        "activo": None if pd.isnull(row['activo']) else row['activo'],
                        "prov": None if pd.isnull(row['prov']) else row['prov'],
                        "nombreProveedor": None if pd.isnull(row['nombreProveedor']) else row['nombreProveedor'],
                        "unidad": None if pd.isnull(row['unidad']) else row['unidad'],
                        "codigoSat": None if pd.isnull(row['codigoSat']) else row['codigoSat'],
                        "nomCodSat": None if pd.isnull(row['nomCodSat']) else row['nomCodSat'],
                        "unidadSat": None if pd.isnull(row['unidadSat']) else row['unidadSat'],
                        "nomUniSat": None if pd.isnull(row['nomUniSat']) else row['nomUniSat'],
                    }
                )
                print(producto, created)
            except IntegrityError:
                print("Error al insertar el producto: ", row['codigo'])
                pass
        
        messages.success(
            request, "Se actualizo correctamente la información del producto "
        )

    return render(request, "product/load_data.html")
