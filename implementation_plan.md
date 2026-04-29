# FCM Push Notifications — Implementation Plan

Implement end-to-end Firebase Cloud Messaging (FCM) push notifications for the RepairMyBike app. The backend stores device tokens, sends notifications on key business events (booking confirmed, mechanic dispatched, order shipped, etc.), and Flutter handles permission, token registration, and display.

## User Review Required

> [!IMPORTANT]
> **You must provide the Firebase service account JSON file** for the backend.
> 1. Go to [Firebase Console](https://console.firebase.google.com/) → Your Project → Project Settings → Service Accounts
> 2. Click "Generate new private key" → download the JSON file
> 3. Place it at: `repairmybike_backend/firebase_credentials.json`
> 4. Set env var: `FIREBASE_CREDENTIALS_PATH=firebase_credentials.json`

> [!IMPORTANT]
> **You must provide `google-services.json` for Android.**
> 1. Firebase Console → Project Settings → Your Android App (`com.repairmybike`)
> 2. Download `google-services.json`
> 3. Place it at: `repairmybike_frontend/android/app/google-services.json`

> [!NOTE]
> The `google-services.json` and `firebase_credentials.json` files must **NEVER be committed to git**. They are already in [.gitignore](file:///d:/developer/repairmybike/repairmybike_backend/.gitignore) pattern, but double-check.

---

## Proposed Changes

### Backend — New `notifications` App

#### [NEW] notifications/models.py
- `FCMDevice` — stores one token per user+platform. Fields: `user (FK)`, `token (text, unique)`, `platform (android/ios/web)`, `is_active (bool)`, `created_at`, `updated_at`
- `NotificationLog` — history of every notification sent. Fields: `user (FK, nullable)`, `title`, `body`, `data (JSONField)`, `fcm_response`, `sent_at`

#### [NEW] notifications/utils.py
- `init_firebase_app()` — initializes Firebase Admin SDK once (called in [apps.py](file:///d:/developer/repairmybike/repairmybike_backend/staff/apps.py))
- `send_push(user, title, body, data={})` — fetches all active tokens for user, calls `firebase_admin.messaging.send_each()`, logs result to `NotificationLog`, handles `UnregisteredError` by deactivating stale tokens
- Individual helper functions (called from signals/views):
  - `notify_booking_confirmed(booking)`
  - `notify_booking_status_changed(booking, old_status)`
  - `notify_order_shipped(order)`
  - `notify_quick_service_update(qs_request)`

#### [NEW] notifications/views.py
- `RegisterDeviceView (POST /api/notifications/device/)` — authenticated users only, upserts FCMDevice for the current user with the given token + platform
- `UnregisterDeviceView (DELETE /api/notifications/device/)` — deactivates the token on logout

#### [NEW] notifications/urls.py
```
POST   /api/notifications/device/     → register token
DELETE /api/notifications/device/     → unregister token
```

#### [NEW] notifications/apps.py
- `ready()` — calls `init_firebase_app()` on startup

#### [NEW] notifications/admin.py
- Register `FCMDevice` and `NotificationLog` for Django Admin visibility

---

### Backend — Wire Into Existing Apps

#### [MODIFY] bookings/views.py
- After `booking_status` is updated → call `notify_booking_status_changed(booking, old_status)`

#### [MODIFY] quick_service/views.py
- After [QuickServiceRequest](file:///d:/developer/repairmybike/repairmybike_backend/quick_service/models.py#19-43) status changes → call `notify_quick_service_update(qs_request)`

#### [MODIFY] spare_parts/views.py
- After `Order.status` changes to `fulfilled` → call `notify_order_shipped(order)`

#### [MODIFY] repairmybike/settings.py
- Add `'notifications'` to `INSTALLED_APPS`
- Add `FIREBASE_CREDENTIALS_PATH = config('FIREBASE_CREDENTIALS_PATH', default='firebase_credentials.json')`

#### [MODIFY] repairmybike/urls.py
- Add `path('api/notifications/', include('notifications.urls'))`

#### [MODIFY] requirements.txt
- Add `firebase-admin==6.5.0`

---

### Frontend (Flutter)

#### [MODIFY] pubspec.yaml
Add dependencies:
```yaml
firebase_core: ^3.6.0
firebase_messaging: ^15.1.3
flutter_local_notifications: ^17.2.3
```

#### [NEW] lib/utils/fcm_service.dart
- `FcmService` class with:
  - `initialize()` — call `Firebase.initializeApp()`, request permissions, set foreground notification options
  - `getToken()` → `String?` — returns the FCM token
  - `registerTokenWithBackend(token)` — POST to `/api/notifications/device/`
  - `setupMessageHandlers()` — handles `onMessage` (foreground), `onMessageOpenedApp` (tap from background), `getInitialMessage` (tap from terminated)
  - `_handleNotificationTap(message)` — reads `data.type` and navigates to the right page (booking, order, quick_service)
- Top-level `@pragma('vm:entry-point') firebaseMessagingBackgroundHandler()` — required by FCM for terminated state

#### [MODIFY] lib/main.dart
- Make [main()](file:///d:/developer/repairmybike/repairmybike_frontend/lib/main.dart#8-14) async
- Call `WidgetsFlutterBinding.ensureInitialized()` (already present)
- Call `await Firebase.initializeApp()` before `runApp()`
- Register `FirebaseMessaging.onBackgroundMessage(firebaseMessagingBackgroundHandler)`

#### [MODIFY] lib/data/app_state.dart (or auth flow)
- After successful login → call `FcmService().getToken()` + `FcmService().registerTokenWithBackend(token)`
- On logout → DELETE `/api/notifications/device/` to unregister

---

## Verification Plan

### Manual Verification Steps

**Step 1 — Backend device registration**
```bash
# After logging in and getting a session token:
curl -X POST https://repairmybikebackend-production.up.railway.app/api/notifications/device/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"token": "test_fcm_token_123", "platform": "android"}'
# Expected: 201 Created with {"message": "Device registered"}
```

**Step 2 — Send test notification from Django shell**
```bash
cd repairmybike_backend
python manage.py shell
>>> from notifications.utils import send_push
>>> from authentication.models import User
>>> u = User.objects.first()
>>> send_push(u, "Test 🔔", "This is a test notification", {"type": "test"})
# Expected: FCM returns success response, NotificationLog entry created
```

**Step 3 — End-to-end booking notification**
1. Open the app on a real Android device (emulators may not receive FCM)
2. Create a new booking via the app
3. In Django Admin → Bookings → change status to `confirmed`
4. Expected: Device receives notification "Booking Confirmed ✅"

**Step 4 — Background notification**
1. Close the app completely (remove from recents)
2. Trigger a booking status change from admin
3. Expected: Notification appears in status bar, tapping it opens the app to booking details
