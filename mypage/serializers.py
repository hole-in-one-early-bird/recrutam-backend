from rest_framework import serializers
from .models import *

class UserBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookmark
        fields = '__all__'
