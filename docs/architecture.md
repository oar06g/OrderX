```
OrderX/
│
├── gateway/                ← API Gateway (FastAPI/Express)
│   ├── Dockerfile
│   └── src/...
│
├── services/
│   ├── user-service/
│   │   ├── Dockerfile
│   │   └── src/...
│   ├── product-service/
│   │   ├── Dockerfile
│   │   └── src/...
│   ├── order-service/
│   │   ├── Dockerfile
│   │   └── src/...
│   └── payment-service/
│       ├── Dockerfile
│       └── src/...
│
├── infra/
│   ├── docker-compose.yml   ← يشغل كل الخدمات
│   ├── rabbitmq/
│   └── db/
│
├── scripts/
│   ├── build_all.sh
│   ├── start.sh
│   └── stop.sh
│
└── README.md
```


```
User
  |
  | 1) POST /order
  v
API Gateway
  |
  |--> Forward to Order Service
  v
Order Service
  | 
  |--(2) Create order in DB (status = "pending")
  |
  |--(3) Publish Event: "order.created"
  v
==================== Kafka ====================
  |                     |
  |                     |-- Payment Service Subscribes
  |                     |
================================================
                          |
                          |--(4) Payment Service receives "order.created"
                          v
                    Payment Service
                          |
                          |-- Simulate payment
                          |-- Publish Event: "payment.success"
                          v
==================== Kafka ====================
  |                     |
  |                     |-- Order Service Subscribes
  |                     |
================================================
  |
  |--(5) Order Service receives "payment.success"
  |-- Update order in DB (status = "paid")
  |-- Publish Event: "order.completed"
  v
==================== Kafka ====================
  |                     |
  |                     |-- Notification Service Subscribes
  |                     |
================================================
                          |
                          |--(6) Notification Service receives "order.completed"
                          |-- Send email/notification (simulate)
                          v
                    Notification Service

------------------------------------------------

Meanwhile…

User
  |
  |--(7) GET /order/status/{id}
  v
API Gateway
  |
  |--> Forward to Order Service
  v
Order Service
  |
  |-- Returns status = "paid"
  v
API Gateway
  |
  |-- Response to User → "Order Completed Successfully"
  v
User
```