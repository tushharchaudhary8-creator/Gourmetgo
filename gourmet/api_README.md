# GourmetGo FastAPI

This directory contains the FastAPI application for GourmetGo. The API provides REST endpoints for mobile apps and external integrations.

## Running the API

```bash
cd gourmet
uvicorn api:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `GET /api/auth/users` - Get all users

### Restaurants
- `GET /api/restaurants` - List all restaurants
- `GET /api/restaurants/{id}` - Get restaurant details
- `POST /api/restaurants` - Create a restaurant

### Menu
- `GET /api/restaurants/{id}/menu` - Get restaurant menu
- `GET /api/menu/{id}` - Get menu item
- `POST /api/menu` - Create menu item

### Orders
- `GET /api/orders` - List orders (with user_id and role filters)
- `GET /api/orders/{id}` - Get order details
- `POST /api/orders` - Create an order
- `PUT /api/orders/{id}/status` - Update order status

### Payments
- `GET /api/payments/{order_id}` - Get payment details
- `POST /api/payments` - Process payment

### Coupons
- `GET /api/coupons` - List active coupons
- `POST /api/coupons/validate` - Validate a coupon code

### Ratings
- `GET /api/restaurants/{id}/ratings` - Get restaurant ratings
- `POST /api/ratings` - Create a rating

### Health
- `GET /api/health` - Health check endpoint

## Example Usage

```bash
# Start the server
uvicorn api:app --reload

# Get all restaurants
curl http://localhost:8000/api/restaurants

# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "pass123", "role": "customer"}'
```

