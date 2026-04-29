# Final Approach: Operations Command Center Upgrade

## Executive Summary
Transform your Django dashboard into a **real-time operations hub** using Django Channels + HTMX, optimized for your cash-only bike repair business.

---

## Phase 1: Real-Time Foundation (Week 1)

### Backend Core

#### 1. Install Dependencies
```bash
pip install channels channels-redis django-auditlog
```

#### 2. Update `settings.py`
```python
INSTALLED_APPS = [
    'daphne',  # Add at the top
    'channels',
    'auditlog',
    # ... your existing apps
]

ASGI_APPLICATION = 'repairmybike_backend.asgi.application'

# Redis Channel Layer (required for 5+ concurrent staff)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# Audit logging
AUDITLOG_INCLUDE_ALL_MODELS = False  # We'll register models manually
```

#### 3. Create `dashboard/signals.py`
```python
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from auditlog.registry import auditlog
from .models import Booking, Order

channel_layer = get_channel_layer()

def broadcast_to_dashboard(event_type, data):
    """Central broadcast function"""
    async_to_sync(channel_layer.group_send)(
        'dashboard_notifications',
        {
            'type': 'dashboard_update',
            'event': event_type,
            'data': data
        }
    )

@receiver(post_save, sender=Booking)
def booking_update_handler(sender, instance, created, **kwargs):
    event_type = 'booking_created' if created else 'booking_updated'
    
    broadcast_to_dashboard(event_type, {
        'id': instance.id,
        'customer_name': instance.customer_name,
        'service': instance.service_type,
        'status': instance.status,
        'mechanic': instance.mechanic.name if instance.mechanic else None,
        'assigned_by': instance.assigned_by.username if instance.assigned_by else None,
        'timestamp': instance.created_at.isoformat(),
        'cash_collected': instance.cash_collected
    })
    
    # Auto-notify mechanic via WhatsApp if assigned
    if instance.mechanic and instance.status == 'assigned':
        send_mechanic_notification(instance)

@receiver(post_save, sender=Order)
def order_update_handler(sender, instance, created, **kwargs):
    if created:
        broadcast_to_dashboard('order_created', {
            'id': instance.id,
            'customer': instance.customer_name,
            'items': instance.items_count,
            'status': instance.status,
            'timestamp': instance.created_at.isoformat()
        })

def send_mechanic_notification(booking):
    """Integration with your Kapso WhatsApp skill"""
    # TODO: Connect to your existing WhatsApp service
    message = f"""
🔧 New Assignment!
Booking ID: {booking.id}
Customer: {booking.customer_name}
Service: {booking.service_type}
Address: {booking.customer_address}
Phone: {booking.customer_phone}
"""
    # kapso_send_whatsapp(booking.mechanic.phone, message)
    pass

# Register models for audit logging
auditlog.register(Booking, exclude_fields=['updated_at'])
auditlog.register(Order, exclude_fields=['updated_at'])
```

#### 4. Update `dashboard/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    # ... your existing fields ...
    
    # NEW FIELDS for cash reconciliation
    cash_collected = models.BooleanField(default=False)
    cash_collected_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='cash_collections'
    )
    cash_collected_at = models.DateTimeField(null=True, blank=True)
    
    # NEW FIELDS for conflict prevention
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignments'
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'cash_collected']),
            models.Index(fields=['created_at']),
        ]
```

#### 5. Update `dashboard/consumers.py`
```python
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join dashboard notification group
        await self.channel_layer.group_add(
            'dashboard_notifications',
            self.channel_name
        )
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Real-time updates active'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'dashboard_notifications',
            self.channel_name
        )

    async def dashboard_update(self, event):
        """Handle broadcasts from signals"""
        await self.send(text_data=json.dumps({
            'type': event['event'],
            'data': event['data']
        }))
```

#### 6. Update `dashboard/routing.py`
```python
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
]
```

#### 7. Create Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Phase 2: Frontend Real-Time (Week 1)

### Update `dashboard/templates/dashboard/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Operations Command Center</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://unpkg.com/htmx.org/dist/ext/ws.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        .toast {
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .pulse-dot {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: .5; }
        }
    </style>
