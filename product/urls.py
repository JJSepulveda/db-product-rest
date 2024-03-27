from django.urls import include, path
from . import views

app_name = "product"
urlpatterns = [
    path("load/", views.load_data, name="load"),
    path("load/v2/", views.load_data_v2, name="load_v2"),
    path("load/v3/", views.load_data_v3, name="load_v3"),
    path("load/api/v1/", views.load_data_api, name="load_api"),
    path("", views.index, name="index"),
    path('api-auth/', include('rest_framework.urls')),
]
