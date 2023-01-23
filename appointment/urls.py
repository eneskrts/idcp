from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
# router.register(r'availability',views.AvailabilityViewSet)
# router.register(r'meeting-room',views.MeetingRoomViewSet)
# router.register(r'appointment-request',views.AppointmentRequestViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
