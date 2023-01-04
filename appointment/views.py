from django.shortcuts import render
import datetime
from .models import Availability, AppointmentRequest, MeetingRoom
from django.contrib.auth.models import User
from psycopg2.extras import DateTimeTZRange, DateTimeRange
from django.utils import timezone
from zoneinfo import ZoneInfo 

# Create your views here.

def DateToHours(time):
    hours = []
    
    end_time = time.upper
    start_time = time.lower
    i=0
    a=(end_time-start_time).total_seconds()/3600
    
    while i<a:
        hour = start_time + datetime.timedelta(hours=i)
        hours.append(hour)
        i+=1
            
    return hours



# users type = User objects, meeting type = MeetingRoom objects
def SendMeetingRequests(users, meeting):
    
    for user in users:
        AppointmentRequest.objects.create(meeting=meeting, doctor=user)
        
        
# meeting_times type = DataTimeRange
# attendees type = User objects
def CheckAvailability(meeting_times,attendees):
    users = []
    hours = DateToHours(meeting_times)
    
    for hour in hours:
        
        available_users = Availability.objects.filter(available_user__in=attendees,available_time__contained_by=DateTimeTZRange(hour,hour+datetime.timedelta(hours=1)),reserved=0)
        users.append(available_users)
        
    return users


#user = User.objects.get
#avaiable_tme_list = dateTimeTZRange
def CreateAvailability(user,available_times):
        available_hours = DateToHours(available_times)
        
        for available_hour in available_hours:
            time = DateTimeTZRange(available_hour,available_hour+datetime.timedelta(hours=1))
            Availability.objects.create(available_user=user, available_time=time)
            

#appointment_request = AppointmentRequest object
#answer = str choices(accepted,waiting,rejected)
def UpdateAppointmentRequest(appointment_request,answer):
    now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
    
    if appointment_request.meeting.meeting_start_time < now:
        return False
    
    appointment_request.doctor_request = answer
    appointment_request.save()
    time = appointment_request.meeting.meeting_start_time
    
    availability = Availability.objects.get(available_user=appointment_request.doctor,available_time=DateTimeTZRange(time,time+datetime.timedelta(hours=1)))
    if answer == 'accepted':
        availability.reserved = 1
    
        # Kabul edilen istek toplantısı ile aynı saattaki istekler reddediliyor
        all_requests= AppointmentRequest.objects.filter(meeting__meeting_start_time=time, doctor=appointment_request.doctor)
        for a in all_requests:
            if a.id != appointment_request.id:
                a.doctor_request='rejected'
                a.save()
                
    else:
        availability.reserved = 0
        
    availability.save()
    
    
    
# Filterset
from django_filters import FilterSet, DateTimeFromToRangeFilter, rest_framework as filters
from django_filters.widgets import RangeWidget


class AvailableFilter(FilterSet):
    available_time = DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'type':'datetime-local'}))

    class Meta:
        model = Availability
        fields = ["available_user","available_time"]
        
        
    def filter_queryset(self, queryset):
        if self.data:
            if self.data["available_user"]:
                user = self.data["available_user"]
                queryset = queryset.filter(available_user=user)
            
            if self.data['available_time_max'] and self.data['available_time_min']:
                available_time_max = datetime.datetime.strptime(self.data['available_time_max'],'%Y-%m-%dT%H:%M').astimezone(tz=ZoneInfo("Turkey"))
                available_time_min = datetime.datetime.strptime(self.data['available_time_min'],'%Y-%m-%dT%H:%M').astimezone(tz=ZoneInfo("Turkey"))
                time = DateTimeTZRange(available_time_min,available_time_max)
                queryset = queryset.filter(available_time__contained_by=time)
            
            return queryset
        
        return queryset
    
    
class MeetingRoomFilter(FilterSet):
    class Meta:
        model = MeetingRoom
        fields = ["meeting_host","attendees"]


class AppointmentRequestFilter(FilterSet):
    class Meta:
        model = AppointmentRequest
        fields = ["doctor","meeting"]



    
            
#API
from rest_framework import viewsets
from .serializers import AvailabilitySerializer,  MeetingRoomSerializer, AppointmentRequestSerializer
from rest_framework.viewsets import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

class AvailabilityViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    
    queryset=Availability.objects.all()
    serializer_class=AvailabilitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AvailableFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for query in queryset:
            show_upper = query.available_time.upper.astimezone(tz=ZoneInfo("Turkey"))
            show_lower = query.available_time.lower.astimezone(tz=ZoneInfo("Turkey"))
            show_time = DateTimeTZRange(show_lower,show_upper)
            query.available_time = show_time

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        show_upper = instance.available_time.upper.astimezone(tz=ZoneInfo("Turkey"))
        show_lower = instance.available_time.lower.astimezone(tz=ZoneInfo("Turkey"))
        show_time = DateTimeTZRange(show_lower,show_upper)
        instance.d = show_time
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
    
class MeetingRoomViewSet(viewsets.ModelViewSet):
    
    queryset=MeetingRoom.objects.all()
    serializer_class=MeetingRoomSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MeetingRoomFilter

    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        for meeting_room in queryset:
            show_time =meeting_room.meeting_start_time.astimezone(tz=ZoneInfo("Turkey"))
            meeting_room.meeting_start_time = show_time
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        show_time = instance.meeting_start_time.astimezone(tz=ZoneInfo("Turkey"))
        instance.meeting_start_time = show_time
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
        
class AppointmentRequestViewSet(viewsets.ModelViewSet):
    
    queryset=AppointmentRequest.objects.all()
    serializer_class=AppointmentRequestSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AppointmentRequestFilter
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        for meeting_room in queryset:
            show_time =meeting_room.meeting.meeting_start_time.astimezone(tz=ZoneInfo("Turkey"))
            meeting_room.meeting.meeting_start_time = show_time
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        show_time = instance.meeting.meeting_start_time.astimezone(tz=ZoneInfo("Turkey"))
        instance.meeting.meeting_start_time = show_time
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
