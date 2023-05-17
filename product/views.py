from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, "product/index.html")

def load_data(request):
    return render(request, "product/load_data.html")