from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _

class StatusOption(models.TextChoices):
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
        
        
class DoctorsRequest(models.TextChoices):
    ACCEPTED = "accepted", _("Accepted")
    WAITING = "waiting", _("Waiting")
    REJECTED = "rejected", _("Rejected")
        
