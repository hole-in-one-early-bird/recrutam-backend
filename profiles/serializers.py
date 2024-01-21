from rest_framework import serializers
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'gender', 'age', 'about_me']

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = '__all__'

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = ['id', 'user_id', 'education', 'major', 'major_check']

class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = ['id', 'user_id', 'experience_type', 'experience_content']

class UserKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKeyword
        fields = '__all__'

class UserKeywordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKeywordType
        fields = ['id', 'user_id', 'type']