</head>
<body class="bg-gray-50" x-data="dashboardApp()">
    
    <!-- Connection Status -->
    <div class="fixed top-4 right-4 z-50 flex items-center gap-2 bg-white px-4 py-2 rounded-lg shadow">
        <span class="pulse-dot w-2 h-2 rounded-full" :class="connected ? 'bg-green-500' : 'bg-red-500'"></span>
        <span class="text-sm" x-text="connected ? 'Live' : 'Connecting...'"></span>
    </div>

    <!-- Toast Notifications -->
    <div class="fixed top-20 right-4 z-40 space-y-2" id="toast-container">
        <template x-for="toast in toasts" :key="toast.id">
            <div class="toast bg-white px-6 py-4 rounded-lg shadow-lg border-l-4" 
                 :class="toast.type === 'booking' ? 'border-blue-500' : 'border-green-500'">
                <div class="flex items-start gap-3">
                    <span class="text-2xl" x-text="toast.type === 'booking' ? '🔧' : '📦'"></span>
                    <div>
                        <p class="font-semibold" x-text="toast.title"></p>
                        <p class="text-sm text-gray-600" x-text="toast.message"></p>
                    </div>
                </div>
            </div>
        </template>
    </div>

    <div class="container mx-auto p-6">
        
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">Operations Command Center</h1>
            <p class="text-gray-600">Real-time tracking for {{ user.get_full_name }}</p>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white p-6 rounded-lg shadow">
                <div class="text-sm text-gray-600">Active Bookings</div>
                <div class="text-3xl font-bold" x-text="stats.active_bookings">0</div>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
                <div class="text-sm text-gray-600">Pending Assignment</div>
                <div class="text-3xl font-bold text-orange-500" x-text="stats.pending_assignment">0</div>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
                <div class="text-sm text-gray-600">Cash Pending</div>
                <div class="text-3xl font-bold text-red-500" x-text="stats.cash_pending">0</div>
            </div>
            <div class="bg-white p-6 rounded-lg shadow">
                <div class="text-sm text-gray-600">Today's Revenue</div>
                <div class="text-3xl font-bold text-green-500">₹<span x-text="stats.revenue">0</span></div>
            </div>
        </div>

        <!-- Quick Search -->
        <div class="mb-6">
            <input 
                type="text" 
                x-model="searchQuery"
                @input="filterBookings()"
                placeholder="Search bookings by customer name, phone, or booking ID..."
                class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
        </div>

        <!-- Tabs -->
        <div class="mb-6 border-b border-gray-200">
            <nav class="flex gap-8">
                <button 
                    @click="activeTab = 'bookings'"
                    :class="activeTab === 'bookings' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500'"
                    class="py-4 px-1 border-b-2 font-medium">
                    Bookings
                </button>
                <button 
                    @click="activeTab = 'orders'"
                    :class="activeTab === 'orders' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500'"
                    class="py-4 px-1 border-b-2 font-medium">
                    Spare Parts Orders
                </button>
                <button 
                    @click="activeTab = 'cash'"
                    :class="activeTab === 'cash' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500'"
                    class="py-4 px-1 border-b-2 font-medium">
                    Cash Reconciliation
                </button>
            </nav>
        </div>

        <!-- Bookings Tab -->
        <div x-show="activeTab === 'bookings'" id="bookings-container">
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Service</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Mechanic</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cash</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200" id="bookings-list">
                        {% for booking in recent_bookings %}
                        <tr data-booking-id="{{ booking.id }}" class="hover:bg-gray-50">
                            <td class="px-6 py-4 whitespace-nowrap text-sm">#{{ booking.id }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">{{ booking.customer_name }}</div>
                                <div class="text-sm text-gray-500">{{ booking.customer_phone }}</div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm">{{ booking.service_type }}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                                    {% if booking.status == 'pending' %}bg-yellow-100 text-yellow-800
                                    {% elif booking.status == 'assigned' %}bg-blue-100 text-blue-800
                                    {% elif booking.status == 'completed' %}bg-green-100 text-green-800
                                    {% else %}bg-gray-100 text-gray-800{% endif %}">
                                    {{ booking.status }}
                                </span>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm">
                                {{ booking.mechanic.name|default:"Unassigned" }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                {% if booking.cash_collected %}
                                    <span class="text-green-600">✓ Collected</span>
                                {% else %}
                                    <span class="text-red-600">⏳ Pending</span>
                                {% endif %}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm">
                                {% if not booking.mechanic %}
                                <button 
                                    @click="openAssignModal({{ booking.id }})"
                                    class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded">
                                    Assign
                                </button>
                                {% endif %}
                                {% if booking.status == 'completed' and not booking.cash_collected %}
                                <button 
                                    @click="markCashCollected({{ booking.id }})"
                                    class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded">
                                    Collect Cash
                                </button>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Cash Reconciliation Tab -->
        <div x-show="activeTab === 'cash'">
            <div class="bg-white rounded-lg shadow p-6">
                <h3 class="text-lg font-semibold mb-4">Pending Cash Collections</h3>
                <div class="space-y-3">
                    {% for booking in cash_pending_bookings %}
                    <div class="flex items-center justify-between p-4 bg-gray-50 rounded">
                        <div>
                            <span class="font-semibold">#{{ booking.id }}</span> - {{ booking.customer_name }}
                            <span class="text-gray-600">₹{{ booking.total_amount }}</span>
                        </div>
                        <button 
                            @click="markCashCollected({{ booking.id }})"
                            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
                            Mark Collected
                        </button>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>

    </div>

    <!-- Assignment Modal -->
    <div x-show="showAssignModal" 
         x-cloak
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
         @click.self="showAssignModal = false">
        <div class="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 class="text-xl font-semibold mb-4">Assign Mechanic</h3>
            <div class="space-y-3 mb-6">
                <template x-for="mechanic in availableMechanics" :key="mechanic.id">
                    <button 
                        @click="assignMechanic(mechanic.id)"
                        class="w-full text-left p-4 border rounded hover:bg-blue-50 hover:border-blue-500 transition">
                        <div class="font-semibold" x-text="mechanic.name"></div>
                        <div class="text-sm text-gray-600" x-text="mechanic.active_bookings + ' active jobs'"></div>
                    </button>
                </template>
            </div>
            <button 
                @click="showAssignModal = false"
                class="w-full bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded">
                Cancel
            </button>
        </div>
    </div>

    <script>
        function dashboardApp() {
            return {
                connected: false,
                activeTab: 'bookings',
                searchQuery: '',
                showAssignModal: false,
                selectedBookingId: null,
                toasts: [],
                stats: {
                    active_bookings: {{ stats.active_bookings|default:0 }},
                    pending_assignment: {{ stats.pending_assignment|default:0 }},
                    cash_pending: {{ stats.cash_pending|default:0 }},
                    revenue: {{ stats.revenue|default:0 }}
                },
                availableMechanics: {{ mechanics_json|safe }},
                
                init() {
                    this.connectWebSocket();
                    this.playSound('connect');
                },
                
                connectWebSocket() {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    const ws = new WebSocket(`${protocol}//${window.location.host}/ws/dashboard/`);
                    
                    ws.onopen = () => {
                        this.connected = true;
                        console.log('WebSocket connected');
                    };
                    
                    ws.onclose = () => {
                        this.connected = false;
                        console.log('WebSocket disconnected, reconnecting...');
                        setTimeout(() => this.connectWebSocket(), 3000);
                    };
                    
                    ws.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        this.handleWebSocketMessage(data);
                    };
                },
                
                handleWebSocketMessage(data) {
                    console.log('Received:', data);
                    
                    if (data.type === 'booking_created') {
                        this.addNewBooking(data.data);
                        this.showToast('booking', 'New Booking', `#${data.data.id} - ${data.data.customer_name}`);
                        this.playSound('new_booking');
                        this.updateStats();
                    } else if (data.type === 'booking_updated') {
                        this.updateBooking(data.data);
                        this.updateStats();
                    }
                },
                
                addNewBooking(booking) {
                    const tableBody = document.getElementById('bookings-list');
                    const row = this.createBookingRow(booking);
                    tableBody.insertAdjacentHTML('afterbegin', row);
                },
                
                updateBooking(booking) {
                    const row = document.querySelector(`tr[data-booking-id="${booking.id}"]`);
                    if (row) {
                        // Update status, mechanic, etc.
                        row.querySelector('.status-badge').textContent = booking.status;
                    }
                },
                
                showToast(type, title, message) {
                    const toast = {
                        id: Date.now(),
                        type,
                        title,
                        message
                    };
                    this.toasts.push(toast);
                    setTimeout(() => {
                        this.toasts = this.toasts.filter(t => t.id !== toast.id);
                    }, 5000);
                },
                
                playSound(type) {
                    // Optional: Add audio notifications
                    const sounds = {
                        'new_booking': '/static/sounds/notification.mp3',
                        'connect': '/static/sounds/connect.mp3'
                    };
                    if (sounds[type]) {
                        new Audio(sounds[type]).play().catch(() => {});
                    }
                },
                
                openAssignModal(bookingId) {
                    this.selectedBookingId = bookingId;
                    this.showAssignModal = true;
                },
                
                async assignMechanic(mechanicId) {
                    const response = await fetch(`/api/bookings/${this.selectedBookingId}/assign/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': '{{ csrf_token }}'
                        },
                        body: JSON.stringify({ mechanic_id: mechanicId })
                    });
                    
                    if (response.ok) {
                        this.showAssignModal = false;
                        this.showToast('booking', 'Assigned', 'Mechanic assigned successfully');
                    }
                },
                
                async markCashCollected(bookingId) {
                    if (!confirm('Confirm cash collection?')) return;
                    
                    const response = await fetch(`/api/bookings/${bookingId}/collect-cash/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': '{{ csrf_token }}'
                        }
                    });
                    
                    if (response.ok) {
                        this.showToast('booking', 'Cash Collected', `Booking #${bookingId}`);
                        location.reload(); // Temporary - will be replaced with live update
                    }
                },
                
                filterBookings() {
                    // Client-side filtering logic
                    const query = this.searchQuery.toLowerCase();
                    document.querySelectorAll('#bookings-list tr').forEach(row => {
                        const text = row.textContent.toLowerCase();
                        row.style.display = text.includes(query) ? '' : 'none';
                    });
                },
                
                updateStats() {
                    // Fetch updated stats via API
                    fetch('/api/dashboard/stats/')
                        .then(r => r.json())
                        .then(data => this.stats = data);
                }
            }
        }
    </script>

