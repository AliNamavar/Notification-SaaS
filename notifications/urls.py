from django.urls import path
from .views import SentNotifications, Notification_filter

urlpatterns = [
    path('api/notifications/send/', SentNotifications.as_view(), name='senf_notifications'),
    path('api/notifications/', Notification_filter.as_view(), name='notifications_status'),
    path('api/notifications/<uuid:request_id>/', Notification_filter.as_view(), name='notification_status_filter')
]