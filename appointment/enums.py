from django.db import models
import datetime

class MeetingStatusOption(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTİVE = "inactive", "Inactive"
        
        
class DoctorsRequest(models.TextChoices):
    ACCEPTED = "accepted", "Accepted"
    WAITING = "waiting", "Waiting"
    REJECTED = "rejected", "Rejected"
        
        
class birthdate(models.TextChoices):
    boş="now",datetime.datetime.now
    