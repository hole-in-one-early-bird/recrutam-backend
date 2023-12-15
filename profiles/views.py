from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

class UserProfileView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()  # UserProfile 객체를 생성하고 반환
            user_id = user_profile.id  # 생성된 UserProfile 객체의 ID 추출
            return Response({"user_id": user_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInterestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserInterestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserEducationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserEducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserExperienceView(APIView):
    def post(self, request, *args, **kwargs):
        experiences_data = request.data.get("experiences", [])
        errors = []

        for experience_data in experiences_data:
            serializer = UserExperienceSerializer(data=experience_data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Experiences added successfully"}, status=status.HTTP_201_CREATED)