</body>
</html>
```

---

## Phase 3: API Endpoints (Week 2)

### Create `dashboard/api_views.py`

```python
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking, Mechanic

@login_required
@require_POST
def assign_mechanic(request, booking_id):
    """Assign mechanic to booking with conflict detection"""
    booking = Booking.objects.select_for_update().get(id=booking_id)
    mechanic_id = request.POST.get('mechanic_id')
    
    # Conflict detection
    if booking.mechanic:
        if booking.assigned_at and (timezone.now() - booking.assigned_at).seconds < 10:
            return JsonResponse({
                'error': f'Already assigned by {booking.assigned_by.username} just now'
            }, status=409)
    
    mechanic = Mechanic.objects.get(id=mechanic_id)
    booking.mechanic = mechanic
    booking.status = 'assigned'
    booking.assigned_by = request.user
    booking.assigned_at = timezone.now()
    booking.save()
    
    return JsonResponse({'success': True})

@login_required
@require_POST
def collect_cash(request, booking_id):
    """Mark cash as collected"""
    booking = Booking.objects.get(id=booking_id)
    
    if booking.status != 'completed':
        return JsonResponse({'error': 'Booking not completed'}, status=400)
    
    booking.cash_collected = True
    booking.cash_collected_by = request.user
    booking.cash_collected_at = timezone.now()
    booking.save()
    
    return JsonResponse({'success': True})

