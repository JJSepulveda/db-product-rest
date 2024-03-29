"""
URL configuration for elarco project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from product.views import index

schema_view = get_schema_view(
    openapi.Info(
        title="El Arco API",
        default_version="1.0.0",
        description="API for El Arco",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="artjsc@outlook.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("product/", include("product.urls", namespace="product")),
    path(
        "api/v1/",
        include(
            [
                path("", include("product.api.urls", namespace="product_api")),
                path("swagger/schema/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-schema"),
            ]
        ),
    ),
    path(
        "api/v2/",
        include(
            [
                path("", include("product.api.urlsv2", namespace="product_api_v2")),
            ]
        ),
    ),
    path('accounts/', include('django.contrib.auth.urls')),
    # path("", include("account.urls", namespace="account")),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="product/robots.txt", content_type="text/plain"),
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
