from django.urls import include, path, re_path
from rest_framework import routers

from . import views

app_name = "product_api_v2"
urlpatterns = [
    path(
        "products/",
        views.ProductListCreateV2.as_view(),
        name="product_list",
    ),
    path(
        "products/<int:pk>/",
        views.ProductRetrieveUpdateDestroyV2.as_view(),
        name="product_detail_v2",
    ),
    re_path(
        r"^products/c/(?P<codigo>.+)/$",
        views.ProductRetrieveUpdateDestroyCodeV2.as_view(),
        name="product_detail_code_v2",
    ),
    path(
        "products/bulk/", 
        views.ProductStockView.as_view(), 
        name="bulk_p"
    ),
]
