# RepairMyBike: Full-Stack System Design & Architecture

This document provides a comprehensive technical overview of the **RepairMyBike** ecosystem. It is intended for developers and architects to understand the core infrastructure, data flow, and technology choices.

---

## 1. System Overview
RepairMyBike is a hyperlocal service platform for two-wheelers. It comprises a **Flutter Mobile App** for customers/mechanics and a **Django REST Backend** for operations and business logic.

### Core Philosophy:
- **Modular Backend:** Specialized Django apps for clear separation of concerns (Bookings, Spares, Auth).
- **Service-Oriented Frontend:** Flutter with Provider pattern for predictable state management.
- **Offline-First Resilience:** Support for patchy network conditions (retry interceptors, local caching).
- **Cash-Friendly Workflow:** Optimized for offline payments and manual reconciliation.

---

## 2. Backend Architecture (Django REST Framework)
The backend is structured into domain-specific modules, ensuring that changes to one feature (e.g., Spare Parts) do not impact others (e.g., Booking logic).

### Key Modules (Apps):
- `authentication`: Custom User model supporting Phone-Number-based OTP auth, roles (Staff, Customer), and `UserAddress` management.
- `bookings`: Orchestrates the service lifecycle (Service Categories -> Models -> Tiers -> Scheduling -> Assignment).
- `spare_parts`: Full E-commerce engine for parts, including inventory management, shipping updates, and order tracking.
- `dashboard`: Internal operations hub using Django Channels for real-time WebSocket notifications.
- `staff`: Dedicated REST endpoints for field personnel (Mechanics) to manage assigned tasks.
- `notifications`: Centralized service for Firebase Push Notifications, Email, and SMS/WhatsApp.
- `vehicles`: Normalized registry of Bike Brands, Models, and Engine Types (used globally).

### Database Schema (Entity Relationship)
- **User & Profile:** Extends `AbstractUser`. One-to-many relationship with `UserAddress`.
- **Booking Engine:**
    - `Booking` (Header): Links to Customer, Vehicle Model, and Staff.
    - `BookingService` (Lines): Intermediary for many-to-many relationship between Bookings and Services.
    - `BookingStatusUpdate`: Historical audit log of every state change (Pending -> Completed).
- **Commerce Engine:**
    - `Order`: Links to `SparePart` through `OrderItem`.
    - `ShipmentUpdate`: Tracks granular movement of parts.

---

## 3. Frontend Architecture (Flutter)
The frontend uses a clean UI layer separated from data providers.

### Tech Stack:
- **State Management:** `Provider` (used for Auth, Routing, Cart, and Idempotency).
- **Navigation:** `GoRouter` for deep-linking and declarative route handling.
- **Networking:** Custom `SecureApiClient` wrapped around `Dio`, implementing:
    - `OfflineRetryInterceptor` for network resilience.
    - Automatic Token Injection for authenticated requests.
- **Layouts:** Custom `MainShell` with adaptive bottom navigation.

### Frontend Synchronization:
- **Optimistic UI:** Cart updates and simple status toggles happen instantly, with rollback on failure.
- **Idempotency:** A `Unique-Request-ID` header is sent with critical POST requests (bookings/orders) to prevent duplicate transactions on network retries.
- **Media:** Cloudinary SDK for efficient image retrieval and transformation.

---

## 4. Real-Time Operations (Staff Panel)
The staff-side system leverages a **Hybrid Sync Strategy**:
1. **Initial Hydration:** When a staff member opens the dashboard, the data is fetched via standard HTTP REST.
2. **Real-time Push:** A WebSocket connection (`/ws/dashboard/notifications/`) listens for events.
3. **Event Types:**
    - `NEW_BOOKING`: Triggers a toast and chimes.
    - `STATUS_CHANGED`: Updates the live activity feed.
    - `LOW_STOCK`: Alert if a spare part inventory dips.

---

## 5. Security & Authentication
- **Customer Auth:** Stateless JWT/DRF Tokens.
- **Staff Auth:** Traditional Session-based auth for the Web Dashboard + Token-based for API access.
- **Access Control:** `IsStaffAuthenticated` custom permission class enforces role-based access.
- **Legacy Support:** `STAFF_API_KEY` header for programmatic automation (to be deprecated in favor of IAM).

---

## 6. Points for Improvement (Peer Review)
*As a developer building this system, here are the identified gaps where a senior engineer's input is valued:*

1. **Database Bottlenecks:** Aggregating dashboard metrics (Revenue, Task counts) currently uses standard Django `aggregate()`. As data grows, this should move to a cache-aside pattern or a separate materialized view (Redis/PostgreSQL View).
2. **State Management Migration:** While `Provider` works well now, complex nested states in the "Booking Form" might benefit from `Riverpod` for better testability and reactivity.
3. **Role Granularity:** The current binary `is_staff` check is too broad. Implementing `django-guardian` for Object-Level Permissions is recommended for multi-vendor scaling.
4. **Offline Sync:** Implement a standard `SyncQueue` for offline-created bookings that doesn't rely solely on HTTP interceptors.

---

## 7. Deployment & Infrastructure
- **Web Server:** Gunicorn with Daphne for ASGI/WebSocket support.
- **Environment:** Containerized via Docker.
- **Media Engine:** Cloudinary for storage; Whitenoise for static files.
- **Database:** PostgreSQL (highly recommended over SQLite for production concurrency).
