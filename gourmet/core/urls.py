from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),
    path('workflow/', views.workflow_demo, name='workflow_demo'),
    path('restaurant-guide/', views.restaurant_guide, name='restaurant_guide'),

    # AUTH
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # ORDERS
    path('my-orders/', views.my_orders, name='my_orders'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # RESTAURANT FEATURES
    path('manage-menu/', views.manage_menu, name='manage_menu'),
    path('restaurant-orders/', views.restaurant_orders, name='restaurant_orders'),
    path('update-order/<int:order_id>/', views.update_order_status, name='update_order_status'),

    # CUSTOMER FEATURES
    path('order/<int:menu_id>/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('rate/<int:order_id>/', views.rate_order, name='rate_order'),
]
