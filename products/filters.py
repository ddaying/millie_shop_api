from django_filters import rest_framework as filters

from products.models import Product, Category


class ProductFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category', method='filter_category')

    class Meta:
        model = Product
        fields = ['category']

    def filter_category(self, queryset, name, value):
        try:
            # filter 를 커스터마이징 하여 카테고리가 존재하지 않는 경우 빈 배열을 반환하도록 한다.
            category_id = int(value)
            if Category.objects.filter(id=category_id).exists():
                return queryset.filter(category_id=category_id)
            else:
                return Product.objects.none()
        except ValueError:
            return Product.objects.none()
