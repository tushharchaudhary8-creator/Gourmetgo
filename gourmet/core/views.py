from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Restaurant, Menu, Order, Payment, Coupon, Rating
from django.conf import settings
from django.db import models


# =========================
# HOME (SHOW RESTAURANTS)
# =========================
def home(request):
    restaurants = Restaurant.objects.prefetch_related('menu_set').all()
    return render(request, 'home.html', {'restaurants': restaurants})


# =========================
# WORKFLOW DEMO
# =========================
def workflow_demo(request):
    return render(request, 'workflow_demo.html')


# =========================
# RESTAURANT GUIDE
# =========================
def restaurant_guide(request):
    return render(request, 'restaurant_guide.html')


# =========================
# REGISTER
# =========================
def register(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        role = request.POST.get('role', 'customer')
        
        errors = []
        
        # Validation
        if not username:
            errors.append('Username is required.')
        elif User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        
        if not email:
            errors.append('Email is required.')
        elif User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        
        if password != password_confirm:
            errors.append('Passwords do not match.')
        
        if errors:
            return render(request, 'auth/register.html', {'errors': errors, 'username': username, 'email': email, 'role': role})
        
        # Create user and update profile (signal auto-creates profile)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.role = role
        user.profile.save()
        
        # Auto-create restaurant if owner
        if role == 'restaurant':
            Restaurant.objects.create(owner=user, name=f"{username}'s Restaurant", location="Not set")
        
        return redirect('login')
    
    return render(request, 'auth/register.html')


# =========================
# LOGIN
# =========================
def user_login(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'auth/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


# =========================
# MY ORDERS PAGE
# =========================
@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    # Calculate order counts by status
    pending_count = orders.filter(status='pending').count()
    accepted_count = orders.filter(status='accepted').count()
    delivery_count = orders.filter(status='out_for_delivery').count()
    completed_count = orders.filter(status='delivered').count()
    
    # Pending payment orders
    pending_payment = orders.filter(payment_status=False)
    
    # Check if any orders have ratings
    has_rated = Rating.objects.filter(customer=request.user).exists()
    
    return render(request, 'orders.html', {
        'orders': orders,
        'pending_payment': pending_payment,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'delivery_count': delivery_count,
        'completed_count': completed_count,
        'has_rated': has_rated,
    })


# =========================
# DASHBOARD (ROLE BASED)
# =========================
# @login_required
# def dashboard(request):
#     role = request.user.profile.role

#     if role == 'customer':
#         menus = Menu.objects.all()
#         return render(request, 'dashboards/customer.html', {'menus': menus})

#     if role == 'restaurant':
#         restaurant = Restaurant.objects.filter(owner=request.user).first()
#         menu_items = Menu.objects.filter(restaurant=restaurant)
#         orders = Order.objects.filter(restaurant=restaurant)
#         return render(request, 'dashboards/restaurant.html', {
#             'restaurant': restaurant,
#             'menu_items': menu_items,
#             'orders': orders
#         })

#     if role == 'delivery':
#         orders = Order.objects.filter(status='out_for_delivery')
#         return render(request, 'dashboards/delivery.html', {'orders': orders})

@login_required
def dashboard(request):
    # In production (DEBUG=False) redirect users to home instead of showing dashboards
    if not settings.DEBUG:
        return redirect('home')

    role = request.user.profile.role.lower()

    if role == 'customer':
        menus = Menu.objects.all()
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, 'dashboards/customer.html', {'menus': menus, 'orders': orders})

    elif role == 'restaurant':
        restaurant = Restaurant.objects.filter(owner=request.user).first()
        menu_items = Menu.objects.filter(restaurant=restaurant)
        orders = Order.objects.filter(restaurant=restaurant).order_by('-created_at')
        return render(request, 'dashboards/restaurant.html', {
            'restaurant': restaurant,
            'menu_items': menu_items,
            'orders': orders
        })

    elif role == 'delivery':
        orders = Order.objects.filter(status='out_for_delivery').order_by('-created_at')
        return render(request, 'dashboards/delivery.html', {'orders': orders})

    return redirect('home')


# =========================
# MANAGE MENU (RESTAURANT)
# =========================
@login_required
def manage_menu(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()

    if request.method == "POST":
        Menu.objects.create(
            restaurant=restaurant,
            item_name=request.POST['item_name'],
            description=request.POST.get('description', ''),
            price=int(request.POST['price'])
        )

        return redirect('dashboard')

    menu_items = Menu.objects.filter(restaurant=restaurant)
    return render(request, 'restaurants/menu.html', {'menu_items': menu_items})


# =========================
# RESTAURANT ORDERS
# =========================
@login_required
def restaurant_orders(request):
    restaurant = Restaurant.objects.filter(owner=request.user).first()
    orders = Order.objects.filter(restaurant=restaurant).order_by('-created_at')
    return render(request, 'restaurants/orders.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.status = request.POST['status']
        order.save()
    return redirect('dashboard')


# =========================
# PLACE ORDER (CUSTOMER)
# =========================
@login_required
def place_order(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

    order = Order.objects.create(
        customer=request.user,
        restaurant=menu.restaurant,
        item=menu,
        total_price=menu.price,
        payment_status=False,  # Set payment as pending
    )

    # Create payment record (not paid yet)
    Payment.objects.create(order=order, amount=menu.price, success=False)

    return redirect('dashboard')


# =========================
# PROCESS PAYMENT (CUSTOMER)
# =========================
@login_required
def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    if request.method == "POST":
        # Handle coupon application
        coupon_code = request.POST.get('coupon_code', '').strip()
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid() and order.total_price >= coupon.min_order:
                    discount = min(int(order.total_price * coupon.discount_percent / 100), coupon.max_discount)
                    order.discount = discount
                    order.coupon = coupon
                    coupon.used_count += 1
                    coupon.save()
                    order.save()
                    return render(request, 'payment/payment.html', {'order': order, 'success': f'Coupon applied! Discount: ₹{discount}'})
                else:
                    return render(request, 'payment/payment.html', {'order': order, 'error': 'Coupon is invalid or expired'})
            except Coupon.DoesNotExist:
                return render(request, 'payment/payment.html', {'order': order, 'error': 'Coupon code not found'})
        
        # Process payment
        payment = Payment.objects.filter(order=order).first()
        if payment:
            payment.success = True
            payment.amount = order.total_price - order.discount  # Update payment amount after discount
            payment.save()
        
        order.payment_status = True
        order.save()
        
        return redirect('dashboard')
    
    return render(request, 'payment/payment.html', {'order': order})


# =========================
# RATING & REVIEWS (CUSTOMER)
# =========================
@login_required
def rate_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    
    if order.status != 'delivered':
        return redirect('dashboard')
    
    if request.method == "POST":
        rating = request.POST.get('rating', 3)
        review = request.POST.get('review', '')
        delivery_rating = request.POST.get('delivery_rating', None)
        delivery_review = request.POST.get('delivery_review', '')
        
        Rating.objects.update_or_create(
            order=order,
            customer=request.user,
            defaults={
                'restaurant': order.restaurant,
                'rating': int(rating),
                'review': review,
                'delivery_rating': int(delivery_rating) if delivery_rating else None,
                'delivery_review': delivery_review,
            }
        )
        
        # Update restaurant rating average
        avg_rating = Rating.objects.filter(restaurant=order.restaurant).aggregate(
            avg=models.Avg('rating')
        )['avg']
        order.restaurant.rating = avg_rating if avg_rating else 0
        order.restaurant.save()
        
        return redirect('dashboard')
    
    existing_rating = Rating.objects.filter(order=order).first()
    return render(request, 'rating/rate_order.html', {'order': order, 'existing_rating': existing_rating})
