from django.db.utils import IntegrityError
from django.shortcuts import render
from django.contrib import messages

import pandas as pd
import numpy as np
from decimal import Decimal, InvalidOperation
import time

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Producto
import logging
# Create your views here.


@login_required
def index(request):
    return redirect('product:load_v3')
    # return render(request, "product/index.html")

## This function is deprecated
@login_required
def load_data(request):
    """ DEPRECATED """
    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo = request.FILES['archivo_csv']

        # Check if the uploaded file has a CSV extension
        if not archivo.name.endswith('.csv'):
            messages.warning(request, 'El archivo debe ser un archivo CSV.')
            return render(request, "product/load_data.html")

        # If pandas can't load it, also sen the same error
        try:
            data_frame = pd.read_csv(archivo, na_values=['NaN', 'N/A', '', 'nan'])
        except Exception:
            messages.warning(request, 'El archivo debe ser un archivo CSV.')
            return render(request, "product/load_data.html")
        
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
                        "existencia": row.get('existencia', None),
                    }
                )
            except IntegrityError:
                print("Error al insertar el producto: ", row['codigo'])
                pass
        
        messages.success(
            request, "Se actualizo correctamente la información del producto "
        )

    return render(request, "product/load_data.html")

def try_convert(row, column, data_type):
    """
    Intenta convertir el valor de la columna al tipo de datos especificado.
    Si hay una excepción, se devuelve None.
    """
    try:
        value = row[column]
        return data_type(str(value)) if value is not None else None
    except (ValueError, TypeError, InvalidOperation, Exception):
        return None
    
def get_stock(stock):
    """ Retorna un valor positivo"""
    # Si no existe el valor de stock entonces manda 0
    value = stock if stock else 0
    # Si el valor de stock es negativo, conviertelo a 0
    existencia = value if value >= 0 else 0
    return existencia

def get_stocks(row):
    existenciaPiso = get_stock(try_convert(row, "existenciaPiso", int))
    existenciaProd = get_stock(try_convert(row, "existenciaProd", int))
    existenciaTubos = get_stock(try_convert(row, "existenciaTubos", int))
    existenciaTanques = get_stock(try_convert(row, "existenciaTanques", int))
    existenciaDistr = get_stock(try_convert(row, "existenciaDistr", int))
    existenciaMakita = get_stock(try_convert(row, "existenciaMakita", int))
    existenciaStaRosa = get_stock(try_convert(row, "existenciaStaRosa", int))
    existenciaTotal = get_stock(try_convert(row, "existenciaTotal", int))
    
    results = {
        "existenciaPiso": existenciaPiso,
        "existenciaProd": existenciaProd,
        "existenciaTubos": existenciaTubos,
        "existenciaTanques": existenciaTanques,
        "existenciaDistr": existenciaDistr,
        "existenciaMakita": existenciaMakita,
        "existenciaStaRosa": existenciaStaRosa,
        "existenciaTotal": existenciaTotal,
    }
    
    return results

