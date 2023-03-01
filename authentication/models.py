import datetime
from django.db import models
from django.core.validators import EmailValidator, FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
import pytz
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

year_choices = []
for r in range(1980, (datetime.datetime.now().year+1)):
    year_choices.append((r,r))

def avatar_upload(instance, filename):
    new_filename = '{}_{}.{}'.format('user',instance.pk, 'png')
    return "user_avatar/{}".format(new_filename)

def id_card_upload(instance, filename):
    new_filename = '{}_{}.{}'.format('user',instance.pk, 'pdf')
    return "user_id_card/{}".format(new_filename)

def cv_upload(instance, filename):
    new_filename = '{}_{}.{}'.format('user',instance.pk, 'pdf')
    return "user_cv/{}".format(new_filename)

class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    timezone = models.CharField(max_length=32, choices=TIMEZONES,default='GMT')
    id_card = models.FileField(upload_to='doctors/id_card_upload', blank=True,
                               default='default_id_card.png')
    is_accepted = models.BooleanField(default=False)
    username = models.EmailField(
        "Email",
        unique=True,
        validators=[EmailValidator],
        error_messages={
            "unique": _("Bu email sistemimizde kayıtlıdır."),
        },
    )

    def __str__(self):
        return self.username
 
   
class Profession(MPTTModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.DO_NOTHING)
    full_path = models.CharField("Full Path", max_length=200, editable=False, default="default")

    class Meta:
        verbose_name_plural = "Professions"

    def save(self, *args, **kwargs):
        self.full_path = self.prep_full_path()
        super().save(*args, **kwargs)

    def prep_full_path(self):
        path = ""
        while self.parent:
            path += self.name
            if self.parent:
                path += ">"
            self = self.parent
        path += self.name
        path_list = path.split(">")
        return ">".join(path_list[::-1])

    def __str__(self):
        return self.name


class Experience(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='experience',null=True)
    experience_place = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    city= models.ForeignKey( City, related_name='experience', on_delete=models.DO_NOTHING )
    start_year = models.IntegerField(('start_year'),  choices=year_choices,
                                     default=datetime.datetime.now().year)
    end_year = models.IntegerField(('end_year'),  choices=year_choices,
                                    default=datetime.datetime.now().year)


class Education(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='education' )
    education_place = models.CharField(max_length=100)
    education_branch = models.CharField(max_length=100)
    city= models.ForeignKey( City,related_name='education', on_delete=models.DO_NOTHING )
    start_year = models.IntegerField(('start_year'),  choices=year_choices,
                                     default=datetime.datetime.now().year)
    end_year = models.IntegerField(('end_year'),  choices=year_choices,
                                   default=datetime.datetime.now().year)


class Profile(models.Model):
    TITLE_CHOICES = (
        ('PROFESSOR DOCTOR', _('Professor Doctor')),
        ('ASSOCIATE PROFESSOR', _('Associate Professor')),
        ('SPECIALIST', _('Specialist')),
        ('LECTURER', _('Lecturer')),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='doctors/avatar_upload',
    blank=True, default='default_1.png',
    validators=[FileExtensionValidator(['jpg','jpeg', 'gif', 'png',])])
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country= models.ForeignKey( Country, related_name='profile', on_delete=models.DO_NOTHING )
    city= models.ForeignKey( City, related_name='profile', on_delete=models.DO_NOTHING )
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=30, choices=TITLE_CHOICES)
    is_employee = models.BooleanField(default=False)
    orcid_account = models.URLField(max_length=200, null=True)
    pubmed_account = models.URLField(max_length=200, null=True)


class Employee(models.Model):
    CURRENCY_UNIT_CHOICES = (
        ('DOLLAR', '$'),
        ('EURO', '€'),
        ('TL', '₺'),
    )

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='employee')
    birth_date = models.DateField(max_length=8,blank=True)
    treatment_methods = ArrayField(models.CharField(max_length=100),null=True)
    scientific_publications = ArrayField(models.CharField(max_length=500),null=True )
    professional_memberships = ArrayField(models.CharField(max_length=500),null=True)
    professional_awards_degree = ArrayField(models.CharField(max_length=500),null=True)
    vocational_courses_conferences = ArrayField(models.CharField(max_length=500),null=True)
    client_cost = models.IntegerField()
    currency_unit = models.CharField(max_length=6, choices=CURRENCY_UNIT_CHOICES)
    patient_consultation = models.BooleanField(default=False)
    academic_consultation = models.BooleanField(default=False)
    cv = models.FileField(upload_to='doctors/cv_upload', blank=True, default='default_cv.png')
    about_doctor = models.CharField(max_length=700)
    hobbies = ArrayField(models.CharField(max_length=500),null=True)

