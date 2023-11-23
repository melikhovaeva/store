from django.urls import path, include

from rest_framework import routers

from api.views import ProductModelViewSet, UserViewSet, BasketModelViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'users', UserViewSet)
router.register(r'baskets', BasketModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]