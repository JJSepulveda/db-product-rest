from django.urls import include, path
from rest_framework import routers

from . import views

app_name = views.APP_NAME
urlpatterns = [
    path(
        "api/products/",
        views.ProductListCreate.as_view(),
        name=views.ProductListCreate.name,
    ),
    path(
        "api/products/<int:pk>/",
        views.ProductRetrieveUpdateDestroy.as_view(),
        name=views.ProductRetrieveUpdateDestroy.name,
    ),
    path(
        "api/products/c/<str:codigo>/",
        views.ProductRetrieveUpdateDestroyCode.as_view(),
        name=views.ProductRetrieveUpdateDestroy.name,
    ),
    path(
        "api-key/",
        views.GetApiKey.as_view(),
        name=views.GetApiKey.name,
    ),
    path("", views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
