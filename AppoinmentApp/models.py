from django.db import models
from AccountApp.models import Doctor, Patient

# Create your models here.


class Appointement(models.Model):
    reason = models.TextField()
    prescription = models.FileField(
        blank=True,  # n'est pas obligatoire
        upload_to='prescription/'
    )

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    # 2eme solution :
    # status = models.CharField(max_length=10, choices=
    #                           [("PENDING", "En attente"), ("CONFIRMED", "Confirmé"), ("CANCELLED", "Annulé")]
    #                           , default=Status.PENDING)

    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    appointement_date = models.DateField()

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointements")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointements")
    # ou : patient = models.ForeignKey("AccountApp.Patient", on_delete=models.CASCADE, related_name="appointements")

    class Meta:
        ordering = ["appointement_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointement_date"],
                name="unicite_patient-doctor-date",
                violation_error_message="ce docteur possede un rdv avec cette date"
            )
        ]