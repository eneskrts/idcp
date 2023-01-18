from rest_framework import serializers
from .models import Availability, MeetingRoom, AppointmentRequest
from .views import DateToHours, CheckAvailability, UpdateAppointmentRequest
from psycopg2.extras import DateTimeTZRange
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from zoneinfo import ZoneInfo


class AvailabilitySerializer(serializers.ModelSerializer):
    available_user_info = serializers.SerializerMethodField('_get_available_user')

    def _get_available_user(self, obj):
        user = obj.available_user
        data = {
            "User": {"id": user.id,
                     "name": user.first_name,
                     "surname": user.last_name,
                     "username": user.username,
                     "email": user.email}
        }
        return data

    available_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Availability
        fields = "__all__"

    def check_date(self, validated_data):
        time = validated_data["available_time"]
        now = timezone.now()

        if (time.upper.year != time.lower.year) or (time.upper.month != time.lower.month) or (
                time.upper.day != time.lower.day):
            error = {'message': "Saat aralığı farklı tarihlerde ve farklı günlerde olamaz", 'time': time}
            raise serializers.ValidationError(error)

        elif time.upper < now:
            error = {'messages': 'Geçmişte müsait olamazsınız', 'time': time}
            raise serializers.ValidationError(error)


        elif (time.upper.minute != 0) or (time.lower.minute != 0):
            error = {'messages': 'sadece Tam saatler girmelisiniz, dakika 00 olmalıdır ', 'time': time}
            raise serializers.ValidationError(error)

    def create(self, validated_data):
        time = validated_data["available_time"]

        self.check_date(validated_data)

        hours = DateToHours(time)
        for hour in hours:
            validated_data["available_time"] = DateTimeTZRange(hour, hour + datetime.timedelta(hours=1))
            new_time = super().create(validated_data)
        return new_time


class MeetingRoomSerializer(serializers.ModelSerializer):
    attendees_info = serializers.SerializerMethodField('_get_attendees_info')
    host_info = serializers.SerializerMethodField('_get_host_info')

    def _get_attendees_info(self, obj):
        data = {}
        users = obj.attendees.all()
        for user in users:
            user_data = {
                user.id: {"name": user.first_name,
                          "surname": user.last_name,
                          "username": user.username,
                          "email": user.email}
            }
            data.update(user_data)
        return data

    def _get_host_info(self, obj):
        user = obj.meeting_host
        data = {
            user.id: {"name": user.first_name,
                      "surname": user.last_name,
                      "username": user.username,
                      "email": user.email}
        }
        return data

    attendees = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, write_only=True)
    meeting_host = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    meeting_start_time = serializers.CharField()

    class Meta:
        model = MeetingRoom
        fields = "__all__"

    def create(self, validated_data):
        validated_data["meeting_start_time"] = validated_data["meeting_start_time"].replace(" ", "T")
        try:
            time = datetime.datetime.strptime(validated_data["meeting_start_time"], '%Y-%m-%dT%H:%M:%S') \
                .astimezone(tz=ZoneInfo("Turkey"))
            validated_data["meeting_start_time"] = time
        except:
            error = {
                'messages': 'Tarih "1999-09-09 12:00:00" formatında olmalıdır',
                'start_time': validated_data["meeting_start_time"]
            }
            raise serializers.ValidationError(error)

        now = timezone.now()

        if time < now:
            error = {'messages': 'Geçmişte Meeting düzenleyemezsiniz', 'time': time}
            raise serializers.ValidationError(error)

        elif time.minute != 0:
            error = {'messages': 'sadece Tam saatler girmelisiniz, dakika 00 olmalıdır ', 'time': time}
            raise serializers.ValidationError(error)

        time_range = DateTimeTZRange(time, time + datetime.timedelta(hours=1))
        check = CheckAvailability(time_range, validated_data["attendees"])

        # available time chek
        check = User.objects.filter(id__in=check[0].values_list("available_user"))

        if len(check) == len(validated_data["attendees"]):

            return super().create(validated_data)

        else:
            notIn = []
            for u in validated_data["attendees"]:
                if u not in check:
                    notIn.append(u.username)
            data = {
                'messages': "Tüm doktorlar müsait değil",
                'müsait_olmayan_doktorlar': notIn,
                'data': {
                    "attendees": validated_data["attendees"],
                    "meeting_host": validated_data["meeting_host"],
                    "meeting_name": validated_data["meeting_name"],
                    "meeting_description": validated_data["meeting_description"],
                    "meeting_url": validated_data["meeting_url"],
                    "meeting_start_time": validated_data["meeting_start_time"],
                    "meeting_status": validated_data["meeting_status"]
                }
            }
            raise serializers.ValidationError(data)


class AppointmentRequestSerializer(serializers.ModelSerializer):
    meeting_info = serializers.SerializerMethodField('_get_meeting_info')
    doctor_info = serializers.SerializerMethodField('_get_doctor_info')

    def _get_doctor_info(self, obj):
        user = obj.doctor
        data = {
            user.id: {"name": user.first_name,
                      "surname": user.last_name,
                      "username": user.username,
                      "email": user.email}
        }
        return data

    def _get_meeting_info(self, obj):
        meeting = obj.meeting
        data = {
            meeting.id: {"meeting_name": meeting.meeting_name,
                         "meeting_description": meeting.meeting_description,
                         "meeting_host": meeting.meeting_host.username,
                         "meeting_url": meeting.meeting_url,
                         "meeting_status": meeting.meeting_status
                         }
        }
        return data

    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    meeting = serializers.PrimaryKeyRelatedField(queryset=MeetingRoom.objects.all(), write_only=True)

    class Meta:
        model = AppointmentRequest
        fields = "__all__"

    def update(self, instance, validated_data):
        answer = validated_data["doctor_request"]
        instance = AppointmentRequest.objects.get(id=instance.id)
        UpdateAppointmentRequest(instance, answer)

        return instance
