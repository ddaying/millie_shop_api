# 쇼핑몰 상품 관리 API

## Environment
- Python
- Django
- Mysql
- Docker

## Run
- mysql 컨테이너 실행
```
docker-compose up
```
- django 실행
```
python manage.py runserver
```

## Project Structure
```
$ tree -I venv

.
├── README.md
├── docker-compose.yml
├── fixtures
│   └── sample.json
├── manage.py
├── millie_shop_api
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── settings.cpython-310.pyc
│   │   ├── urls.cpython-310.pyc
│   │   └── wsgi.cpython-310.pyc
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── products
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── admin.cpython-310.pyc
│   │   ├── apps.cpython-310.pyc
│   │   ├── models.cpython-310.pyc
│   │   ├── serializers.cpython-310.pyc
│   │   └── views.cpython-310.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_category_created_at_alter_category_updated_at_and_more.py
│   │   ├── 0003_product_coupons.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-310.pyc
│   │       ├── 0002_alter_category_created_at_alter_category_updated_at_and_more.cpython-310.pyc
│   │       ├── 0003_product_coupons.cpython-310.pyc
│   │       └── __init__.cpython-310.pyc
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── requirements.txt
└── templates
```

## DDL
```
-- 카테고리
CREATE TABLE `products_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

-- 상품
CREATE TABLE `products_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `price` int unsigned NOT NULL,
  `discount_rate` decimal(5,2) NOT NULL,
  `coupon_applicable` tinyint(1) NOT NULL,
  `category_id` bigint NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_product_category_id_9b594869_fk_products_category_id` (`category_id`),
  CONSTRAINT `products_product_category_id_9b594869_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`),
  CONSTRAINT `products_product_chk_1` CHECK ((`price` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
;

-- 쿠폰
CREATE TABLE `products_coupon` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `discount_rate` decimal(5,2) NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

-- 상품별 사용한 쿠폰
CREATE TABLE `products_product_coupons` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `coupon_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `products_product_coupons_product_id_coupon_id_a2713097_uniq` (`product_id`,`coupon_id`),
  KEY `products_product_cou_coupon_id_dbc8bee2_fk_products_` (`coupon_id`),
  CONSTRAINT `products_product_cou_coupon_id_dbc8bee2_fk_products_` FOREIGN KEY (`coupon_id`) REFERENCES `products_coupon` (`id`),
  CONSTRAINT `products_product_cou_product_id_17ad83df_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
```

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