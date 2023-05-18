from django.urls import include, path
from . import views

app_name = "product"
urlpatterns = [
    path("load/", views.load_data, name="load"),
    path("", views.index, name="index"),
    path('api-auth/', include('rest_framework.urls')),
]
