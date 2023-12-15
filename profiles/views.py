from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .keywords import add_keyword_set
import random

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

# 키워드 세트 추가 함수
add_keyword_set()

class Info5View(APIView):
    def get(self, request): # 랜덤으로 각 유형 당 키워드 8개씩 
        keyword_types = ["현장형", "탐구형", "예술형", "사회형", "리더형", "사무형"]
        random_keywords = {}

        for keyword_type in keyword_types:
            keywords = KeywordSet.objects.filter(type=keyword_type)
            selected_keywords = random.sample(list(keywords), min(8, len(keywords)))
            random_keywords[keyword_type] = [{"id": keyword.id, "keyword": keyword.keyword} for keyword in selected_keywords]

        return Response(random_keywords, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        user_keywords_data = request.data.get('user_keywords', [])

        user_keywords = []
        for keyword_data in user_keywords_data:
            user_keyword_data = {
                'user_id': user_id,
                'keyword': keyword_data['keyword'],
                'type': keyword_data['type'],
            }
            user_keyword_serializer = UserKeywordSerializer(data=user_keyword_data)
            if user_keyword_serializer.is_valid():
                user_keywords.append(user_keyword_serializer.save())
            else:
                return Response(user_keyword_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserKeywordSerializer(user_keywords, many=True).data, status=status.HTTP_201_CREATED)