from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta


# =========================
# USER PROFILE (ROLE SYSTEM)
# =========================
class Profile(models.Model):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant'),
        ('delivery', 'Delivery Partner'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# =========================
# RESTAURANT MODEL
# =========================
class Restaurant(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


# =========================
# MENU / FOOD ITEMS
# =========================
class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.item_name} ({self.restaurant.name})"


# =========================
# ORDER SYSTEM
# =========================
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    discount = models.IntegerField(default=0)  # Discount amount in rupees
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


# =========================
# PAYMENT MODEL
# =========================
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    success = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


# =========================
# COUPON / PROMO CODE SYSTEM
# =========================
class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=200, blank=True)
    discount_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_discount = models.IntegerField(default=500)  # Max discount in rupees
    min_order = models.IntegerField(default=100)  # Minimum order amount to apply
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    usage_limit = models.IntegerField(default=100)
    used_count = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def is_valid(self):
        return self.active and self.used_count < self.usage_limit and datetime.now() < self.valid_until

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% off"


# =========================
# RATING & REVIEW SYSTEM
# =========================
class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    delivery_rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    delivery_review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating for Order #{self.order.id} - {self.rating} stars"

    class Meta:
        unique_together = ('order', 'customer')
