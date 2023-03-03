from django.db import models
from django.utils.translation import gettext_lazy as _    


class Title(models.TextChoices):
    PROFESSOR_DOCTOR = "professor doctor", _("Professor Doctor")
    ASSOCIATE_PROFESSOR = "associate professor", _("Associate Professor")
    SPECIALIST = "specialist", _("Specialist")
    LECTURER = "lecturer", _("Lecturer")


class CurrencyUnit(models.TextChoices):
    DOLLAR = "dollar", ("$")
    EURO = "euro", ("€")
    TL = "tl", ("₺")
