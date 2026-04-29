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

def send_live_test():
    username = 'admin'
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"❌ User {username} not found!")
        return

    print(f"🚀 Sending live notification to {username}...")
    success = send_push_notification(
        user=user,
        title="Hello from RepairMyBike!",
        body="This is a live test of your push notification system. It's working!",
        data={'test': 'true', 'type': 'test_push'}
    )

    if success:
        print("✅ Notification sent! Please check your device/emulator.")
    else:
        print("❌ Failed to send notification. Check backend logs.")

if __name__ == "__main__":
    send_live_test()
