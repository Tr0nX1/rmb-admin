import os
import django
import sys
from pathlib import Path

# Add the project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent / 'repairmybike_backend'
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'repairmybike.settings')
django.setup()

from notifications.utils import send_push_notification
from authentication.models import User
from notifications.models import FCMDevice

def send_test_push():
    print("🚀 Starting FCM Push Notification Test...")
    
    # 1. Get or Create a test user
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_user(username='testpushuser', password='password123', phone_number='+919999999999')
    
    print(f"👤 Using User: {user.username} ({user.phone_number})")

    # 2. Register a dummy device
    dummy_token = "fcm_dummy_token_1234567890_this_will_fail_delivery_but_verify_sdk"
    device, created = FCMDevice.objects.update_or_create(
        token=dummy_token,
        defaults={
            'user': user,
            'platform': 'android',
            'is_active': True
        }
    )
    print(f"📱 Device registered: {device.token[:20]}... (Created: {created})")

    # 3. Send Push
    print("✉️ Sending Multicast Message...")
    success = send_push_notification(
        user=user,
        title="Test from Antigravity",
        body="If you see this, the SDK is working!",
        data={'test': 'true', 'type': 'test'}
    )

    if success:
        print("✅ Push notification logic executed successfully (Check logs for delivery status).")
    else:
        print("❌ Push notification logic failed.")

if __name__ == "__main__":
    send_test_push()
