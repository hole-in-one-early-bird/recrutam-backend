from rest_framework import serializers
from .models import *

class UserCareerAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCareerAnalysis
        fields = '__all__'