@login_required
def dashboard_stats(request):
    """Real-time stats for dashboard"""
    from django.db.models import Sum, Q
    
    stats = {
        'active_bookings': Booking.objects.filter(
            status__in=['pending', 'assigned', 'in_progress']
        ).count(),
        'pending_assignment': Booking.objects.filter(
            status='pending', 
            mechanic__isnull=True
        ).count(),
        'cash_pending': Booking.objects.filter(
            status='completed',
            cash_collected=False
        ).count(),
        'revenue': Booking.objects.filter(
            created_at__date=timezone.now().date(),
            cash_collected=True
        ).aggregate(total=Sum('total_amount'))['total'] or 0
    }
    
    return JsonResponse(stats)
```

### Update `dashboard/urls.py`

```python
from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.dashboard_index, name='dashboard'),
    
    # API endpoints
    path('api/bookings/<int:booking_id>/assign/', api_views.assign_mechanic),
    path('api/bookings/<int:booking_id>/collect-cash/', api_views.collect_cash),
    path('api/dashboard/stats/', api_views.dashboard_stats),
]
```

---

## Phase 4: Deployment Checklist

### 1. Install Redis
```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

### 2. Update `requirements.txt`
```
channels==4.0.0
channels-redis==4.1.0
django-auditlog==2.3.0
daphne==4.0.0
```

