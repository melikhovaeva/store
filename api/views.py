from django.db.models import Q
from django.utils.dateparse import parse_duration
from rest_framework import generics, status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from products.models import Product, Basket
from users.models import User
from products.serializers import ProductSerializer, BasketSerializer
from  users.serializers import UserSerializer
from api.pagination import LargeResultsSetPagination


class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter,  OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['category', 'price']
    
    @action(detail=True, methods=['get'], url_path='product')
    def filter_products(self, request):
           queryset = Product.objects.filter(
               Q(price__gte=1000) & ~Q(price__gte=2400) | Q(category='2')
           )
           serializer = self.get_serializer(queryset, many=True)
           return Response(serializer.data)
       
    @action(detail=False, methods=['post', 'get'])
    def add_product(self, request):
        if request.method == 'POST':
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        elif request.method == 'GET':
            return Response("GET для add_product")
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    pagination_class = LargeResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['username', 'is_staff']
    
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