from django.db import models


class AuditModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(AuditModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Coupon(AuditModel):
    code = models.CharField(max_length=50, unique=True)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="할인율 (예: 0.10은 10% 할인)")

    def __str__(self):
        return f"{self.code} ({self.discount_rate * 100:.0f}%)"


class Product(AuditModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="기본 단위: 원")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="할인율 (예: 0.10은 10% 할인)")
    coupon_applicable = models.BooleanField(default=True)

    def discounted_price(self):
        """할인율을 적용한 가격 반환"""
        return int(self.price * (1 - self.discount_rate))

    def final_price(self, coupon=None):
        """ 쿠폰이 있을 경우 최종 가격 계산 """
        discounted_price = self.discounted_price()
        if coupon and self.coupon_applicable:
            return discounted_price * (1 - coupon.discount_rate)
        return discounted_price

    def __str__(self):
        return self.name
