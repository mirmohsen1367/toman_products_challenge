from django.urls import path, include
from rest_framework import routers
from api.views.shop_views import ProductViewSet

product_router = routers.DefaultRouter()
product_router.register('', ProductViewSet)

urlpatterns = [
    path('', include(product_router.urls)),
]