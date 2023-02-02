from django.db import models


class GenderOptions(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    UNSPECIFIED = "unspecified", "Unspecified"
    

class PacksPerDay(models.TextChoices):
    ZERO = "0"
    QUARTER = "quarter", "Quarter"
    HALF = "half", "Half"
    ONE = "1"
    TWO = "2"
    MORE = "more", "More"


class FamilyMembers(models.TextChoices):
    MaternalGrandmother = "maternal grandmother", "Maternal Grandmother"
    MaternalGrandfather = "maternal grandfather", "Maternal Grandfather"
    PaternalGrandmother = "paternal grandmother", "Paternal Grandmother"
    PaternalGrandfather = "paternal grandfather", "Paternal Grandfather"
    Mother = "mother", "Mother"
    Father = "father", "Father"
    Brother = "brother", "Brother"
    Sister = "sister", "Sister"
    Son = "son", "Son"
    Daughter = "daughters", "Daughters"
    
