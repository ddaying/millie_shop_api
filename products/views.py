from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import ProductFilter
from .models import Product, Category, Coupon
from .serializers import ProductSerializer, CategorySerializer, CouponSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = ProductFilter
    filterset_fields = ['category']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category:
            return Product.objects.filter(category_id=category)

        return Product.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        coupon_code = self.request.query_params.get('coupon_code')
        if coupon_code:
            context['coupon_code'] = coupon_code

        return context
