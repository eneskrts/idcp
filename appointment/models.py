from django.db import models
from django.contrib.postgres.fields import ArrayField, DateTimeRangeField
import datetime
from psycopg2.extras import DateTimeTZRange
from .enums import StatusOption, DoctorsRequest
from django.contrib.auth import get_user_model


# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class Availability(BaseModel):
    available_time = DateTimeRangeField()
    reserved = models.BooleanField(default=0)
    available_user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name='available_user',
                                       null=False)

    def __str__(self):
        return self.available_user.username


class MeetingRoom(BaseModel):
    meeting_host = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="meeting_host")
    meeting_name = models.CharField(max_length=200, null=False)
    meeting_description = models.CharField(max_length=1000)

    attendees = models.ManyToManyField(to='auth.user', related_name="attendees", through="AppointmentRequest")

    meeting_url = models.CharField(max_length=1000)
    meeting_start_time = models.DateTimeField(null=False)

    meeting_status = models.CharField(choices=StatusOption.choices, default=StatusOption.ACTIVE, null=False,
                                      max_length=20)

    def __str__(self):
        return self.meeting_name


class AppointmentRequest(BaseModel):
    meeting = models.ForeignKey("appointment.MeetingRoom", on_delete=models.CASCADE, related_name="meeting_room")
    doctor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="doctor")

    doctor_request = models.CharField(choices=DoctorsRequest.choices, default=DoctorsRequest.WAITING, null=False,
                                      max_length=20)
    request_status = models.CharField(choices=StatusOption.choices, default=StatusOption.ACTIVE, max_length=20)
    explanation = models.CharField(max_length=500)

    def __str__(self):
        return str(self.meeting.meeting_name) + "-" + str(self.doctor.username)