def create_new_products_from_csv(products_code, data_frame):
    # Crear los productos existentes con los nuevos valores del DataFrame
    product_list = []
    for code in products_code:
        codigo_producto_typed = type(data_frame['codigo'].iloc[0])(code)
        row = data_frame[data_frame['codigo'] == codigo_producto_typed].iloc[0]
        # row = data_frame[data_frame['codigo'] == code].iloc[0]
        # Validar el tipo de dato antes de la asignación
        try:
            stock = try_convert(row, 'existencia', int)
            ## Get only one stosk for the version 1 of this function
            existencia = get_stock(stock)
            # Get the all stocks
            stocks = get_stocks(row)
            product_object = Producto(
                codigo=code,
                nombre=try_convert(row, 'nombre', str),
                marca=try_convert(row, 'marca', str),
                linea=try_convert(row, 'linea', str),
                sublinea=try_convert(row, 'sublinea', str),
                departamento=try_convert(row, 'departamento', str),
                costo=try_convert(row, 'costo', Decimal),
                precio1=try_convert(row, 'precio1', Decimal),
                ptje1=try_convert(row, 'ptje1', Decimal),
                ptjeReal=try_convert(row, 'ptjeReal', Decimal),
                precioCalculado=try_convert(row, 'precioCalculado', Decimal),
                maximo=try_convert(row, 'maximo', int),
                minimo=try_convert(row, 'minimo', int),
                estatus=try_convert(row, 'estatus', int),
                nombreStatus=try_convert(row, 'nombreStatus', str),
                tipoProd=try_convert(row, 'tipoProd', int),
                tipoProdDesc=try_convert(row, 'tipoProdDesc', str),
                codigosAlternos=try_convert(row, 'codigosAlternos', str),
                activo=try_convert(row, 'activo', bool),
                prov=try_convert(row, 'prov', str),
                nombreProveedor=try_convert(row, 'nombreProveedor', str),
                unidad=try_convert(row, 'unidad', str),
                codigoSat=try_convert(row, 'codigoSat', str),
                nomCodSat=try_convert(row, 'nomCodSat', str),
                unidadSat=try_convert(row, 'unidadSat', str),
                nomUniSat=try_convert(row, 'nomUniSat', str),
                existencia=existencia,
                existenciaPiso=stocks['existenciaPiso'],
                existenciaProd=stocks['existenciaProd'],
                existenciaTubos=stocks['existenciaTubos'],
                existenciaTanques=stocks['existenciaTanques'],
                existenciaDistr=stocks['existenciaDistr'],
                existenciaMakita=stocks['existenciaMakita'],
                existenciaStaRosa=stocks['existenciaStaRosa'],
                existenciaTotal=stocks['existenciaTotal'],
            )
        except Exception:
            continue

        product_list.append(product_object)
    return product_list

def update_products(codigos_productos, data_frame):
    """ Retorna una lista de los productos que existen en la base de datos con los nuevos datos actualizados """
    productos_existentes = Producto.objects.filter(codigo__in=codigos_productos)
    # Actualizar los productos existentes con los nuevos valores del DataFrame
    for producto_existente in productos_existentes:
        codigo_producto = producto_existente.codigo
        codigo_producto_typed = type(data_frame['codigo'].iloc[0])(codigo_producto)
        row = data_frame[data_frame['codigo'] == codigo_producto_typed].iloc[0]
        stock = try_convert(row, 'existencia', int)
        existencia = get_stock(stock)
        stocks = get_stocks(row)
        
        # Validar el tipo de dato antes de la asignación
        producto_existente.nombre=try_convert(row, 'nombre', str)
        producto_existente.marca=try_convert(row, 'marca', str)
        producto_existente.linea=try_convert(row, 'linea', str)
        producto_existente.sublinea=try_convert(row, 'sublinea', str)
        producto_existente.departamento=try_convert(row, 'departamento', str)
        producto_existente.costo=try_convert(row, 'costo', Decimal)
        producto_existente.precio1=try_convert(row, 'precio1', Decimal)
        producto_existente.ptje1=try_convert(row, 'ptje1', Decimal)
        producto_existente.ptjeReal=try_convert(row, 'ptjeReal', Decimal)
        producto_existente.precioCalculado=try_convert(row, 'precioCalculado', Decimal)
        producto_existente.maximo=try_convert(row, 'maximo', int)
        producto_existente.minimo=try_convert(row, 'minimo', int)
        producto_existente.estatus=try_convert(row, 'estatus', int)
        producto_existente.nombreStatus=try_convert(row, 'nombreStatus', str)
        producto_existente.tipoProd=try_convert(row, 'tipoProd', int)
        producto_existente.tipoProdDesc=try_convert(row, 'tipoProdDesc', str)
        producto_existente.codigosAlternos=try_convert(row, 'codigosAlternos', str)
        producto_existente.activo=try_convert(row, 'activo', bool)
        producto_existente.prov=try_convert(row, 'prov', str)
        producto_existente.nombreProveedor=try_convert(row, 'nombreProveedor', str)
        producto_existente.unidad=try_convert(row, 'unidad', str)
        producto_existente.codigoSat=try_convert(row, 'codigoSat', str)
        producto_existente.nomCodSat=try_convert(row, 'nomCodSat', str)
        producto_existente.unidadSat=try_convert(row, 'unidadSat', str)
        producto_existente.nomUniSat=try_convert(row, 'nomUniSat', str)
        producto_existente.existencia=existencia
        producto_existente.existenciaPiso=stocks['existenciaPiso']
        producto_existente.existenciaProd=stocks['existenciaProd']
        producto_existente.existenciaTubos=stocks['existenciaTubos']
        producto_existente.existenciaTanques=stocks['existenciaTanques']
        producto_existente.existenciaDistr=stocks['existenciaDistr']
        producto_existente.existenciaMakita=stocks['existenciaMakita']
        producto_existente.existenciaStaRosa=stocks['existenciaStaRosa']
        producto_existente.existenciaTotal=stocks['existenciaTotal']

    return productos_existentes

