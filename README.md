# GourmetGo - Food Delivery Platform

A comprehensive Django-based food delivery platform with order tracking, payment processing, ratings, and role-based dashboards.

## Features

- **User Authentication**: Secure login and registration for customers, restaurants, and delivery personnel
- **Order Management**: Complete order lifecycle management with real-time tracking
- **Payment Processing**: Integrated payment system with multiple payment methods
- **Rating & Reviews**: Customer ratings and feedback system for restaurants and orders
- **Role-Based Dashboards**: 
  - Customer Dashboard: View orders, ratings, and payment history
  - Restaurant Dashboard: Manage menu items, view orders, and analytics
  - Delivery Dashboard: Track deliveries and update order status
- **Menu Management**: Restaurants can create and manage menu items with descriptions
- **Coupon System**: Support for discount coupons on orders
- **Real-time Order Tracking**: Track food delivery status in real-time

## Tech Stack

- **Backend**: Django 3.x+
- **Database**: SQLite (development) / PostgreSQL (production recommended)
- **Frontend**: HTML5, CSS3, JavaScript
- **Payment**: Integrated payment gateway support

## Project Structure

```
gourmetgo_clean/
├── gourmet/                    # Main Django project
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # URL routing
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── core/                       # Core app
│   ├── models.py               # Database models
│   ├── views.py                # View logic
│   ├── urls.py                 # App URL routes
│   ├── forms.py                # Form definitions
│   ├── signals.py              # Django signals
│   ├── admin.py                # Admin configuration
│   ├── management/             # Custom management commands
│   │   └── commands/
│   │       └── populate_sample_data.py
│   └── migrations/             # Database migrations
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── auth/                   # Authentication templates
│   ├── dashboards/             # Dashboard templates
│   ├── restaurants/            # Restaurant templates
│   ├── payment/                # Payment templates
│   └── rating/                 # Rating templates
├── static/                     # Static files (CSS, JS, images)
├── db.sqlite3                  # SQLite database
└── manage.py                   # Django management script
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tushharchaudhary8-creator/Gourmetgo.git
   cd Gourmetgo
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django
   ```

4. **Run migrations**
   ```bash
   cd gourmet
   python manage.py migrate
   ```

5. **Load sample data (optional)**
   ```bash
   python manage.py populate_sample_data
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`

## Usage

### Admin Panel
- Access Django admin at `/admin` with your superuser credentials
- Manage users, restaurants, menus, orders, and payments

### Customer Portal
- Register and login
- Browse restaurants and menus
- Place orders
- Track order status
- Rate restaurants and orders
- Apply discount coupons

### Restaurant Portal
- Manage menu items and descriptions
- View and process orders
- Track order delivery status
- View analytics and ratings

### Delivery Portal
- View assigned deliveries
- Update delivery status
- Track earnings

## API Endpoints

Key endpoints available:
- `/auth/login/` - User login
- `/auth/register/` - User registration
- `/orders/` - Order management
- `/payment/` - Payment processing
- `/rating/` - Rating and reviews
- `/restaurants/` - Restaurant information and menus

## Database Models

- **User**: Extended user model with role-based access
- **Restaurant**: Restaurant information and metadata
- **Menu**: Menu items with descriptions and pricing
- **Order**: Order details with status tracking
- **OrderItem**: Items in an order
- **Payment**: Payment transaction records
- **Rating**: Customer ratings for restaurants and orders
- **Coupon**: Discount coupon management

## Configuration

Edit `gourmet/settings.py` to:
- Change database settings
- Configure static/media files
- Set up payment gateway credentials
- Configure email settings
- Adjust security settings for production

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

## Author

Tushar Chaudhari - [GitHub](https://github.com/tushharchaudhary8-creator)

---

**Happy Food Delivery! 🍔🚚**
