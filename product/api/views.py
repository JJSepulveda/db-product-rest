from django.urls import reverse, reverse_lazy
from rest_framework import generics
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from product.models import Producto

from .serializers import ProductoSerializer

APP_NAME = "product_api"

# ViewSets define the view behavior.
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Producto.objects.all()
#     serializer_class = ProductoSerializer


# class WatchDetailAV(APIView):
#     permission_classes = [permissions.IsAdminOrReadOnly]
#     throttle_classes = [AnonRateThrottle]

#     def get(self, request, pk):
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = serializers.WatchListSerializer(movie)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         movie = WatchList.objects.get(pk=pk)
#         serializer = serializers.WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         movie = WatchList.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    name = "product-list"


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    name = "product-detail"


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        product_url = reverse(APP_NAME + ":" + ProductListCreate.name)
        absolute_product_url = request.build_absolute_uri(product_url)
        return Response(
            {
                "products": absolute_product_url,
            }
        )