@login_required
def load_data_v2(request):
    start_time = time.time()
    context = {
        "count": Producto.objects.count()
    }

    if request.method == 'POST' and request.FILES['archivo_csv']:
        archivo = request.FILES['archivo_csv']

        # Verificar si el archivo subido tiene una extensión CSV
        if not archivo.name.endswith('.csv'):
            messages.warning(request, 'El archivo debe ser un archivo CSV.')
            return render(request, "product/load_data.html")

        # import pdb; pdb.set_trace()
        # Cargar datos del archivo CSV
        data_frame = pd.read_csv(archivo, na_values=['NaN', 'N/A', '', 'nan'])
        # data_frame.columns = data_frame.columns.str.lower()

        phase1_time = time.time() - start_time
        logging.info(f"Fase 1: {phase1_time} segundos")

        # Obtener códigos de productos del DataFrame que se usaran para cargar los productos existentes y actualizarlos
        codigos_productos = data_frame['codigo'].tolist()
        productos_existentes = update_products(codigos_productos, data_frame)

        phase2_time = time.time() - start_time
        logging.info(f"Fase 2: {phase2_time} segundos")

        # Separate new and existing elements
        existing_codigos = Producto.objects.values_list('codigo', flat=True)
        
        ## If is empty you don't need to do de comparation
        if bool(existing_codigos):
            codigos_de_productos_nuevos = [p for p in codigos_productos if p not in existing_codigos]
            nuevos_productos = create_new_products_from_csv(codigos_de_productos_nuevos, data_frame)
        else:
            nuevos_productos = create_new_products_from_csv(codigos_productos, data_frame)

        # Check if there are new elements and show how many new elements are new and how many are loaded
        new_elements_count = len(nuevos_productos)
        messages.info(request, f'Se encontraron {new_elements_count} elementos nuevos y se actualizaran {len(productos_existentes)} elementos existentes.')

        phase3_time = time.time() - start_time
        logging.info(f"Fase 3: {phase3_time} segundos")

        # Make bulk update for existing elements
        if productos_existentes:
            try:
                Producto.objects.bulk_update(productos_existentes, fields=[
                    "nombre", "marca", "linea", "sublinea", "departamento",
                    "costo", "precio1", "ptje1", "ptjeReal", "precioCalculado",
                    "maximo", "minimo", "estatus", "nombreStatus", "tipoProd",
                    "tipoProdDesc", "codigosAlternos", "activo", "prov",
                    "nombreProveedor", "unidad", "codigoSat", "nomCodSat",
                    "unidadSat", "nomUniSat", "existencia", "existenciaPiso", "existenciaProd", 
                    "existenciaTubos", "existenciaTanques", "existenciaDistr", "existenciaMakita", 
                    "existenciaStaRosa", "existenciaTotal"
                ], batch_size=1000)
            except IntegrityError:
                logging.error("Error al actualizar los productos:")
                logging.error(e)
                messages.error(request, "Hubo un error al actualizar los productos.")
            else:
                messages.success(request, "Se actualizó correctamente la información de los productos.")
        
        phase4_time = time.time() - start_time
        logging.info(f"Fase 4: {phase4_time} segundos")

        # Make bulk create for new elements
        if nuevos_productos:
            try:
                for i in range(0, len(nuevos_productos), 1000):
                    Producto.objects.bulk_create(nuevos_productos[i:i+1000], batch_size=1000, ignore_conflicts=True)
                    logging.debug(f"batch: {i}")
            except IntegrityError as e:
                logging.error("Error al crear los productos: ")
                logging.error(e)
                messages.error(request, "Hubo un error al crear nuevos productos.")
            else:
                messages.success(request, "Se crearon los nuevo elementos correctamente.")
            
        
        phase5_time = time.time() - start_time
        logging.info(f"Fase 5: {phase5_time} segundos")

    return render(request, "product/load_data.html", context=context)


