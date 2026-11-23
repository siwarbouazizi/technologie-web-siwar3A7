from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    pass


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.name


class Doctor(User):
    licence_numbers = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(4)]
    )
    phone = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    specialities = models.ManyToManyField(
        "AccountApp.Speciality", related_name="doctors"
    )

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


number_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Le CIN ne respecte pas le pattern 8 chiffres exacte"
)


def validate_birth_date(v):
    if v >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à aujourd'hui"
        )


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[number_validator]
    )
    phone = models.CharField(max_length=8)
    birth_date = models.DateField(validators=[validate_birth_date])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'