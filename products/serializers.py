from rest_framework import serializers
from .models import Category, Coupon, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_rate']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    final_price = serializers.SerializerMethodField()
    coupons = serializers.SerializerMethodField()
    applied_coupon = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'discount_rate', 'coupon_applicable', 'final_price',
                  'coupons', 'applied_coupon']

    def get_final_price(self, obj):
        """최종 가격 계산 (쿠폰 코드가 전달되면 해당 쿠폰 할인율을 적용)"""
        coupon_code = self.context.get('coupon_code')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                return obj.get_final_price(coupon)
            except Coupon.DoesNotExist:
                pass

        return obj.get_final_price()

    def get_coupons(self, obj):
        applied_coupon = self.get_applied_coupon(obj)
        available_coupons = obj.coupons.all()

        # 상품 조회시 쿠폰이 적용된 경우 (쿠폰 코드가 전달된 경우) 는 사용 가능 쿠폰 목록에서 제외 한다.
        if applied_coupon:
            available_coupons = available_coupons.exclude(id=applied_coupon["id"])

        return CouponSerializer(available_coupons, many=True).data

    def get_applied_coupon(self, obj):
        """적용된 쿠폰 정보를 반환"""
        coupon_code = self.context.get('coupon_code')

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                return CouponSerializer(coupon).data
            except Coupon.DoesNotExist:
                pass

        return None
