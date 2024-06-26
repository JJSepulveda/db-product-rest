from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, authentication, permissions
from rest_framework.response import Response
from rest_framework import filters
from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter, RangeFilter
from django_filters.rest_framework import FilterSet
from rest_framework_api_key.permissions import HasAPIKey

from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework.exceptions import PermissionDenied

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from product.models import Producto

from .serializers import (
    ProductoSerializer,
    ProductoSerializerV2,
    ProductoStockSerializer,
)

from urllib.parse import quote

import base64

APP_NAME = "product_api"


class ProductoFilter(FilterSet):
    precio = RangeFilter(field_name="precioCalculado")

    class Meta:
        model = Producto
        fields = ["precioCalculado"]


class PostHasAPIKey(HasAPIKey):
    """Only allow POST with API Key and allow GET, HEAD, OPTIONS without API Key"""

    def has_permission(self, request, view):
        if request.method == "POST":
            return super().has_permission(request, view)
        return True


class RetrieveUpdateDestroyAPIKey(HasAPIKey):
    """Only allow GET, HEAD, OPTIONS without API Key, deny DELETE and allow POST, PUT, PATCH with API Key"""

    def has_permission(self, request, view):
        if (
            request.method == "POST"
            or request.method == "PUT"
            or request.method == "PATCH"
        ):
            return super().has_permission(request, view)

        if request.method == "DELETE":
            raise PermissionDenied("You don't have permission to DELETE")

        # GET, HEAD, OPTIONS
        return True


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    name = "product-list"
    filterset_fields = ("nombre",)
    search_fields = ("nombre", "codigo")
    ordering_fields = ("nombre", "created_at")
    permission_classes = [PostHasAPIKey]
    filterset_class = ProductoFilter

    @swagger_auto_schema(tags=["Products"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Products"],
        manual_parameters=[
            openapi.Parameter(
                name="X-Api-Key",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="API key for authorization",
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=ProductoSerializer(many=True),
            ),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    name = "product-detail"
    permission_classes = [RetrieveUpdateDestroyAPIKey]

    @swagger_auto_schema(
        tags=["Products"], operation_description="Retrieve a product by id"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductRetrieveUpdateDestroyCode(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    name = "product-detail-2"
    lookup_field = "codigo"
    permission_classes = [RetrieveUpdateDestroyAPIKey]

    @swagger_auto_schema(tags=["Products"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ApiRoot(generics.GenericAPIView):
    name = "api-root"
    pagination_class = None
    filter_backends = None
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["Info"],
        operation_summary="API Root",
        operation_description="This is the API root view.",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "products": openapi.Schema(type=openapi.TYPE_STRING),
                        "show-api-key": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    def get(self, request, *args, **kwargs):
        product_url = reverse(APP_NAME + ":" + ProductListCreate.name)
        absolute_product_url = request.build_absolute_uri(product_url)
        api_key_url = reverse(APP_NAME + ":" + GetApiKey.name)
        absolute_api_key_url = request.build_absolute_uri(api_key_url)
        return Response(
            {
                "products": absolute_product_url,
                "show-api-key": absolute_api_key_url,
            }
        )


class GetApiKey(generics.GenericAPIView):
    name = "show-api-key"
    pagination_class = None
    filter_backends = None
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        tags=["Info"],
        operation_summary="Get API Key",
        operation_description="This endpoint returns the API key for development purposes.",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "api-key": openapi.Schema(type=openapi.TYPE_STRING),
                        "detail": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    def get(self, request, *args, **kwargs):
        api_key = "yIZKLxfi.aN0B7KGvv33Jrdhg22ZmYp6BLpdOka6D"
        return Response(
            {
                "api-key": api_key,
                "detail": "Here is your API Key for development purposes only. will be removed in production.",
            }
        )


## PRODUCRT APIS VERSION 2
class ProductListCreateV2(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializerV2
    name = "product-list"
    filterset_fields = ("nombre",)
    search_fields = ("nombre", "codigo")
    ordering_fields = ("nombre", "created_at")
    filterset_class = ProductoFilter

    @swagger_auto_schema(tags=["Products"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Products"],
        manual_parameters=[
            openapi.Parameter(
                name="X-Api-Key",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="API key for authorization",
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=ProductoSerializerV2(many=True),
            ),
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductRetrieveUpdateDestroyV2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializerV2
    name = "product_detail_v2"
    permission_classes = [RetrieveUpdateDestroyAPIKey]

    @swagger_auto_schema(
        tags=["Products"], operation_description="Retrieve a product by id"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductRetrieveUpdateDestroyCodeV2(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializerV2
    name = "product_detail_v2"
    lookup_field = "codigo"
    permission_classes = [RetrieveUpdateDestroyAPIKey]

    @swagger_auto_schema(tags=["Products"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Products"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProductStockView(APIView):
    def get(self, request, *args, **kwargs):
        ids = request.query_params.get("ids")

        if not ids:
            return Response({"error": "No se proporcionaron IDs"}, status=400)
        try:
            ids_list = [
                base64.b64decode(codigo.encode("utf-8")).decode("utf-8") for codigo in ids.split(",")
            ]
        except (ValueError, UnicodeDecodeError) as e:
            return Response({"error": "Invalid ID format"}, status=400)

        elementos = Producto.objects.filter(codigo__in=ids_list)
        serializer = ProductoStockSerializer(elementos, many=True)
        return Response(serializer.data)
