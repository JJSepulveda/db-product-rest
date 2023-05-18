from django.urls import include, path
from rest_framework import routers

from . import views

app_name = views.APP_NAME
urlpatterns = [
    path(
        "products/",
        views.ProductListCreate.as_view(),
        name=views.ProductListCreate.name,
    ),
    path(
        "products/<int:pk>/",
        views.ProductRetrieveUpdateDestroy.as_view(),
        name=views.ProductRetrieveUpdateDestroy.name,
    ),
    path("", views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
