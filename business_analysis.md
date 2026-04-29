# RepairMyBike — Business Systems Analysis

## ✅ What You Already Have (Built)

### 1. 🔐 Authentication (`authentication`)
- Custom [User](file:///d:/developer/repairmybike/repairmybike_backend/authentication/models.py#7-21) model with **Descope** OTP (phone + email) integration
- Guest sessions — users can browse without signing up
- [UserAddress](file:///d:/developer/repairmybike/repairmybike_backend/authentication/models.py#23-45) — saved delivery addresses
- [UserSession](file:///d:/developer/repairmybike/repairmybike_backend/authentication/models.py#47-66) — active session tracking with device info & IP
- [StaffDirectory](file:///d:/developer/repairmybike/repairmybike_backend/authentication/models.py#150-167) — pre-provisioned staff logins
- [ContactMessage](file:///d:/developer/repairmybike/repairmybike_backend/authentication/models.py#186-200) — landing page contact form messages
- [OTPAttempt](file:///d:/developer/repairmybike/repairmybike_backend/authentication/models.py#120-148) — rate-limit tracking for OTP abuse

---

### 2. 🚲 Vehicles (`vehicles`)
- [VehicleType](file:///d:/developer/repairmybike/repairmybike_backend/vehicles/models.py#3-15) → [VehicleBrand](file:///d:/developer/repairmybike/repairmybike_backend/vehicles/models.py#17-31) → [VehicleModel](file:///d:/developer/repairmybike/repairmybike_backend/vehicles/models.py#33-47) hierarchy (3 levels)
- [UserVehicle](file:///d:/developer/repairmybike/repairmybike_backend/vehicles/models.py#49-64) — user's garage (default bike + registration number)
- Images for each level

---

### 3. 🔧 Services (`services`)
- [ServiceCategory](file:///d:/developer/repairmybike/repairmybike_backend/services/models.py#6-24) + [Service](file:///d:/developer/repairmybike/repairmybike_backend/services/models.py#26-45) + [ServicePricing](file:///d:/developer/repairmybike/repairmybike_backend/services/models.py#47-62) (price per vehicle model)
- Per-service `rating`, `reviews_count`, `specifications` (JSON), images
- [UserSavedService](file:///d:/developer/repairmybike/repairmybike_backend/services/models.py#64-76) + [GuestSavedService](file:///d:/developer/repairmybike/repairmybike_backend/services/models.py#78-91) — wishlisting

---

### 4. 📅 Bookings (`bookings`)
- [Customer](file:///d:/developer/repairmybike/repairmybike_backend/bookings/models.py#14-27) profile (name, phone, email)
- [Booking](file:///d:/developer/repairmybike/repairmybike_backend/bookings/models.py#29-78) — home or shop visit, appointment date/time, payment method (cash/Razorpay), multi-status flow (`pending → confirmed → in_progress → completed → cancelled`)
- [BookingService](file:///d:/developer/repairmybike/repairmybike_backend/bookings/models.py#80-91) — multiple services per booking
- Linked to subscriptions for visit tracking

---

### 5. 💳 Payments (`payments`)
- [Payment](file:///d:/developer/repairmybike/repairmybike_backend/payments/models.py#5-33) — Razorpay order/payment/signature capture for bookings
- Full payment status lifecycle: `created → authorized → captured → failed → refunded`

---

### 6. 🪙 Subscriptions (`subscriptions`)
- [Plan](file:///d:/developer/repairmybike/repairmybike_backend/subscriptions/models.py#8-62) — Basic/Premium tiers, monthly/quarterly/half-yearly/yearly billing
- [PlanBenefit](file:///d:/developer/repairmybike/repairmybike_backend/subscriptions/models.py#64-77) — structured benefit bullets per plan
- [Subscription](file:///d:/developer/repairmybike/repairmybike_backend/subscriptions/models.py#79-142) — user subscription linked to Razorpay, with `visits_consumed` counter
- Auto-computes [end_date](file:///d:/developer/repairmybike/repairmybike_backend/subscriptions/models.py#124-135) and `next_billing_date`

---

### 7. 🛒 Spare Parts (`spare_parts`)
- Full catalog: [SparePartCategory](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#8-22), [SparePartBrand](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#24-37), [SparePart](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#39-78)
- Rich part data: SKU, EAN, specs (JSON), dimensions, warranty info
- [SparePartFitment](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#95-106) — which part fits which vehicle model
- [SparePartImage](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#80-93) with primary image flag
- Full cart → order flow: [Cart](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#108-124) + [CartItem](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#126-142) → [Order](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#144-184) + [OrderItem](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#186-198)
- Shipping tracking fields (`tracking_number`, `courier_name`, `estimated_delivery`)
- [UserSavedPart](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#199-211) / [GuestSavedPart](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#213-225) — wishlisting

---

### 8. ⚡ Quick Service (`quick_service`)
- [QuickServiceConfig](file:///d:/developer/repairmybike/repairmybike_backend/quick_service/models.py#4-18) — admin-configurable rules and base price
- [QuickServiceRequest](file:///d:/developer/repairmybike/repairmybike_backend/quick_service/models.py#19-43) — user calls, mechanic dispatched, status tracked

---

### 9. ⭐ Feedback (`feedback`)
- [Review](file:///d:/developer/repairmybike/repairmybike_backend/feedback/models.py#7-50) — multi-dimensional ratings (overall, quality, staff behavior, app)
- Generic FK can attach to either a [Service](file:///d:/developer/repairmybike/repairmybike_backend/services/models.py#26-45) or [SparePart](file:///d:/developer/repairmybike/repairmybike_backend/spare_parts/models.py#39-78)
- `chips` (tags like "On-Time", "Professional")
- [ReviewPhoto](file:///d:/developer/repairmybike/repairmybike_backend/feedback/models.py#51-58) — photo uploads on reviews
- Verified flag to ensure only genuine buyers review

---

### 10. 📊 Dashboard (`dashboard`)
- Admin dashboard app exists (WebSocket consumer for real-time updates)

---

## ❌ What's Missing — Build This for a Successful Business

### 🔴 Critical (Without These, Business Loses Money/Customers)

| Gap | Why It Matters |
|---|---|
| **Push Notifications** | No FCM/APNs integration. You can't alert customers when mechanic is dispatched, booking is confirmed, or order is shipped. Customers feel ignored. |
| **WhatsApp / SMS Alerts** | No automated booking confirmation or reminder SMS/WhatsApp. Customers forget appointments → no-shows = lost revenue. |
| **Razorpay Webhooks** | Payment failures aren't auto-handled. If a payment fails, booking status doesn't update automatically. Manual intervention needed. |
| **Subscription Auto-Renewal** | `auto_renew=True` exists but there's no cron/Celery task to actually renew it. Subscriptions silently expire. |
| **Refund Tracking** | `Payment.status` has `refunded` but no refund API or flow exists. Refunds have to be done manually in Razorpay dashboard. |
| **Order Shipping Integration** | Tracking number fields exist but no courier API (Shiprocket/Delhivery) connected. Staff manually updates tracking. |

---

### 🟡 Important (Better Customer Relationships)

| Gap | Why It Matters |
|---|---|
| **Mechanic/Staff Assignment** | No model to assign a specific mechanic to a booking. Customer doesn't know who's coming. |
| **Real-time Mechanic Tracking** | No GPS/live location for the mechanic. High-end competitors (Urban Company) offer this. |
| **Loyalty / Reward Points** | No points system. No reason for customers to return over a competitor. |
| **Referral Program** | No referral code system. Word-of-mouth growth is free but not incentivized. |
| **Promo Codes / Coupons** | No `Coupon` model or discount logic. Can't run seasonal offers. |
| **Customer Complaint / Issue Ticket** | No formal complaint tracking. If a job goes wrong, there's no escalation path. |
| **Service History per Vehicle** | No query to show "all services done on my Activa 5G". Key for trust and upsells. |
| **Recurring Service Reminders** | No system to remind "Your oil change is due in 30 days". Huge retention driver. |

---

### 🟢 Growth & Analytics (Scale the Business)

| Gap | Why It Matters |
|---|---|
| **Business Analytics Dashboard** | No revenue charts, booking trends, top services, or customer LTV (lifetime value) data. |
| **Mechanic Performance Reports** | Can't measure who is the best mechanic or who gets the most complaints. |
| **Inventory Management** | `stock_qty` exists on spare parts but no low-stock alert or reorder system. |
| **Multi-location / Franchise Support** | No `Shop`/`Branch` model. Can't expand to multiple cities cleanly. |
| **Customer Segments / CRM Tags** | No tagging of customers (e.g., "High Value", "At Risk", "New"). Can't do targeted marketing. |
| **API Rate Limiting & Abuse Protection** | No throttling beyond OTP attempts. Vulnerable to scraping and abuse. |

---

## 🗺️ Recommended Build Roadmap

```
Phase 1 — Stop Losing Money (1-2 months)
  - [x] **Set up Celery + Redis** (Automation engine)
  - [x] **Configure Celery Beat** (Scheduled logic)
  - [x] **Automated Subscriptions** (Renewal/Expiry)
  - [x] **Automated Push Notifications** (Status updates)
  - [x] **Recurring Service Reminders** (Retention)
  - [x] **Service History API** (Vehicle-specific repair log)
  - [x] **Loyalty Points System** (1 point per ₹100 spend)
  - [x] **Referral Program** (₹500 reward for successful referral)
  - [x] **Mechanic Live-Tracking** (Real-time map updates)
  - [ ] **WhatsApp/SMS alerts** (MSG91 or Twilio)
  - [ ] **Razorpay Webhooks Logic** (For automated payment confirmation)

Phase 2 — Delight Customers (2-3 months)
  ✦ Push notifications (Firebase FCM)
  ✦ Mechanic assignment model
  ✦ Promo codes / coupons
  ✦ Service history per vehicle API
  ✦ Complaint/issue ticket system

Phase 3 — Grow the Business (3-6 months)
  ✦ Loyalty points & referral program
  ✦ Recurring service reminders (Celery periodic tasks)
  ✦ Admin analytics dashboard (revenue, bookings, top services)
  ✦ Inventory alerts for spare parts
  ✦ Multi-location / branch support
```

> **Bottom line:** The core transactional backbone is solid. The biggest immediate risk is silent payment failures and subscription expirations. The biggest customer relationship gap is zero proactive communication (no SMS, no push, no reminders).
