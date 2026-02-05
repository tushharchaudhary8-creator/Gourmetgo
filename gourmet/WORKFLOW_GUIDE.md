# GourmetGo Order Workflow Guide

## 📋 Complete Order Flow

This guide shows how to test the complete order lifecycle from customer placing an order to restaurant owner managing it and delivery boy tracking it.

---

## 🏃 Quick Start: Test Accounts

Use these sample accounts created during setup:

### Customer Accounts
- **Username:** `customer1` | **Password:** `password123`
- **Username:** `customer2` | **Password:** `password123`

### Restaurant Owner Accounts
- **Username:** `pizza_palace` | **Password:** `password123`
- **Username:** `burger_barn` | **Password:** `password123`
- **Username:** `sushi_spot` | **Password:** `password123`

### Delivery Partner Accounts
- **Username:** `delivery1` | **Password:** `password123`

---

## 🔄 Step-by-Step Order Workflow

### Step 1️⃣: CUSTOMER PLACES ORDER

**Logged in as:** `customer1`

1. Go to **Home** page (`/`)
2. Browse available restaurants and their menu items
3. Click **"Order Now"** on any food item
4. Order is created and appears in your **Dashboard** → **Pending Payment** section
5. Status: **Pending** (waiting for restaurant to accept)

### Step 2️⃣: PAYMENT (Optional Demo)

**Logged in as:** `customer1`

1. In **Dashboard**, find order in **Pending Payment** section
2. Click **"Pay Now"** button
3. Enter coupon code (optional): `SAVE10`, `NEWUSER20`, or `WELCOME50`
4. Click **"Apply Coupon"** to see discount
5. Select payment method (Card, UPI, Wallet)
6. Click **"Pay ₹XXX"**
7. Order moves to **Order Status** section with **Payment: ✓ Paid**

**Available Coupons:**
- `SAVE10` - 10% discount (max ₹200 off)
- `NEWUSER20` - 20% discount (max ₹300 off)
- `WELCOME50` - ₹50 fixed discount (min ₹200 order)

---

### Step 3️⃣: RESTAURANT OWNER MANAGES ORDER

**Logged in as:** `pizza_palace` (or any restaurant owner)

1. Go to **Dashboard** → See all incoming orders
2. For each order, see **Status dropdown** with options:
   - **Pending** → Initial state (customer just ordered)
   - **Accepted** → Restaurant confirms it will prepare
   - **Out for Delivery** → Food ready, sent to delivery boy
   - **Delivered** → Customer received the order

3. **To update status:**
   - Click the **Status dropdown** for an order
   - Select new status
   - Status updates automatically

**Order Details visible:**
- Item name
- Customer username
- Quantity
- Total price
- Payment status (Paid ✓ or Pending ✗)

---

### Step 4️⃣: DELIVERY BOY TRACKS & UPDATES

**Logged in as:** `delivery1` (or any delivery role account)

1. Go to **Dashboard** → See **Delivery Orders** section
2. Only shows orders with status: **"Out for Delivery"**
3. For each delivery, see:
   - Item name
   - From (Restaurant name & location)
   - To (Customer username)
   - Current location

4. **To complete delivery:**
   - Click the **Status dropdown**
   - Change from "Out for Delivery" → "Delivered"
   - Status updates automatically
   - Order now shows as **Delivered** in customer's dashboard

---

### Step 5️⃣: CUSTOMER RATES ORDER

**Logged in as:** `customer1`

1. After order status = **"Delivered"**, a **"Rate"** button appears
2. Click **"Rate"** button
3. Fill rating form:
   - **Restaurant Rating:** Select 1-5 stars
   - **Review:** Write optional feedback about food
   - **Delivery Rating:** Select 1-5 stars
   - **Delivery Review:** Write optional feedback about delivery
4. Click **"Submit Rating"**
5. Restaurant's overall rating automatically updates (average of all ratings)

---

## 📊 Status Flow Diagram