### 3. Run Daphne (ASGI Server)
```bash
# Development
daphne -b 0.0.0.0 -p 8000 repairmybike_backend.asgi:application

# Production (with systemd)
# Create /etc/systemd/system/daphne.service
```

### 4. Nginx Configuration
```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://django;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws/ {
        proxy_pass http://django;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Testing Plan

### Manual Tests
1. **WebSocket Connection**
   - Open dashboard in 2 browser windows
   - Create booking via API/admin
   - Verify both windows receive notification

2. **Cash Flow**
   - Create booking → Assign → Mark completed
   - Verify "Collect Cash" button appears
   - Click button → Verify audit log entry

3. **Conflict Detection**
   - Open assignment modal in 2 windows simultaneously
   - Assign different mechanics
   - Verify second assignment shows conflict warning

### Automated Tests
```python
# dashboard/tests.py
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from .consumers import DashboardConsumer

class WebSocketTests(TestCase):
    async def test_broadcast_on_booking_create(self):
        communicator = WebsocketCommunicator(DashboardConsumer.as_asgi(), "/ws/dashboard/")
        connected, _ = await communicator.connect()
        assert connected
        
        # Create booking (triggers signal)
        Booking.objects.create(customer_name="Test", service_type="Repair")
        
        # Verify websocket receives message
        response = await communicator.receive_json_from()
        assert response['type'] == 'booking_created'
        
        await communicator.disconnect()
```

---

## Performance Expectations

| Metric | Target |
|--------|--------|
| WebSocket latency | < 100ms |
| Page load | < 2 seconds |
| Concurrent staff | 50+ (with Redis) |
| Real-time updates | < 500ms |

---

## Future Enhancements (Phase 4+)

1. **Mechanic Mobile App** - React Native app for mechanics to update status
2. **Google Maps Integration** - Show mechanic locations in real-time
3. **Cash Deposit Photos** - Require photo upload for cash reconciliation
4. **Analytics Dashboard** - Manager view with charts (Chart.js)
5. **WhatsApp Bot** - Two-way communication with customers

---

## Open Questions - Need Your Input

1. **How many staff members use dashboard concurrently?** (For Redis sizing)
2. **Do you have WhatsApp Business API credentials?** (For auto-notifications)
3. **What's your Redis hosting preference?** (Local, AWS ElastiCache, Redis Cloud)
4. **Cash reconciliation - do you want photo uploads now or later?**

---

**Ready to implement? Reply with:**
- Your concurrent staff count
- WhatsApp integration preference (yes/no)
- Start date

I'll begin with Phase 1 backend setup immediately upon confirmation.