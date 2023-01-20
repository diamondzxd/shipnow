"""shipnow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from main import views as main


from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('admin/', admin.site.urls),

    #Main App
    #Index
    path('',main.Index),

    #Login
    path('login/', LoginView.as_view(), name='login'),
    #Addresses
    path('addaddress/',main.AddAddress),
    path('displayaddress/',main.DisplayAddress),
    path('updateaddress/<id>',main.UpdateAddress),
    path('deleteaddress/<id>',main.DeleteAddress),
    path('fetchaddress/',main.FetchAddress),

    #Products
    path('addproduct/',main.AddProduct),
    path('displayproduct/',main.DisplayProduct),
    path('updateproduct/<id>',main.UpdateProduct),
    path('deleteproduct/<id>',main.DeleteProduct),
    path('fetchproduct/',main.FetchProduct),

    #Orders
    path('addorder/',main.AddOrder),
    path('displayorder/',main.DisplayOrder),
    path('deleteorder/<id>',main.DeleteOrder),
    path('fetchorders/',main.FetchOrder),

    #Shipments
    path('createshipment/<oid>',main.CreateShipment),
    path('createshipment/<oid>/<courier>',main.CreateShipmentFinal),
    path('displayshipments/',main.DisplayShipments),
    path('displayshipments/<sid>',main.DisplayShipmentDetail),
    path('generateinvoice/<oid>',main.GenerateInvoice),
    path('labeltest/',main.LabelTesting),

    #Protected Media View
    path('cdn/<path:path>', main.protected_serve, name='protected_serve'),
    
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)