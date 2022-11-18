from django.db import models
from django.contrib.postgres.fields import ArrayField,DateTimeRangeField
from .enums import SessionTimeSlots
import datetime
from psycopg2.extras import DateTimeTZRange
# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        abstract = True
class Availability(BaseModel):
    
    available_time=DateTimeRangeField()
    available_user=models.ForeignKey(to='auth.User', on_delete=models.DO_NOTHING, related_name='available_user',null=False)

    
    
