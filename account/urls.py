from django.urls import include, path
from . import views

from django.contrib.auth.views import LoginView

app_name = "account"
urlpatterns = [
    # path("login/", LoginView.as_view(), name="login"), 
    # La vista anterior no es necearia si agregas: path('accounts/', include('django.contrib.auth.urls')), en el url pricipal
]
