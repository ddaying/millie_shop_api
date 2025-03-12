# 쇼핑몰 상품 관리 API

## 샘플 데이터 추가
```
python manage.py loaddata fixtures/sample.json
```

## API
### 1. 상품 목록 조회 및 카테고리별 조회
- 상품 목록 전체 조회
```
curl -X GET 'http://127.0.0.1:8000/api/products/' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1076  100  1076    0     0  44688      0 --:--:-- --:--:-- --:--:-- 51238
[
  {
    "id": 1,
    "name": "상품1",
    "description": "상품 설명 입니다.",
    "price": 10000,
    "category": {
      "id": 1,
      "name": "패션의류"
    },
    "discount_rate": "0.05",
    "coupon_applicable": true,
    "final_price": 9500,
    "coupons": [
      {
        "id": 1,
        "code": "DISCOUNT_10",
        "discount_rate": "0.10"
      },
      {
        "id": 2,
        "code": "DISCOUNT_20",
        "discount_rate": "0.20"
      }
    ],
    "applied_coupon": null
  },
  {
    "id": 2,
    "name": "상품2",
    "description": "상품 설명 입니다.",
    "price": 20000,
    "category": {
      "id": 2,
      "name": "디지털/가전"
    },
    "discount_rate": "0.15",
    "coupon_applicable": true,
    "final_price": 17000,
    "coupons": [
      {
        "id": 1,
        "code": "DISCOUNT_10",
        "discount_rate": "0.10"
      }
    ],
    "applied_coupon": null
  },
  {
    "id": 3,
    "name": "상품3",
    "description": "상품 설명 입니다.",
    "price": 1000,
    "category": {
      "id": 2,
      "name": "디지털/가전"
    },
    "discount_rate": "0.15",
    "coupon_applicable": false,
    "final_price": 850,
    "coupons": [],
    "applied_coupon": null
  },
  {
    "id": 4,
    "name": "상품4",
    "description": "상품 설명 입니다.",
    "price": 5000,
    "category": {
      "id": 2,
      "name": "디지털/가전"
    },
    "discount_rate": "0.00",
    "coupon_applicable": false,
    "final_price": 5000,
    "coupons": [],
    "applied_coupon": null
  }
]
```

- 특정 카테고리로 상품 목록을 조회 하는 경우
```
curl -X GET 'http://127.0.0.1:8000/api/products/?category=1' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   333  100   333    0     0  12115      0 --:--:-- --:--:-- --:--:-- 13875
[
  {
    "id": 1,
    "name": "상품1",
    "description": "상품 설명 입니다.",
    "price": 10000,
    "category": {
      "id": 1,
      "name": "패션의류"
    },
    "discount_rate": "0.05",
    "coupon_applicable": true,
    "final_price": 9500,
    "coupons": [
      {
        "id": 1,
        "code": "DISCOUNT_10",
        "discount_rate": "0.10"
      },
      {
        "id": 2,
        "code": "DISCOUNT_20",
        "discount_rate": "0.20"
      }
    ],
    "applied_coupon": null
  }
]
```

2. 상품 상세 정보 조회
```
curl -X GET 'http://127.0.0.1:8000/api/products/1/' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   331  100   331    0     0  12945      0 --:--:-- --:--:-- --:--:-- 15761
{
  "id": 1,
  "name": "상품1",
  "description": "상품 설명 입니다.",
  "price": 10000,
  "category": {
    "id": 1,
    "name": "패션의류"
  },
  "discount_rate": "0.05",
  "coupon_applicable": true,
  "final_price": 9500,
  "coupons": [
    {
      "id": 1,
      "code": "DISCOUNT_10",
      "discount_rate": "0.10"
    },
    {
      "id": 2,
      "code": "DISCOUNT_20",
      "discount_rate": "0.20"
    }
  ],
  "applied_coupon": null
}
```

3. 쿠폰 적용 상품 조회
> 적용된 쿠폰은 사용 가능한 쿠폰 목록 (coupons) 에서 제외 됩니다.
```
curl -X GET 'http://127.0.0.1:8000/api/products/1/?coupon_code=DISCOUNT_10' | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   326  100   326    0     0  12287      0 --:--:-- --:--:-- --:--:-- 14818
{
  "id": 1,
  "name": "상품1",
  "description": "상품 설명 입니다.",
  "price": 10000,
  "category": {
    "id": 1,
    "name": "패션의류"
  },
  "discount_rate": "0.05",
  "coupon_applicable": true,
  "final_price": 8550,
  "coupons": [
    {
      "id": 2,
      "code": "DISCOUNT_20",
      "discount_rate": "0.20"
    }
  ],
  "applied_coupon": {
    "id": 1,
    "code": "DISCOUNT_10",
    "discount_rate": "0.10"
  }
}
```