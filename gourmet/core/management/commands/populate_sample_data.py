from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Profile, Restaurant, Menu, Coupon
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate sample data for GourmetGo'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create restaurant owners
        restaurants_data = [
            ('pizza_palace', 'pizza_palace@gmail.com', "Pizza Palace", "123 Main St"),
            ('burger_barn', 'burger_barn@gmail.com', "Burger Barn", "456 Oak Ave"),
            ('sushi_spot', 'sushi_spot@gmail.com', "Sushi Spot", "789 Park Ln"),
        ]

        for username, email, rest_name, location in restaurants_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password='password123')
                user.profile.role = 'restaurant'
                user.profile.save()
                
                Restaurant.objects.create(
                    owner=user,
                    name=rest_name,
                    location=location,
                    rating=4.5
                )
                self.stdout.write(f'✓ Created restaurant: {rest_name}')

        # Create menu items
        menu_items = [
            ('Pizza Palace', [
                ('Margherita Pizza', 'Fresh tomato sauce, mozzarella, basil', 299),
                ('Pepperoni Pizza', 'Pepperoni, cheese, tomato sauce', 349),
                ('Garlic Bread', 'Crispy bread with garlic butter', 99),
            ]),
            ('Burger Barn', [
                ('Classic Burger', 'Beef patty, cheese, lettuce, tomato', 199),
                ('Bacon Burger', 'Double patty with crispy bacon', 299),
                ('Chicken Sandwich', 'Grilled chicken with special sauce', 179),
            ]),
            ('Sushi Spot', [
                ('California Roll', 'Crab, avocado, cucumber', 249),
                ('Spicy Tuna Roll', 'Tuna with spicy mayo', 279),
                ('Salmon Nigiri', 'Fresh salmon on rice', 199),
            ]),
        ]

        for rest_name, items in menu_items:
            try:
                rest = Restaurant.objects.get(name=rest_name)
                for item_name, description, price in items:
                    if not Menu.objects.filter(restaurant=rest, item_name=item_name).exists():
                        Menu.objects.create(
                            restaurant=rest,
                            item_name=item_name,
                            description=description,
                            price=price,
                            available=True
                        )
                self.stdout.write(f'✓ Created {len(items)} menu items for {rest_name}')
            except Restaurant.DoesNotExist:
                pass

        # Create sample coupons
        coupons = [
            ('SAVE10', 'Save 10% on your order', 10, 200, 100),
            ('NEWUSER20', 'New users get 20% off', 20, 300, 150),
            ('WELCOME50', 'Welcome bonus - save 50 rupees', 0, 50, 200),
        ]

        for code, desc, percent, max_disc, min_order in coupons:
            if not Coupon.objects.filter(code=code).exists():
                Coupon.objects.create(
                    code=code,
                    description=desc,
                    discount_percent=percent,
                    max_discount=max_disc,
                    min_order=min_order,
                    valid_from=datetime.now(),
                    valid_until=datetime.now() + timedelta(days=90),
                    usage_limit=500,
                    active=True
                )
                self.stdout.write(f'✓ Created coupon: {code}')

        # Create sample customers
        customer_data = [
            ('customer1', 'customer1@gmail.com'),
            ('customer2', 'customer2@gmail.com'),
        ]

        for username, email in customer_data:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password='password123')
                user.profile.role = 'customer'
                user.profile.save()
                self.stdout.write(f'✓ Created customer: {username}')

        self.stdout.write(self.style.SUCCESS('✓ Sample data created successfully!'))
