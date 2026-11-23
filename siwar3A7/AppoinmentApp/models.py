from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from AccountApp.models import Doctor, Patient


class Appointement(models.Model):
    reason = models.TextField()
    prescription = models.FileField(blank=True, upload_to='prescription/')

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    appointement_date = models.DateField()

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointements")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointements")

    def clean(self):
        if not self.appointement_date:
            return

        # On ne vérifie la date que pour un nouveau rdv ou si la date a changé
        if self._state.adding:
            date_modifiee = True
        else:
            date_modifiee = not Appointement.objects.filter(
                pk=self.pk, appointement_date=self.appointement_date
            ).exists()

        if date_modifiee and self.appointement_date <= timezone.localdate():
            raise ValidationError(
                "La date du rdv doit être postérieure à la date d'aujourd'hui."
            )

    class Meta:
        ordering = ["appointement_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointement_date"],
                name="unicite_doctor_date",
                violation_error_message="Ce docteur possède déjà un rdv à cette date.",
            )
        ]