@login_required
def load_data_v3(request):
    context = {
        "count": Producto.objects.count()
    }
    return render(request, "product/load_data_api.html", context=context)



from django.http import JsonResponse

@login_required
def load_data_api(request):
    start_time = time.time()
    response_data = {}  # Inicializar el diccionario para almacenar los datos de respuesta
    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo = request.FILES['archivo_csv']

        # Verificar si el archivo subido tiene una extensión CSV
        if not archivo.name.endswith('.csv'):
            response_data['error'] = 'El archivo debe ser un archivo CSV.'
            return JsonResponse(response_data, status=400)

        # import pdb; pdb.set_trace()
        # Cargar datos del archivo CSV
        data_frame = pd.read_csv(archivo, na_values=['NaN', 'N/A', '', 'nan'])
        # data_frame.columns = data_frame.columns.str.lower()

        phase1_time = time.time() - start_time
        logging.info(f"Fase 1: {phase1_time} segundos")

        # Obtener códigos de productos del DataFrame que se usaran para cargar los productos existentes y actualizarlos
        codigos_productos = data_frame['codigo'].tolist()
        productos_existentes = update_products(codigos_productos, data_frame)

        phase2_time = time.time() - start_time
        logging.info(f"Fase 2: {phase2_time} segundos")

        # Separate new and existing elements
        existing_codigos = Producto.objects.values_list('codigo', flat=True)
        
        ## If is empty you don't need to do de comparation
        if bool(existing_codigos):
            codigos_de_productos_nuevos = [p for p in codigos_productos if p not in existing_codigos]
            nuevos_productos = create_new_products_from_csv(codigos_de_productos_nuevos, data_frame)
        else:
            nuevos_productos = create_new_products_from_csv(codigos_productos, data_frame)

        # Check if there are new elements and show how many new elements are new and how many are loaded
        new_elements_count = len(nuevos_productos)
        logging.info(f'Se encontraron {new_elements_count} elementos nuevos y se actualizaran {len(productos_existentes)} elementos existentes.')

        phase3_time = time.time() - start_time
        logging.info(f"Fase 3: {phase3_time} segundos")

        # Make bulk update for existing elements
        if productos_existentes:
            try:
                Producto.objects.bulk_update(productos_existentes, fields=[
                    "nombre", "marca", "linea", "sublinea", "departamento",
                    "costo", "precio1", "ptje1", "ptjeReal", "precioCalculado",
                    "maximo", "minimo", "estatus", "nombreStatus", "tipoProd",
                    "tipoProdDesc", "codigosAlternos", "activo", "prov",
                    "nombreProveedor", "unidad", "codigoSat", "nomCodSat",
                    "unidadSat", "nomUniSat", "existencia", "existenciaPiso", "existenciaProd", 
                    "existenciaTubos", "existenciaTanques", "existenciaDistr", "existenciaMakita", 
                    "existenciaStaRosa", "existenciaTotal"
                ], batch_size=1000)
            except IntegrityError:
                logging.error("Error al actualizar los productos:")
                logging.error(e)
                response_data['message'] = 'Hubo un error al actualizar los productos.'
                response_data['update'] = 'error'
                return JsonResponse(response_data, status=500)
            else:
                response_data['update'] = 'Se actualizó correctamente la información de los productos.'
        
        phase4_time = time.time() - start_time
        logging.info(f"Fase 4: {phase4_time} segundos")

        # Make bulk create for new elements
        if nuevos_productos:
            try:
                for i in range(0, len(nuevos_productos), 1000):
                    Producto.objects.bulk_create(nuevos_productos[i:i+1000], batch_size=1000, ignore_conflicts=True)
                    logging.debug(f"batch: {i}")
            except IntegrityError as e:
                logging.error("Error al crear los productos: ")
                logging.error(e)
                response_data['message'] = 'Hubo un error al crear nuevos productos.'
                response_data['create'] = 'error'
                return JsonResponse(response_data, status=500)
            else:
                response_data['create'] = 'Se crearon los nuevo elementos correctamente.'

        response_data['message'] = f'Se crearon {new_elements_count} elementos nuevos y se actualizaron {len(productos_existentes)} elementos.'
            
        phase5_time = time.time() - start_time
        logging.info(f"Fase 5: {phase5_time} segundos")
    
    return JsonResponse(response_data)
