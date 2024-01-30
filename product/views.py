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
        # Convertir nombres de columnas a minúsculas
        data_frame.columns = data_frame.columns.str.lower()

        for index, row in data_frame.iterrows():
            # import pdb; pdb.set_trace()
            try:
                producto, created = Producto.objects.update_or_create(
                    codigo=row['codigo'],
                    defaults= {
                        "nombre": row.get('nombre', None),
                        "marca": row.get('marca', None),
                        "linea": row.get('linea', None),
                        "sublinea": row.get('sublinea', None),
                        "departamento": row.get('departamento', None),
                        "costo": row.get('costo', None),
                        "precio1": row.get('precio1', None),
                        "ptje1": row.get('ptje1', None),
                        "ptjeReal": row.get('ptjeReal', None),
                        "precioCalculado": row.get('precioCalculado', None),
                        "maximo": row.get('maximo', None),
                        "minimo": row.get('minimo', None),
                        "estatus": row.get('estatus', None),
                        "nombreStatus": row.get('nombreStatus', None),
                        "tipoProd": row.get('tipoProd', None),
                        "tipoProdDesc": row.get('tipoProdDesc', None),
                        "codigosAlternos": row.get('codigosAlternos', None),
                        "activo": row.get('activo', None),
                        "prov": row.get('prov', None),
                        "nombreProveedor": row.get('nombreProveedor', None),
                        "unidad": row.get('unidad', None),
                        "codigoSat": row.get('codigoSat', None),
                        "nomCodSat": row.get('nomCodSat', None),
                        "unidadSat": row.get('unidadSat', None),
                        "nomUniSat": row.get('nomUniSat', None),
                    }
                )
            except IntegrityError:
                print("Error al insertar el producto: ", row['codigo'])
                pass
        
        messages.success(
            request, "Se actualizo correctamente la información del producto "
        )

    return render(request, "product/load_data.html")
