from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from profiles.models import *
from profiles.serializers import *
import requests
import re


class SyncProfileDataView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # URL에서 user_id 가져오기
            user_id = self.kwargs.get('user_id')

            data = request.data

            request_data = {
                'messages': data,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 256,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True
            }

            # Clova Studio API 호출
            clova_api_url = 'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-002'
            api_key = 'NTA0MjU2MWZlZTcxNDJiY7VDXefhz8V4ZzoevLBpy8lJ9HQR1OewMP1dViNpAkBnsyT5RAuHrfNCxdaSN7/iI9deWFY3wGBkGWgVquZizF72rWtMP1Yf3n5caxDqZg34MapRMeCxReYpDBRg+IlrKlF8lDyG4jxkgiy6od/4VGLQr1m8rgV7PbwSSvHI7icG1B1ysktd1FG2zC3ymdvFqLPP+1bV1BKIcjXvVX1GIxQ='

            headers = {
                'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY7VDXefhz8V4ZzoevLBpy8lJ9HQR1OewMP1dViNpAkBnsyT5RAuHrfNCxdaSN7/iI9deWFY3wGBkGWgVquZizF72rWtMP1Yf3n5caxDqZg34MapRMeCxReYpDBRg+IlrKlF8lDyG4jxkgiy6od/4VGLQr1m8rgV7PbwSSvHI7icG1B1ysktd1FG2zC3ymdvFqLPP+1bV1BKIcjXvVX1GIxQ=',
                'X-NCP-APIGW-API-KEY': 'oaIUfy0HmblC79yvZdADVBsuWyg0XhdhUw04mEFK',
                'X-NCP-CLOVASTUDIO-REQUEST-ID': '7b6b237de52245c59ae8aaf92bdb0e0d',
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'text/event-stream',
            }

            response = requests.post(clova_api_url, headers=headers, json=request_data, stream=True)

            if response.status_code == 200:

                # 정규표현식을 사용하여 "content" 다음의 문자열 추출
                content_matches = re.findall(r'"content":\s*"([^"]*)"', response.text)

                # "\\n"을 제거한 내용을 리스트로 저장
                cleaned_contents = [content.replace("\\n", " ") for content in content_matches]
                #print(cleaned_contents)

                # 길이에 따라 내림차순 정렬
                sorted_contents = sorted(cleaned_contents, key=len, reverse=True)

                # 상위 1개 추출
                longest_content = sorted_contents[0] if sorted_contents else None

                # 숫자를 기준으로 텍스트 쪼개기
                splitted_contents = re.split(r'\s*(\d+\.)\s*', longest_content)

                # 빈 문자열 및 None 제거
                result_list = [item.strip() for item in splitted_contents if item.strip() and item is not None]

                #print(result_list)

                # 저장할 모델 데이터 생성
                
                user_career_data = {
                    'user_id': user_id,
                    'job_name': result_list[1],
                    'job_description': result_list[3],
                    'related_major': result_list[5],
                    'certifications': result_list[7],  
                    'recommendation_reason': result_list[9] 
                }
                        
                # 시리얼라이저를 사용하여 데이터 유효성 검사 및 저장
                serializer = UserCareerAnalysisSerializer(data=user_career_data)
                if serializer.is_valid():
                    serializer.save()
                    

                # UserCareerAnalysis 테이블의 user_id에 맞는 데이터 가져옴
                #user_career_data = UserCareerAnalysis.objects.filter(user_id=user_id)
                user_career_data = UserCareerAnalysis.objects.filter(user_id=user_id).first()

                # 시리얼라이저를 사용하여 데이터를 직렬화
                serializer = UserCareerAnalysisSerializer(user_career_data)

                # 직렬화된 데이터를 response로 반환
                return Response(serializer.data, status=status.HTTP_200_OK)
                #return Response(response.text, status=status.HTTP_200_OK)
                #return Response(status=status.HTTP_200_OK)
                #print(response.text)

            return Response({"message": "Failed to sync data with Clova Studio API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, user_id):
        try:
            # 사용자 ID를 기반으로 profiles 앱 모델에서 데이터 검색
            user_profile = UserProfile.objects.get(id=user_id)
            user_education = UserEducation.objects.filter(user_id=user_id)
            user_experience = UserExperience.objects.filter(user_id=user_id)
            user_interest = UserInterest.objects.filter(user_id=user_id)
            user_keyword = UserKeyword.objects.filter(user_id=user_id)

            # 데이터 시리얼라이즈
            profile_serializer = UserProfileSerializer(user_profile)
            education_serializer = UserEducationSerializer(user_education, many=True)
            experience_serializer = UserExperienceSerializer(user_experience, many=True)
            interest_serializer = UserInterestSerializer(user_interest, many=True)
            keyword_serializer = UserKeywordSerializer(user_keyword, many=True)

            # 응답에 시리얼라이즈된 데이터 반환
            response_data = {
                'profile': profile_serializer.data,
                'education': education_serializer.data,
                'experience': experience_serializer.data,
                'interest': interest_serializer.data,
                'keyword': keyword_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except UserProfile.DoesNotExist:
            return Response({'error': '사용자 프로필을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

class CareerChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            request_data = {
                'messages': data,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 256,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True
            }

            # Clova Studio API 호출
            clova_api_url = 'https://clovastudio.stream.ntruss.com/testapp/v1/chat-completions/HCX-002'
            api_key = 'NTA0MjU2MWZlZTcxNDJiY58tx3puRhjmUbXrip8aqvbbrRCJug21YyQ5Mclpjcn3nt5hRJlFB1xYDM9yukOOuEIFhD9vBWwK/xn5+t8hy57vSMOXP7OWJmCK1rIkMfwVPJBb8e0jDnZ5nrMRh5ueFrGx8ffz7bQMkKbu4K9rJk2g+Gttnjtx6pGovnGDwAKudGrb3aI7z7wHjaeK25kgC3dQHpbQFF4Gw4ocAvdsNxU='

            headers = {
                'X-NCP-CLOVASTUDIO-API-KEY': 'NTA0MjU2MWZlZTcxNDJiY7VDXefhz8V4ZzoevLBpy8lJ9HQR1OewMP1dViNpAkBnsyT5RAuHrfNCxdaSN7/iI9deWFY3wGBkGWgVquZizF72rWtMP1Yf3n5caxDqZg34MapRMeCxReYpDBRg+IlrKlF8lDyG4jxkgiy6od/4VGLQr1m8rgV7PbwSSvHI7icG1B1ysktd1FG2zC3ymdvFqLPP+1bV1BKIcjXvVX1GIxQ=',
                'X-NCP-APIGW-API-KEY': 'oaIUfy0HmblC79yvZdADVBsuWyg0XhdhUw04mEFK',
                'X-NCP-CLOVASTUDIO-REQUEST-ID': '7b6b237de52245c59ae8aaf92bdb0e0d',
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'text/event-stream',
            }

            response = requests.post(clova_api_url, headers=headers, json=request_data, stream=True)

            if response.status_code == 200:
                
                 # 정규표현식을 사용하여 "content" 다음의 문자열 추출
                content_matches = re.findall(r'"content":\s*"([^"]*)"', response.text)

                # "\\n"을 제거한 내용을 리스트로 저장
                cleaned_contents = [content.replace("\\n", " ") for content in content_matches]
                #print(cleaned_contents)

                # 길이에 따라 내림차순 정렬
                sorted_contents = sorted(cleaned_contents, key=len, reverse=True)

                # 상위 1개 추출
                longest_content = sorted_contents[0] if sorted_contents else None

                # 숫자를 기준으로 텍스트 쪼개기
                splitted_contents = re.split(r'\s*(\d+\.)\s*', longest_content)

                # 빈 문자열 및 None 제거
                result_list = [item.strip() for item in splitted_contents if item.strip() and item is not None]
                #print(result_list)

                result_string = " ".join(result_list)

                #return Response(response.text, status=status.HTTP_200_OK)
                return Response(result_string, status=status.HTTP_200_OK)

            return Response({"message": "Failed to sync data with Clova Studio API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            job_names = UserCareerAnalysis.objects.values_list('job_name', flat=True).last()

            return Response(job_names, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)