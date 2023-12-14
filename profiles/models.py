from django.db import models

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    about_me = models.TextField()

    def __str__(self):
        return self.name


class UserInterest(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    interest1 = models.CharField(max_length=255)
    interest2 = models.CharField(max_length=255)
    interest3 = models.CharField(max_length=255)

    def __str__(self):
        return f"User: {self.user_id.name}, Interests: {self.interest1}, {self.interest2}, {self.interest3}"