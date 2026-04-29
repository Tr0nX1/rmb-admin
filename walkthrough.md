# Walkthrough — FCM Push Notifications Implementation

I have successfully integrated Firebase Cloud Messaging (FCM) into the RepairMyBike ecosystem. This allows the backend to send real-time alerts to users which the app then displays.

## 1. Backend: The `notifications` App

I created a new Django app called `notifications` to handle everything related to push alerts.

- **Models**:
  - [FCMDevice](file:///d:/developer/repairmybike/repairmybike_backend/notifications/models.py#4-32): Stores device tokens for each user.
  - [NotificationLog](file:///d:/developer/repairmybike/repairmybike_backend/notifications/models.py#33-53): Keeps a history of all sent notifications for debugging.
- **Triggers**: I used Django signals to automatically fire notifications when:
  - A Booking status changes (e.g., `confirmed`, `completed`).
  - A Quick Service request status changes (e.g., `mechanic_dispatched`).
  - A Spare Part order is marked as `fulfilled` (shipped).
- **Core Logic**:
  - [send_push()](file:///d:/developer/repairmybike/repairmybike_backend/notifications/utils.py#30-86): A robust utility that sends messages to all active devices of a user and automatically deactivates stale tokens.

## 2. Frontend: Flutter Integration

The app is now equipped to receive and display notifications.

- **FcmService**: A new utility ([lib/utils/fcm_service.dart](file:///d:/developer/repairmybike/repairmybike_frontend/lib/utils/fcm_service.dart)) that manages:
  - Permission requests.
  - Fetching the FCM token.
  - Registering the token with the backend after a successful login.
  - Handling foreground, background, and terminated state messages.
- **Initialization**: Firebase and FCM are initialized in [main.dart](file:///d:/developer/repairmybike/repairmybike_frontend/lib/main.dart) before the app starts.

---

## 3. Important: Post-Implementation Steps

For push notifications to actually reach devices, you **must** add two configuration files that were intentionally omitted from git for security:

1. **Backend**: Place `firebase_credentials.json` in `repairmybike_backend/`.
2. **Frontend**: Place `google-services.json` in `repairmybike_frontend/android/app/`.

---

## 4. Verification

### Backend Registration
I've implemented the endpoint `POST /api/notifications/device/` for token registration. You can verify it's working by checking the Django Admin under **FCM Devices** after logging into the app.

### Sending a Test
You can test the pipeline via the Django shell:
```python
from notifications.utils import send_push
from authentication.models import User
u = User.objects.get(phone_number="+91XXXXXXXXXX")
send_push(u, "Hello! 👋", "Test notification from RepairMyBike")
```
