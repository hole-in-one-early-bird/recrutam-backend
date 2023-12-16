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
    #id = models.AutoField(primary_key=True)
    #user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    interest1 = models.CharField(max_length=255)
    interest2 = models.CharField(max_length=255)
    interest3 = models.CharField(max_length=255)

    def __str__(self):
        return f"User: {self.user_id.name}, Interests: {self.interest1}, {self.interest2}, {self.interest3}"


class UserEducation(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    education = models.CharField(max_length=10)
    major = models.CharField(max_length=50)
    major_check = models.CharField(max_length=50)

    def __str__(self):
        return f"User: {self.user_id.name}, Education: {self.education}, Major: {self.major}, Major Check: {self.major_check}"


class UserExperience(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    experience_type = models.CharField(max_length=255)
    experience_content = models.CharField(max_length=255)

    def __str__(self):
        return f"User: {self.user_id.name}, Experience Type: {self.experience_type}, Experience Content: {self.experience_content}"


class KeywordSet(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"Keyword: {self.keyword}, Type: {self.type}"


class UserKeyword(models.Model):
    id = models.AutoField(primary_key=True)
    #user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    keyword = models.CharField(max_length=20)
    type = models.CharField(max_length=20)

    class Meta:
        unique_together = ('keyword', 'type', 'user_id')

    def __str__(self):
        return f"User: {self.user_id.name}, Keyword: {self.keyword}, Type: {self.type}"


class UserKeywordType(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)

    class Meta:
        unique_together = ('user_id', 'type')
