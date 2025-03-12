from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category, Coupon, Product
from django.urls import reverse


class CategoryAPITests(APITestCase):
    def setUp(self):
        # 테스트용 카테고리 생성
        self.category = Category.objects.create(name="패션의류")
        self.url = reverse('category-list')

    def test_category_list_success(self):
        # 카테고리 목록 조회 성공 테스트
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], '패션의류')


class CouponAPITests(APITestCase):
    def setUp(self):
        # 테스트용 쿠폰 생성
        self.coupon = Coupon.objects.create(code="DISCOUNT_10", discount_rate=0.10)
        self.url = reverse('coupon-list')

    def test_coupon_list_success(self):
        # 쿠폰 목록 조회 성공 테스트
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['code'], 'DISCOUNT_10')


class ProductAPITests(APITestCase):
    def setUp(self):
        # 테스트용 카테고리, 쿠폰, 상품 생성
        self.category = Category.objects.create(name="패션의류")
        self.coupon = Coupon.objects.create(code="DISCOUNT_10", discount_rate=0.10)
        self.product = Product.objects.create(
            name="상품1", description="상품 설명 입니다.", price=10000, category=self.category
        )
        self.product.coupons.add(self.coupon)  # 상품에 쿠폰 연결
        self.url = reverse('product-list')  # Product API 목록 URL

    def test_product_list_success(self):
        # 상품 목록 조회 성공 테스트
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], '상품1')

    def test_product_list_empty(self):
        # 잘못된 카테고리로 상품 목록 조회 실패 테스트
        url = self.url + "?category=9999"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_product_with_coupon_success(self):
        # 쿠폰 코드 전달 시 상품 최종 가격 조회
        url = self.url + f"?coupon_code=DISCOUNT_10"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['final_price'], 9000)

    def test_product_with_coupon_fail(self):
        # 잘못된 쿠폰 코드로 상품 조회
        url = self.url + f"?coupon_code=INVALID_CODE"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['final_price'], 10000)
