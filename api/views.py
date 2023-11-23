from django.db.models import Q
from django.utils.dateparse import parse_duration
from rest_framework import generics, status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from products.models import Product, Basket
from users.models import User
from products.serializers import ProductSerializer, BasketSerializer
from  users.serializers import UserSerializer
from api.pagination import LargeResultsSetPagination


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    @action(detail=False, methods=['get'])
    def filter_products(self, request):
        price_gt = self.request.query_params.get('price_gt')
        price_lt = self.request.query_params.get('price_lt')
        if price_gt is not None and price_lt is not None:
           queryset = Product.objects.filter(
               Q(price__gte=price_gt) & ~Q(price__gte=int(price_lt)-1) | Q(price=price_lt)
           )
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
        else:
            return self.list(request)
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = LargeResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
    
    @action(detail=False, methods=['get'])
    def filter_user(self, request):
        queryset = User.objects.filter(
            Q(username__startswith='s') & ~Q(username__startswith='r') | Q(username__startswith='a')
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class BasketModelViewSet(ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        queryset = super(BasketModelViewSet, self).get_queryset()
        return queryset.filter(user=self.request.user)