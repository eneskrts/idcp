from django.db import models
import datetime

class StatusOption(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTİVE = "inactive", "Inactive"
        
        
class DoctorsRequest(models.TextChoices):
    ACCEPTED = "accepted", "Accepted"
    WAITING = "waiting", "Waiting"
    REJECTED = "rejected", "Rejected"
        
