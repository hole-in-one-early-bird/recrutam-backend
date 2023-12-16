from django.db import models
from profiles.models import *

class UserBookmark(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    job_name = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255)
    related_major = models.CharField(max_length=255)
    certifications = models.CharField(max_length=255)
    recommendation_reason = models.CharField(max_length=255)
