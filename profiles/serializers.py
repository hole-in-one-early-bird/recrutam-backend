from rest_framework import serializers
from .models import UserProfile, UserInterest

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'gender', 'age', 'about_me']

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ['id', 'user_id', 'interest1', 'interest2', 'interest3']
