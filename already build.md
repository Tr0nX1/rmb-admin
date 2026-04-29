  WHAT'S ALREADY BUILT ✅

  Backend (Django) — 213 files

  ┌──────────────────────────────────────────┬────────────────┬───────────────────────────────────────────────────────┐
  │                  Module                  │     Status     │                         Notes                         │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Authentication (OTP, JWT, Guest)         │ ✅ Complete    │ Descope + custom auth                                 │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Vehicles catalog                         │ ✅ Complete    │ Type → Brand → Model                                  │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Services catalog                         │ ✅ Complete    │ Categories, tiers, pricing                            │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Bookings                                 │ ✅ Complete    │ CRUD, idempotency, live location WS                   │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Subscription plans + signals             │ ✅ Complete    │ Multiple billing periods                              │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Subscription renewal (Celery task)       │ ✅ Complete    │ Auto-renew, expire, 3-day reminder                    │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Payments — Razorpay create + HMAC verify │ ✅ Complete    │ Signature validation present                          │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Refund workflow                          │ ✅ Complete    │ Full state machine (request→approve→process→complete) │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Spare parts e-commerce                   │ ✅ Complete    │ Cart, orders, shipment tracking                       │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Quick/emergency service                  │ ✅ Complete    │                                                       │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Notifications (FCM push)                 │ ✅ Complete    │ Celery async tasks                                    │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Dashboard WebSocket + SSE                │ ✅ Complete    │ Real-time metrics + live feed                         │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Staff / mechanic job management          │ ✅ Complete    │                                                       │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Feedback & Reviews                       │ ✅ Complete    │ Multi-dimensional ratings                             │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Content/CMS                              │ ✅ Complete    │                                                       │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Policies                                 │ ✅ Complete    │                                                       │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Shop                                     │ ✅ Complete    │                                                       │
  ├──────────────────────────────────────────┼────────────────┼───────────────────────────────────────────────────────┤
  │ Promotions                               │ ⚠️ Models only │ No views/endpoints                                    │
  └──────────────────────────────────────────┴────────────────┴───────────────────────────────────────────────────────┘

  Frontend (Flutter) — 94 files

  ┌───────────────────────────────┬─────────────┐
  │            Screen             │   Status    │
  ├───────────────────────────────┼─────────────┤
  │ Auth (OTP login)              │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Home / Landing                │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Booking form + list           │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Cart + Checkout               │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Spare parts catalog + detail  │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Subscription plans + checkout │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Quick service                 │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Profile + address             │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Notifications page            │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Feedback / Reviews            │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Vehicles selector             │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Saved services/parts          │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Search                        │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Policies / content            │ ✅ Complete │
  ├───────────────────────────────┼─────────────┤
  │ Order history                 │ ✅ Complete │
  └───────────────────────────────┴─────────────┘

  Admin Dashboard (Next.js) — 25 files

  ┌───────────────────────────────────────────┬─────────────┐
  │                   Page                    │   Status    │
  ├───────────────────────────────────────────┼─────────────┤
  │ Operations Overview (real-time metrics)   │ ✅ Complete │
  ├───────────────────────────────────────────┼─────────────┤
  │ Bookings (table, search, filter, assign)  │ ✅ Complete │
  ├───────────────────────────────────────────┼─────────────┤
  │ Mechanics network (grid, availability)    │ ✅ Complete │
  ├───────────────────────────────────────────┼─────────────┤
  │ Inventory (stock table, low-stock alerts) │ ✅ Complete │
  ├───────────────────────────────────────────┼─────────────┤
  │ Cash Reconciliation (verify payments)     │ ✅ Complete │
  ├───────────────────────────────────────────┼─────────────┤
  │ Tickets / Support                         │ ✅ Complete │
  └───────────────────────────────────────────┴─────────────┘

  ---
  BUGS TO FIX 🐛

  ┌─────┬─────────────────────────┬───────────────────────────────────────────────────────┬───────────────────────────────────────────────────┐   
  │  #  │          File           │                          Bug                          │                      Impact                       │   
  ├─────┼─────────────────────────┼───────────────────────────────────────────────────────┼───────────────────────────────────────────────────┤   
  │ 1   │ bookings/signals.py     │ Missing from authentication.models import User,       │ CRASH — loyalty points & referral bonuses break   │   
  │     │ line 1                  │ LoyaltyTransaction                                    │ on booking completion                             │   
  ├─────┼─────────────────────────┼───────────────────────────────────────────────────────┼───────────────────────────────────────────────────┤   
  │ 2   │ bookings/views.py line  │ Missing import logging + logger =                     │ CRASH — NameError when booking list or creation   │   
  │     │ 1                       │ logging.getLogger(__name__)                           │ fails                                             │   
  └─────┴─────────────────────────┴───────────────────────────────────────────────────────┴───────────────────────────────────────────────────┘   

  ---
  MISSING / INCOMPLETE 🔧

  ┌─────┬─────────────────────────────┬───────────────────────────────┬───────────────────────────────────────────────────────────────────────┐   
  │  #  │            Item             │           Location            │                                  Gap                                  │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 3   │ Promotions/Coupons          │ promotions/                   │ Models exist, no views or URLs                                        │   
  │     │ endpoints                   │                               │                                                                       │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 4   │ WhatsApp notifications      │ notifications/whatsapp.py     │ File exists but integration incomplete                                │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 5   │ Celery Beat schedule config │ settings.py                   │ process_subscription_renewals_task not scheduled in                   │   
  │     │                             │                               │ CELERY_BEAT_SCHEDULE                                                  │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 6   │ scenerio_based_design file  │ root                          │ File is empty — needs content                                         │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 7   │ Admin: no session/auth      │ repairmybike_admin            │ Any user can access dashboard with no login                           │   
  │     │ guard                       │                               │                                                                       │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 8   │ CORS restriction            │ settings.py                   │ CORS_ALLOW_ALL_ORIGINS = True — too open                              │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 9   │ DEBUG AllowAny on admin API │ admin_api/operations/views.py │ Unsafe permission pattern                                             │   
  ├─────┼─────────────────────────────┼───────────────────────────────┼───────────────────────────────────────────────────────────────────────┤   
  │ 10  │ Mechanic live GPS tracking  │ Flutter + backend             │ WebSocket endpoint exists; Flutter UI not connected                   │   
  └─────┴─────────────────────────────┴───────────────────────────────┴───────────────────────────────────────────────────────────────────────┘   

  ---
  BUILDING PLAN

  Phase 1 — Critical Bug Fixes (2 files, ~10 min)

  - Fix bookings/signals.py — add missing imports
  - Fix bookings/views.py — add logger

  Phase 2 — Security Hardening

  - Restrict CORS in settings.py
  - Remove DEBUG AllowAny pattern in admin_api
  - Add admin dashboard login/auth guard (Next.js middleware)

  Phase 3 — Missing Features

  - Promotions endpoints — views + URLs for coupon validation
  - Celery Beat schedule — register subscription renewal task
  - WhatsApp integration — complete notifications/whatsapp.py
  - scenerio_based_design — define and write content

  Phase 4 — Testing

  - Backend: pytest suite (bookings, payments, subscriptions, signals)
  - Backend: test the 2 bug-fixed signal handlers
  - Frontend: widget tests for booking flow
  - Admin: E2E test assign mechanic flow

  Phase 5 — Polish

  - Mechanic live GPS — connect Flutter UI to tracking WebSocket
  - Pagination on bookings API (admin dashboard)
  - Reconciled-today counter (currently hard-coded ₹42,850)
  - Ticket detail page (tickets list exists, no detail view)