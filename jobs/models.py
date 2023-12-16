from django.db import models
from profiles.models import *

class UserCareerAnalysis(models.Model):
    ##user_id = models.IntegerField()
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='career_analysis_by_id') #FK 간 역참조 해결
    #user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='career_analysis_by_name')
    ##user_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='career_analysis')
    user_name = models.CharField(max_length=255)
    job_name = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255)
    related_major = models.CharField(max_length=255)
    certifications = models.CharField(max_length=255)
    recommendation_reason = models.CharField(max_length=255)
