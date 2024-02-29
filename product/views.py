from django.db.utils import IntegrityError
from django.shortcuts import render
from django.contrib import messages

import pandas as pd
import numpy as np
from decimal import Decimal
import time

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Producto
# Create your views here.


@login_required
def index(request):
    return redirect('product:load_v2')
    # return render(request, "product/index.html")


@login_required
def load_data(request):
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo = request.FILES['archivo_csv']

        # Check if the uploaded file has a CSV extension
        if not archivo.name.endswith('.csv'):
            messages.warning(request, 'El archivo debe ser un archivo CSV.')
            return render(request, "product/load_data.html")


        data_frame = pd.read_csv(archivo, na_values=['NaN', 'N/A', '', 'nan'])
        # Convertir nombres de columnas a minúsculas
        data_frame.columns = data_frame.columns.str.lower()

        for index, row in data_frame.iterrows():
            # import pdb; pdb.set_trace()
            try:
                if not row.get('codigo', None):
                    continue

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

@login_required
def load_data_v2(request):
    start_time = time.time()

    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo = request.FILES['archivo_csv']

        # Verificar si el archivo subido tiene una extensión CSV
        if not archivo.name.endswith('.csv'):
            messages.warning(request, 'El archivo debe ser un archivo CSV.')
            return render(request, "product/load_data.html")

        # Cargar datos del archivo CSV
        data_frame = pd.read_csv(archivo, na_values=['NaN', 'N/A', '', 'nan'])
        data_frame.columns = data_frame.columns.str.lower()

        # Obtener códigos de productos del DataFrame
        codigos_productos = data_frame['codigo'].tolist()

        # Filtrar productos existentes en la base de datos por sus códigos
        productos_existentes = Producto.objects.filter(codigo__in=codigos_productos)

        phase1_time = time.time() - start_time
        print(f"Fase 1: {phase1_time} segundos")

        # Actualizar los productos existentes con los nuevos valores del DataFrame
        for producto_existente in productos_existentes:
            row = data_frame[data_frame['codigo'] == producto_existente.codigo].iloc[0]

            producto_existente.nombre = row.get('nombre', None)
            producto_existente.marca = row.get('marca', None)
            producto_existente.linea = row.get('linea', None)
            producto_existente.sublinea = row.get('sublinea', None)
            producto_existente.departamento = row.get('departamento', None)
            producto_existente.costo = row.get('costo', None)
            producto_existente.precio1 = row.get('precio1', None)
            producto_existente.ptje1 = row.get('ptje1', None)
            producto_existente.ptjeReal = row.get('ptjeReal', None)
            producto_existente.precioCalculado = row.get('precioCalculado', None)
            producto_existente.maximo = row.get('maximo', None)
            producto_existente.minimo = row.get('minimo', None)
            producto_existente.estatus = row.get('estatus', None)
            producto_existente.nombreStatus = row.get('nombreStatus', None)
            producto_existente.tipoProd = row.get('tipoProd', None)
            producto_existente.tipoProdDesc = row.get('tipoProdDesc', None)
            producto_existente.codigosAlternos = row.get('codigosAlternos', None)
            producto_existente.activo = row.get('activo', None)
            producto_existente.prov = row.get('prov', None)
            producto_existente.nombreProveedor = row.get('nombreProveedor', None)
            producto_existente.unidad = row.get('unidad', None)
            producto_existente.codigoSat = row.get('codigoSat', None)
            producto_existente.nomCodSat = row.get('nomCodSat', None)
            producto_existente.unidadSat = row.get('unidadSat', None)
            producto_existente.nomUniSat = row.get('nomUniSat', None)

        phase2_time = time.time() - start_time
        print(f"Fase 2: {phase2_time} segundos")

        # Separate new and existing elements
        existing_codigos = Producto.objects.values_list('codigo', flat=True)
        nuevos_productos = [p for p in productos_existentes if p.codigo not in existing_codigos]

        # Check if there are new elements and show how many new elements are new and how many are loaded
        new_elements_count = len(nuevos_productos)
        existing_elements_count = len(productos_existentes) - new_elements_count
        messages.info(request, f'Se encontraron {new_elements_count} elementos nuevos y se actualizaran {existing_elements_count} elementos existentes.')

        phase3_time = time.time() - start_time
        print(f"Fase 3: {phase3_time} segundos")

        # Make bulk update for existing elements
        if productos_existentes:
            try:
                Producto.objects.bulk_update(productos_existentes, fields=[
                    "nombre", "marca", "linea", "sublinea", "departamento",
                    "costo", "precio1", "ptje1", "ptjeReal", "precioCalculado",
                    "maximo", "minimo", "estatus", "nombreStatus", "tipoProd",
                    "tipoProdDesc", "codigosAlternos", "activo", "prov",
                    "nombreProveedor", "unidad", "codigoSat", "nomCodSat",
                    "unidadSat", "nomUniSat"
                ])
            except IntegrityError:
                print("Error al actualizar los productos.")
                messages.error(request, "Hubo un error al actualizar los productos.")
            else:
                messages.success(request, "Se actualizó correctamente la información de los productos.")
        
        phase4_time = time.time() - start_time
        print(f"Fase 4: {phase4_time} segundos")

        # Make bulk create for new elements
        if nuevos_productos:
            try:
                Producto.objects.bulk_create(nuevos_productos)
            except IntegrityError:
                print("Error al crear nuevos productos.")
                messages.error(request, "Hubo un error al crear nuevos productos.")
            else:
                messages.success(request, "Se crearon los nuevo elementos correctamente.")
            
        
        phase5_time = time.time() - start_time
        print(f"Fase 5: {phase5_time} segundos")

    return render(request, "product/load_data.html")
