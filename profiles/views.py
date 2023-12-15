from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .keywords import add_keyword_set
import random
from collections import Counter
from django.shortcuts import get_object_or_404

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

        # 한 번만 호출하여 user_profile을 가져옴
        user_profile = get_object_or_404(UserProfile, id=user_id)

        # 유형 뽑아서 UserKeywordType 테이블에 저장
        user_keyword_types = UserKeyword.objects.filter(user_id=user_id).values_list('type', flat=True)
        type_counts = Counter(user_keyword_types)

        #print(type_counts)
         # 등장 횟수에 따라 순위 부여
         # 코드 수정해야 함!갯수가 동일한 경우 동일한 값 모두 포함하도록#
        type_ranks = {}
        current_rank = 1
        prev_count = None
        for type_, count in type_counts.most_common():
            if prev_count != None and prev_count == count:
                type_ranks[type_] = current_rank
                continue
            type_ranks[type_] = current_rank
            current_rank += 1
            prev_count = count

        # 등장 횟수가 동일한 경우를 고려하여 userkeywordtype에 저장할 유형 선정
        user_keyword_type_instances = []
        for user_type, rank in type_ranks.items():
            if rank <= 2:  # 갯수별 차이가 확실한 경우 상위 2개 유형만 추출
                user_keyword_type_instances.append(UserKeywordType(user_id=user_profile, type=user_type))
        #print(type_ranks)
        # 동일한 갯수를 가진 경우 모든 유형을 포함
        remaining_types = []
        if len(type_ranks) > 2 and rank == 2:
            remaining_types = [UserKeywordType(user_id=user_profile, type=user_type) for user_type in type_ranks.keys() - user_keyword_type_instances]

        # 유형 저장
        UserKeywordType.objects.bulk_create(user_keyword_type_instances + remaining_types)

        return Response(UserKeywordSerializer(user_keywords, many=True).data, status=status.HTTP_201_CREATED)