"""
FastAPI API for GourmetGo
Provides REST API endpoints for mobile app and external integrations
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gourmet.settings')
django.setup()

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from django.contrib.auth.models import User
from django.db.models import Q
from core.models import (
    Profile, Restaurant, Menu, Order, Payment, Coupon, Rating
)

app = FastAPI(title="GourmetGo API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Pydantic Models
# =========================

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str  # customer, restaurant, delivery


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    
    class Config:
        from_attributes = True


class RestaurantCreate(BaseModel):
    name: str
    location: str
    owner_id: int


class RestaurantResponse(BaseModel):
    id: int
    name: str
    location: str
    rating: float
    
    class Config:
        from_attributes = True


class MenuCreate(BaseModel):
    restaurant_id: int
    item_name: str
    description: str = ""
    price: int
    available: bool = True


class MenuResponse(BaseModel):
    id: int
    restaurant_id: int
    item_name: str
    description: str
    price: int
    available: bool
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    customer_id: int
    restaurant_id: int
    item_id: int
    quantity: int = 1


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    item_id: int
    quantity: int
    total_price: int
    status: str
    payment_status: bool
    created_at: str
    
    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    order_id: int
    amount: int


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: int
    transaction_id: Optional[str]
    success: bool
    paid_at: str
    
    class Config:
        from_attributes = True


class CouponValidate(BaseModel):
    code: str
    order_amount: int


class RatingCreate(BaseModel):
    order_id: int
    customer_id: int
    restaurant_id: int
    rating: int
    review: str = ""
    delivery_rating: Optional[int] = None
    delivery_review: str = ""


class RatingResponse(BaseModel):
    id: int
    order_id: int
    rating: int
    review: str
    
    class Config:
        from_attributes = True


# =========================
# Authentication Endpoints
# =========================

@app.post("/api/auth/register", response_model=UserResponse)
def register_user(user: UserCreate):
    if User.objects.filter(username=user.username).exists():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    django_user = User.objects.create_user(
        username=user.username,
        email=user.email,
        password=user.password
    )
    
    Profile.objects.create(user=django_user, role=user.role)
    
    return UserResponse(
        id=django_user.id,
        username=django_user.username,
        email=django_user.email,
        role=user.role
    )


@app.get("/api/auth/users", response_model=List[UserResponse])
def get_users():
    users = User.objects.all()
    profiles = Profile.objects.all()
    profile_map = {p.user_id: p.role for p in profiles}
    
    return [
        UserResponse(
            id=u.id,
            username=u.username,
            email=u.email,
            role=profile_map.get(u.id, 'customer')
        )
        for u in users
    ]


# =========================
# Restaurant Endpoints
# =========================

@app.get("/api/restaurants", response_model=List[RestaurantResponse])
def get_restaurants():
    restaurants = Restaurant.objects.all()
    return [
        RestaurantResponse(
            id=r.id,
            name=r.name,
            location=r.location,
            rating=r.rating
        )
        for r in restaurants
    ]


@app.get("/api/restaurants/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return RestaurantResponse(
            id=restaurant.id,
            name=restaurant.name,
            location=restaurant.location,
            rating=restaurant.rating
        )
    except Restaurant.DoesNotExist:
        raise HTTPException(status_code=404, detail="Restaurant not found")


@app.post("/api/restaurants", response_model=RestaurantResponse)
def create_restaurant(restaurant: RestaurantCreate):
    try:
        owner = User.objects.get(id=restaurant.owner_id)
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_restaurant = Restaurant.objects.create(
        owner=owner,
        name=restaurant.name,
        location=restaurant.location
    )
    
    return RestaurantResponse(
        id=new_restaurant.id,
        name=new_restaurant.name,
        location=new_restaurant.location,
        rating=new_restaurant.rating
    )


# =========================
# Menu Endpoints
# =========================

@app.get("/api/restaurants/{restaurant_id}/menu", response_model=List[MenuResponse])
def get_menu(restaurant_id: int):
    menu_items = Menu.objects.filter(restaurant_id=restaurant_id)
    return [
        MenuResponse(
            id=m.id,
            restaurant_id=m.restaurant_id,
            item_name=m.item_name,
            description=m.description,
            price=m.price,
            available=m.available
        )
        for m in menu_items
    ]


@app.get("/api/menu/{menu_id}", response_model=MenuResponse)
def get_menu_item(menu_id: int):
    try:
        menu = Menu.objects.get(id=menu_id)
        return MenuResponse(
            id=menu.id,
            restaurant_id=menu.restaurant_id,
            item_name=menu.item_name,
            description=menu.description,
            price=menu.price,
            available=menu.available
        )
    except Menu.DoesNotExist:
        raise HTTPException(status_code=404, detail="Menu item not found")


@app.post("/api/menu", response_model=MenuResponse)
def create_menu_item(menu: MenuCreate):
    try:
        restaurant = Restaurant.objects.get(id=menu.restaurant_id)
    except Restaurant.DoesNotExist:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    new_menu = Menu.objects.create(
        restaurant=restaurant,
        item_name=menu.item_name,
        description=menu.description,
        price=menu.price,
        available=menu.available
    )
    
    return MenuResponse(
        id=new_menu.id,
        restaurant_id=new_menu.restaurant_id,
        item_name=new_menu.item_name,
        description=new_menu.description,
        price=new_menu.price,
        available=new_menu.available
    )


# =========================
# Order Endpoints
# =========================

@app.get("/api/orders", response_model=List[OrderResponse])
def get_orders(user_id: Optional[int] = None, role: Optional[str] = None):
    if user_id:
        if role == 'restaurant':
            try:
                restaurant = Restaurant.objects.get(owner_id=user_id)
                orders = Order.objects.filter(restaurant=restaurant)
            except Restaurant.DoesNotExist:
                return []
        elif role == 'customer':
            orders = Order.objects.filter(customer_id=user_id)
        else:
            orders = Order.objects.all()
    else:
        orders = Order.objects.all()
    
    return [
        OrderResponse(
            id=o.id,
            customer_id=o.customer_id,
            restaurant_id=o.restaurant_id,
            item_id=o.item_id,
            quantity=o.quantity,
            total_price=o.total_price,
            status=o.status,
            payment_status=o.payment_status,
            created_at=o.created_at.isoformat()
        )
        for o in orders
    ]


@app.get("/api/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    try:
        order = Order.objects.get(id=order_id)
        return OrderResponse(
            id=order.id,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            item_id=order.item_id,
            quantity=order.quantity,
            total_price=order.total_price,
            status=order.status,
            payment_status=order.payment_status,
            created_at=order.created_at.isoformat()
        )
    except Order.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")


@app.post("/api/orders", response_model=OrderResponse)
def create_order(order: OrderCreate):
    try:
        customer = User.objects.get(id=order.customer_id)
        restaurant = Restaurant.objects.get(id=order.restaurant_id)
        menu_item = Menu.objects.get(id=order.item_id)
    except (User.DoesNotExist, Restaurant.DoesNotExist, Menu.DoesNotExist) as e:
        raise HTTPException(status_code=404, detail=f"Resource not found: {str(e)}")
    
    total_price = menu_item.price * order.quantity
    
    new_order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        item=menu_item,
        quantity=order.quantity,
        total_price=total_price,
        status='pending',
        payment_status=False
    )
    
    return OrderResponse(
        id=new_order.id,
        customer_id=new_order.customer_id,
        restaurant_id=new_order.restaurant_id,
        item_id=new_order.item_id,
        quantity=new_order.quantity,
        total_price=new_order.total_price,
        status=new_order.status,
        payment_status=new_order.payment_status,
        created_at=new_order.created_at.isoformat()
    )


@app.put("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status: str):
    try:
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()
        return {"message": "Order status updated", "status": status}
    except Order.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")


# =========================
# Payment Endpoints
# =========================

@app.get("/api/payments/{order_id}", response_model=PaymentResponse)
def get_payment(order_id: int):
    try:
        payment = Payment.objects.get(order_id=order_id)
        return PaymentResponse(
            id=payment.id,
            order_id=payment.order_id,
            amount=payment.amount,
            transaction_id=payment.transaction_id,
            success=payment.success,
            paid_at=payment.paid_at.isoformat()
        )
    except Payment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Payment not found")


@app.post("/api/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentCreate):
    try:
        order = Order.objects.get(id=payment.order_id)
    except Order.DoesNotExist:
        raise HTTPException(status_code=404, detail="Order not found")
    
    new_payment = Payment.objects.create(
        order=order,
        amount=payment.amount,
        success=True,
        transaction_id=f"TXN{payment.order_id}{payment.amount}"
    )
    
    # Update order payment status
    order.payment_status = True
    order.save()
    
    return PaymentResponse(
        id=new_payment.id,
        order_id=new_payment.order_id,
        amount=new_payment.amount,
        transaction_id=new_payment.transaction_id,
        success=new_payment.success,
        paid_at=new_payment.paid_at.isoformat()
    )


# =========================
# Coupon Endpoints
# =========================

@app.post("/api/coupons/validate")
def validate_coupon(coupon: CouponValidate):
    try:
        coupon_obj = Coupon.objects.get(code=coupon.code)
        
        if not coupon_obj.is_valid():
            return {"valid": False, "message": "Coupon is invalid or expired"}
        
        if coupon.order_amount < coupon_obj.min_order:
            return {
                "valid": False, 
                "message": f"Minimum order amount is {coupon_obj.min_order}"
            }
        
        discount = (coupon_obj.discount_percent * coupon.order_amount) / 100
        discount = min(discount, coupon_obj.max_discount)
        
        return {
            "valid": True,
            "discount": discount,
            "message": f"Coupon applied! You save ₹{discount}"
        }
    except Coupon.DoesNotExist:
        return {"valid": False, "message": "Coupon not found"}


@app.get("/api/coupons", response_model=List[dict])
def get_coupons():
    coupons = Coupon.objects.filter(active=True)
    return [
        {
            "code": c.code,
            "description": c.description,
            "discount_percent": c.discount_percent,
            "max_discount": c.max_discount,
            "min_order": c.min_order
        }
        for c in coupons
    ]


# =========================
# Rating Endpoints
# =========================

@app.get("/api/restaurants/{restaurant_id}/ratings", response_model=List[RatingResponse])
def get_restaurant_ratings(restaurant_id: int):
    ratings = Rating.objects.filter(restaurant_id=restaurant_id)
    return [
        RatingResponse(
            id=r.id,
            order_id=r.order_id,
            rating=r.rating,
            review=r.review
        )
        for r in ratings
    ]


@app.post("/api/ratings", response_model=RatingResponse)
def create_rating(rating: RatingCreate):
    try:
        customer = User.objects.get(id=rating.customer_id)
        restaurant = Restaurant.objects.get(id=rating.restaurant_id)
        order = Order.objects.get(id=rating.order_id)
    except (User.DoesNotExist, Restaurant.DoesNotExist, Order.DoesNotExist):
        raise HTTPException(status_code=404, detail="Resource not found")
    
    new_rating = Rating.objects.create(
        order=order,
        customer=customer,
        restaurant=restaurant,
        rating=rating.rating,
        review=rating.review,
        delivery_rating=rating.delivery_rating,
        delivery_review=rating.delivery_review
    )
    
    # Update restaurant rating
    ratings = Rating.objects.filter(restaurant=restaurant)
    avg_rating = sum(r.rating for r in ratings) / len(ratings)
    restaurant.rating = round(avg_rating, 1)
    restaurant.save()
    
    return RatingResponse(
        id=new_rating.id,
        order_id=new_rating.order_id,
        rating=new_rating.rating,
        review=new_rating.review
    )


# =========================
# Health Check
# =========================

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "GourmetGo API"}


@app.get("/")
def root():
    return {"message": "Welcome to GourmetGo API", "docs": "/docs"}

