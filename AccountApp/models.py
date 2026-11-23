from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.


class User(AbstractUser):
    pass


class Doctor(User):
    licence_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6), MaxLengthValidator(8)]
    )
    phone = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    specialities = models.ManyToManyField(
        "AccountApp.Speciality",
        related_name="doctors"  # s.doctors => recuperer la liste des docteurs
    )  # automatiquement many to many => liste dans class Speciality


number_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="le numero ne respecte pas le pattern 8 chiffres exacte"
)


# fonction personnalisee
def validate_birth_date(v):
    if v >= timezone.localdate():
        raise ValidationError("la date de naissance doit etre inférieur à la date d'aujourd'hui")


class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[number_validator])
    phone = models.CharField(max_length=8, validators=[number_validator])

    birth_date = models.DateField(validators=[validate_birth_date])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)