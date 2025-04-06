from django.db import models
from django.utils.timezone import now
from datetime import datetime

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True, blank=True)
    assigned_personnel = models.TextField(max_length=100)
    due_date = models.DateField(blank=False)
    status = models.CharField(max_length=20, default='Completed')

    def save(self, *args, **kwargs):
        today = now().date()

        if isinstance(self.due_date, str):
            self.due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()

            
        if self.status != 'Complete':
            if self.due_date < today:
                self.status = "Overdue"
            elif self.due_date == today:
                self.status = "Due Today"
            else:
                self.status = "Upcoming"

        super().save(*args, **kwargs)
