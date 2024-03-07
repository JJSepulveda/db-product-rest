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

def create_new_products_from_csv(products_code, data_frame):
    # Actualizar los productos existentes con los nuevos valores del DataFrame
    product_list = []
    for code in products_code:
        row = data_frame[data_frame['codigo'] == code].iloc[0]

        # Validar el tipo de dato antes de la asignación
        product_object = Producto(
            codigo = code,
            nombre = str(row['nombre']) if row.get('nombre') is not None else None,
            marca = str(row['marca']) if row.get('marca') is not None else None,
            linea = str(row['linea']) if row.get('linea') is not None else None,
            sublinea = str(row['sublinea']) if row.get('sublinea') is not None else None,
            departamento = str(row['departamento']) if row.get('departamento') is not None else None,
            costo = Decimal(str(row['costo'])) if row.get('costo') is not None else None,
            precio1 = Decimal(str(row['precio1'])) if row.get('precio1') is not None else None,
            ptje1 = int(row['ptje1']) if row.get('ptje1') is not None else None,
            ptjeReal = int(row['ptjeReal']) if row.get('ptjeReal') is not None else None,
            precioCalculado = Decimal(str(row['precioCalculado'])) if row.get('precioCalculado') is not None else None,
            maximo = int(row['maximo']) if row.get('maximo') is not None else None,
            minimo = int(row['minimo']) if row.get('minimo') is not None else None,
            estatus = int(row['estatus']) if row.get('estatus') is not None else None,
            nombreStatus = str(row['nombreStatus']) if row.get('nombreStatus') is not None else None,
            tipoProd = int(row['tipoProd']) if row.get('tipoProd') is not None else None,
            tipoProdDesc = str(row['tipoProdDesc']) if row.get('tipoProdDesc') is not None else None,
            codigosAlternos = str(row['codigosAlternos']) if row.get('codigosAlternos') is not None else None,
            activo = bool(row['activo']) if row.get('activo') is not None else None,
            prov = str(row['prov']) if row.get('prov') is not None else None,
            nombreProveedor = str(row['nombreProveedor']) if row.get('nombreProveedor') is not None else None,
            unidad = str(row['unidad']) if row.get('unidad') is not None else None,
            codigoSat = str(row['codigoSat']) if row.get('codigoSat') is not None else None,
            nomCodSat = str(row['nomCodSat']) if row.get('nomCodSat') is not None else None,
            unidadSat = str(row['unidadSat']) if row.get('unidadSat') is not None else None,
            nomUniSat = str(row['nomUniSat']) if row.get('nomUniSat') is not None else None
        )

        product_list.append(product_object)
    return product_list

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
        # data_frame.columns = data_frame.columns.str.lower()

        # Obtener códigos de productos del DataFrame
        codigos_productos = data_frame['codigo'].tolist()

        # Filtrar productos existentes en la base de datos por sus códigos
        productos_existentes = Producto.objects.filter(codigo__in=codigos_productos)

        phase1_time = time.time() - start_time
        print(f"Fase 1: {phase1_time} segundos")

        # Actualizar los productos existentes con los nuevos valores del DataFrame
        for producto_existente in productos_existentes:
            row = data_frame[data_frame['codigo'] == producto_existente.codigo].iloc[0]

            # Validar el tipo de dato antes de la asignación
            producto_existente.nombre = str(row['nombre']) if row.get('nombre') is not None else None
            producto_existente.marca = str(row['marca']) if row.get('marca') is not None else None
            producto_existente.linea = str(row['linea']) if row.get('linea') is not None else None
            producto_existente.sublinea = str(row['sublinea']) if row.get('sublinea') is not None else None
            producto_existente.departamento = str(row['departamento']) if row.get('departamento') is not None else None
            producto_existente.costo = Decimal(str(row['costo'])) if row.get('costo') is not None else None
            producto_existente.precio1 = Decimal(str(row['precio1'])) if row.get('precio1') is not None else None
            producto_existente.ptje1 = int(row['ptje1']) if row.get('ptje1') is not None else None
            producto_existente.ptjeReal = int(row['ptjeReal']) if row.get('ptjeReal') is not None else None
            producto_existente.precioCalculado = Decimal(str(row['precioCalculado'])) if row.get('precioCalculado') is not None else None
            producto_existente.maximo = int(row['maximo']) if row.get('maximo') is not None else None
            producto_existente.minimo = int(row['minimo']) if row.get('minimo') is not None else None
            producto_existente.estatus = int(row['estatus']) if row.get('estatus') is not None else None
            producto_existente.nombreStatus = str(row['nombreStatus']) if row.get('nombreStatus') is not None else None
            producto_existente.tipoProd = int(row['tipoProd']) if row.get('tipoProd') is not None else None
            producto_existente.tipoProdDesc = str(row['tipoProdDesc']) if row.get('tipoProdDesc') is not None else None
            producto_existente.codigosAlternos = str(row['codigosAlternos']) if row.get('codigosAlternos') is not None else None
            producto_existente.activo = bool(row['activo']) if row.get('activo') is not None else None
            producto_existente.prov = str(row['prov']) if row.get('prov') is not None else None
            producto_existente.nombreProveedor = str(row['nombreProveedor']) if row.get('nombreProveedor') is not None else None
            producto_existente.unidad = str(row['unidad']) if row.get('unidad') is not None else None
            producto_existente.codigoSat = str(row['codigoSat']) if row.get('codigoSat') is not None else None
            producto_existente.nomCodSat = str(row['nomCodSat']) if row.get('nomCodSat') is not None else None
            producto_existente.unidadSat = str(row['unidadSat']) if row.get('unidadSat') is not None else None
            producto_existente.nomUniSat = str(row['nomUniSat']) if row.get('nomUniSat') is not None else None


        phase2_time = time.time() - start_time
        print(f"Fase 2: {phase2_time} segundos")

        # Separate new and existing elements
        existing_codigos = Producto.objects.values_list('codigo', flat=True)
        
        ## If is empty you don't need to do de comparation
        if bool(existing_codigos):
            nuevos_productos = [p for p in codigos_productos if p not in existing_codigos]
        else:
            nuevos_productos = create_new_products_from_csv(codigos_productos, data_frame)

        # Check if there are new elements and show how many new elements are new and how many are loaded
        new_elements_count = len(nuevos_productos)
        existing_elements_to_update_count = len(productos_existentes) - new_elements_count if len(productos_existentes) >= new_elements_count else 0
        messages.info(request, f'Se encontraron {new_elements_count} elementos nuevos y se actualizaran {existing_elements_to_update_count} elementos existentes.')

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
