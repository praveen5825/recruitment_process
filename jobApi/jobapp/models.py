from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class JobDetail(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class AppliedJob(models.Model):
    job = models.ForeignKey(JobDetail, on_delete=models.CASCADE)
    attached_candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.job.title} - {self.attached_candidate.first_name}"
