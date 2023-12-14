from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    about_me = models.TextField()

    def __str__(self):
        return self.name