```
CUSTOMER PLACES ORDER
        ↓
    Pending (waiting for restaurant)
        ↓
Restaurant accepts (RESTAURANT OWNER updates status)
        ↓
    Accepted (restaurant preparing food)
        ↓
Restaurant marks as ready (RESTAURANT OWNER updates status)
        ↓
    Out for Delivery (food sent to customer)
        ↓
Delivery boy updates (DELIVERY BOY updates status)
        ↓
    Delivered (customer received food)
        ↓
Customer rates order (CUSTOMER submits rating)
        ↓
   ⭐ COMPLETE
```

---

## 🎯 Dashboard Views by Role

### 👤 CUSTOMER DASHBOARD
Shows:
- ✅ **Order Food** - Browse all restaurants & menu items
- ✅ **Pending Payment** - Orders awaiting payment
- ✅ **Order Status** - Track all orders with live status
- ✅ **Rate Button** - Rate orders once delivered

### 🍽️ RESTAURANT OWNER DASHBOARD
Shows:
- ✅ **Add Menu Item** - Form to add food items
- ✅ **Your Menu** - All menu items with availability
- ✅ **Incoming Orders** - All customer orders
- ✅ **Status Dropdown** - Change order status
- ✅ **Payment Status** - See if customer paid

### 🚴 DELIVERY BOY DASHBOARD
Shows:
- ✅ **Delivery Orders** - Only "Out for Delivery" orders
- ✅ **From Restaurant** - Which restaurant order is from
- ✅ **To Customer** - Customer receiving the order
- ✅ **Location** - Restaurant location for pickup
- ✅ **Status Dropdown** - Mark as "Delivered" when done

---

## 🔑 Key Features

### ✨ Coupon System
- **Auto-apply:** Enter code at payment page
- **Tracks usage:** Can't use same coupon beyond limit
- **Expires:** Coupons have expiry dates
- **Dynamic discount:** Shows exact discount before paying

### ⭐ Rating System
- **Post-delivery only:** Can rate after order delivered
- **Dual rating:** Rate restaurant food AND delivery service
- **Auto-calculate:** Restaurant rating updates instantly
- **Reviews:** Optional text feedback for each rating

### 💳 Payment System
- **Pending state:** Orders created with payment_status=False
- **Confirmation:** Payment marked as success after submission
- **Discount tracking:** Applied discounts saved to order
- **Payment records:** All transactions logged

---

## 🧪 Testing Scenario

### Complete Test Flow (15 mins)

1. **Login as customer1** → Place order for pizza
2. **Go to payment** → Apply "SAVE10" coupon → Pay
3. **Login as pizza_palace** → See order → Mark as "Accepted"
4. **Still as pizza_palace** → Mark as "Out for Delivery"
5. **Login as delivery1** → See order in deliveries
6. **As delivery1** → Mark as "Delivered"
7. **Back to customer1** → See "Rate" button → Submit rating
8. **Check restaurant rating** → Should show average of all ratings

---

## 🐛 Troubleshooting

**Q: Order not appearing in delivery dashboard?**
- A: Only orders with status "Out for Delivery" show up
- Set restaurant to mark order as "Out for Delivery" first

**Q: Can't rate order?**
- A: Order must be status "Delivered" first
- Rate button only shows for delivered orders

**Q: Coupon not applying?**
- A: Check expiry date and usage limit
- Min order amount must be met

**Q: Restaurant not showing in dropdown?**
- A: Restaurant must have at least one menu item
- Create menu items first

---

## 📱 URLs Map

- **Home:** `/`
- **Register:** `/register/`
- **Login:** `/login/`
- **Dashboard:** `/dashboard/`
- **Place Order:** `/order/<menu_id>/`
- **Payment:** `/payment/<order_id>/`
- **Rate Order:** `/rate/<order_id>/`
- **Manage Menu:** `/manage-menu/`
- **Update Status:** `/update-order/<order_id>/`

---

## 🎨 UI/UX Features

### Color-Coded Status Badges
- 🟨 **Pending** - Yellow (waiting)
- 🟩 **Accepted** - Green (confirmed)
- 🟦 **Out for Delivery** - Blue (in transit)
- 🟩 **Delivered** - Green (complete)

### Payment Indicators
- ✅ **Paid** - Green checkmark
- ❌ **Pending** - Red cross

### Interactive Elements
- Smooth hover animations
- Dropdown status updates
- Form validation with error messages
- Success/error alerts

---

**Happy Testing! 🚀**
