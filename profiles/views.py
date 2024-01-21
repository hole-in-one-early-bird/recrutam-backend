#-- 진로 탐색 개인정보 API --#
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .keywords import add_keyword_set
import random
from collections import Counter
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
import logging
logger = logging.getLogger('pybo')

# 정보 1 - 이름, 성별, 나이, 저는요-
class UserProfileView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        key_list = list(data.keys())

        try:
            json_data = json.loads(key_list[0])
        except json.JSONDecodeError:
            print("Invalid JSON format in the QueryDict.")
            json_data = None

        if json_data:
            serializer = UserProfileSerializer(data=json_data)
            if serializer.is_valid():
                user_profile = serializer.save()
                user_id = user_profile.id
                return Response({"user_id": user_id}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message = "Invalid JSON format in the QueryDict."
            logging.error(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)   

    def get(self, request, user_id, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(id=user_id)
            serializer = UserProfileSerializer(user_profile)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
        except UserProfile.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND, safe=False, json_dumps_params={'ensure_ascii': False})

# 정보 2 - 관심분야 선택
class UserInterestView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        logging.error(f"Request Content: {data}")
        key_list = list(data.keys())
        logging.error(f"Key_list Content: {key_list}")

        try:
            json_data = json.loads(key_list[0])
            print(f'this is json_data : {json_data}')
            logging.error(f"Request json_data Content: {json_data}")
        except json.JSONDecodeError:
            print("Invalid JSON format in the QueryDict.")
            json_data = None
            logging.error("Invalid JSON format in the QueryDict.")

        if json_data:

            # user_id 추출
            user_profile = UserProfile.objects.get(id=json_data.get('user_id'))
            user_id = user_profile.id  # user_id 변수 선언

            # 저장할 모델 데이터 생성
            user_interest_data = {
                'user_id': user_id,
                'interest1': json_data.get('interest1'),
                'interest2': json_data.get('interest2'),
                'interest3': json_data.get('interest3'),
            }

            # 시리얼라이저를 사용하여 데이터 유효성 검사 및 저장
            serializer = UserInterestSerializer(data=user_interest_data)

            logging.error(f"{serializer}")
            if serializer.is_valid():
                # 저장하기 전에 user_id 설정
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                return JsonResponse(serializer.data, status=status.HTTP_400_BAD_REQUEST, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            error_message = "Invalid JSON format in the QueryDict."
            logging.error(error_message)
            return JsonResponse({"Invalid JSON format in the QueryDict."}, status=status.HTTP_400_BAD_REQUEST, safe=False, json_dumps_params={'ensure_ascii': False})

    def get(self, request, user_id, *args, **kwargs):
        try:
            user_interest = UserInterest.objects.get(user_id=user_id)
            serializer = UserInterestSerializer(user_interest)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
        except UserInterest.DoesNotExist:
            return JsonResponse({"message": "UserInterest not found"}, status=status.HTTP_404_NOT_FOUND, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False, json_dumps_params={'ensure_ascii': False})

# 정보 3 - 최종학력, 학과, 전공 적성 체크
class UserEducationView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        key_list = list(data.keys())

        try:
            print(key_list)
            json_data = json.loads(key_list[0])
        except json.JSONDecodeError:
            print("Invalid JSON format in the QueryDict.")
            json_data = None

        if json_data:
            serializer = UserEducationSerializer(data=json_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message = "Invalid JSON format in the QueryDict."
            logging.error(error_message)
            return Response({"message": error_message}, status=status.HTTP_400_BAD_REQUEST)
  
    def get(self, request, user_id, *args, **kwargs):
        try:
            user_education = UserEducation.objects.get(user_id=user_id)
            serializer = UserEducationSerializer(user_education)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
        except UserEducation.DoesNotExist:
            return JsonResponse({"message": "UserEducation not found"}, status=status.HTTP_404_NOT_FOUND, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False, json_dumps_params={'ensure_ascii': False})

# 정보 4 - 경험 선택, 입력
class UserExperienceView(APIView):
    def post(self, request, *args, **kwargs):
        experiences_data = request.data.get("experiences", [])
        logging.error(experiences_data)
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
    
    def get(self, request, user_id, *args, **kwargs):
        try:
            user_experiences = UserExperience.objects.filter(user_id=user_id)
            serializer = UserExperienceSerializer(user_experiences, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False, json_dumps_params={'ensure_ascii': False})

# 키워드 세트 추가 함수
add_keyword_set()

# 정보 5 - 파트 당 랜덤으로 키워드 보여주기
class Info5View(APIView):
    def get(self, request): # 랜덤으로 각 유형 당 키워드 8개씩 
        keyword_types = ["현장형", "탐구형", "예술형", "사회형", "리더형", "사무형"]
        random_keywords = {}

        for keyword_type in keyword_types:
            keywords = KeywordSet.objects.filter(type=keyword_type)
            selected_keywords = random.sample(list(keywords), min(16, len(keywords)))
            random_keywords[keyword_type] = [{"id": keyword.id, "keyword": keyword.keyword} for keyword in selected_keywords]

        return JsonResponse(random_keywords, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
    
    def post(self, request, *args, **kwargs):
        data = request.data
        logging.error(f'This is data: {data}')

        # QueryDict의 키를 추출
        key_list = list(data.keys())
            

        # JSON 문자열로 변환
        try:
            json_data = json.loads(key_list[0])
        except json.JSONDecodeError:
            print("Invalid JSON format in the QueryDict.")
            json_data = None

        # 변환된 JSON 데이터 확인
        if json_data:
            print(f'This is json_data: {json_data}')
            logging.error(f'This is json_data: {json_data}')

        # user_id 추출
        user_id = json_data.get('user_id')

        # user_keywords 추출 (리스트 형태로 예상)
        user_keywords_data = json_data.get('user_keywords', [])

        logging.error(user_id)
        logging.error(user_keywords_data)

        # 한 번만 호출하여 user_profile을 가져옴
        user_profile = UserProfile.objects.get(id=user_id)
        user_id = user_profile.id  # user_id 변수 선언

        user_keywords = []
        for keyword_data in user_keywords_data:
            print(f'this is keyword data : {keyword_data}')
            user_keyword_data = {
                'user_id': user_id,
                'keyword': keyword_data['keyword'],
                'type': keyword_data['type'],
            }
            logging.error(f'This is user_keyword_data: {user_keyword_data}')
            user_keyword_serializer = UserKeywordSerializer(data=user_keyword_data)
            logging.error(f'This is json_data: {user_keyword_serializer}')
            if user_keyword_serializer.is_valid():
                user_keywords.append(user_keyword_serializer.save())
            else:
                return Response(user_keyword_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 유형 뽑아서 UserKeywordType 테이블에 저장
        user_keyword_types = UserKeyword.objects.filter(user_id=user_id).values_list('type', flat=True)
        type_counts = Counter(user_keyword_types)
        logging.error(f'This is user_keyword_types: {user_keyword_types}')

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
 
        # 동일한 갯수를 가진 경우 모든 유형을 포함
        remaining_types = []
        if len(type_ranks) > 2 and rank == 2:
            remaining_types = [UserKeywordType(user_id=user_profile, type=user_type) for user_type in type_ranks.keys() - user_keyword_type_instances]

        # 유형 저장
        UserKeywordType.objects.bulk_create(user_keyword_type_instances + remaining_types)

        return Response(UserKeywordSerializer(user_keywords, many=True).data, status=status.HTTP_201_CREATED)