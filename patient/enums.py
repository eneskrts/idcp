from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderOptions(models.TextChoices):
    MALE = "male", _("Male")
    FEMALE = "female", _("Female")
    UNSPECIFIED = "unspecified", _("Unspecified")
    

class PacksPerDay(models.TextChoices):
    ZERO = "0", _("0")
    QUARTER = "quarter", _("Quarter")
    HALF = "half", _("Half")
    ONE = "1", _("1")
    TWO = "2", _("2")
    MORE = "more", _("More")


class FamilyMembers(models.TextChoices):
    MaternalGrandmother = "maternal grandmother", _("Maternal Grandmother")
    MaternalGrandfather = "maternal grandfather", _("Maternal Grandfather")
    PaternalGrandmother = "paternal grandmother", _("Paternal Grandmother")
    PaternalGrandfather = "paternal grandfather", _("Paternal Grandfather")
    Mother = "mother", _("Mother")
    Father = "father", _("Father")
    Brother = "brother", _("Brother")
    Sister = "sister", _("Sister")
    Son = "son", _("Son")
    Daughter = "daughters", _("Daughters")
    
