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
from django.http import JsonResponse, HttpResponse
from urllib.parse import unquote_plus
import json
import logging
logger = logging.getLogger('pybo')


class SyncProfileDataView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # URL에서 user_id 가져오기
            user_id = self.kwargs.get('user_id')

            data = request.data
            #print(data)

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
                print(f'this is json_data : {json_data}')

            #json.dumps(data) 
            
            # URL 디코딩
            #decoded_data = unquote_plus(data)

            # JSON 형식으로 변환
            #json_data = json.loads(decoded_data)

            request_data = {
                'messages': json_data,
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

                # UserProfile 모델에서 사용자 이름 가져오기
                ###user_profile = UserProfile.objects.get(id=user_id)
                ###user_name = user_profile.name
                user_profile = UserProfile.objects.get(id=user_id)
                user_name = user_profile.name

                # 저장할 모델 데이터 생성
                user_career_data = {
                    'user_id': user_id,
                    'user_name': user_name,  # 사용자 이름 추가
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
                else:
                    print(serializer.errors)

                # UserCareerAnalysis 테이블의 user_id에 맞는 데이터 가져옴
                #user_career_data = UserCareerAnalysis.objects.filter(user_id=user_id)
                ##user_career_data = UserCareerAnalysis.objects.filter(user_id=user_id).first()

                # 시리얼라이저를 사용하여 데이터를 직렬화
                ##serializer = UserCareerAnalysisSerializer(user_career_data)

                 # 정상적인 경우 로그 기록
                logging.info(f"Data synced successfully for user_id: {user_id}")
                logging.error(f"Request Content: {request.data}")
                logging.error(f"Request json_data Content: {json_data}")
                logging.error(f"Request key_list Content: {json_data}")
                # 직렬화된 데이터를 response로 반환
                #return Response(serializer.data, status=status.HTTP_200_OK)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
                #return Response(response.text, status=status.HTTP_200_OK)
                #return Response(status=status.HTTP_200_OK)
                #print(response.text)

            # 에러 응답일 경우 로그 기록
            logging.error(f"Failed to sync data with Clova Studio API. Status Code: {response.status_code}")
            logging.error(f"Response Content: {response.text}")
            logging.error(f"Request Content: {request.data}")

            #return Response({"message": "Failed to sync data with Clova Studio API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return HttpResponse(json.dumps({"message": "Failed to sync data with Clova Studio API."}), content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # 예외 발생 시 로그 기록
            logging.exception(f"An error occurred: {str(e)}")

            return HttpResponse(json.dumps({"message": str(e)}), content_type='application/json', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

            #return Response(response_data, status=status.HTTP_200_OK)
            #return JsonResponse(response_data, status=status.HTTP_200_OK)
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})

        except UserProfile.DoesNotExist:
            return Response({'error': '사용자 프로필을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

class CareerChatbotView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

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
                print(f'this is json_data : {json_data}')
                logging.error(f"Request json_data Content: {json_data}")


            request_data = {
                'messages': json_data,
                'topP': 0.8,
                'topK': 0,
                'maxTokens': 150, #256,
                'temperature': 0.5,
                'repeatPenalty': 5.0,
                'stopBefore': [],
                'includeAiFilters': True
            }

            # Clova Studio API 호출
            clova_api_url = 'your clova_api_url'
            api_key = 'your api_key'

            headers = {
                'X-NCP-CLOVASTUDIO-API-KEY': '',
                'X-NCP-APIGW-API-KEY': '',
                'X-NCP-CLOVASTUDIO-REQUEST-ID': '',
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
        response_data = {}  # 여기에서 response_data 초기화
        try:
            user_id = kwargs.get('user_id')

            #job_names = UserCareerAnalysis.objects.values_list('job_name', flat=True).last()

            #return Response(job_names, status=status.HTTP_200_OK)

            # user_id를 기반으로 데이터를 찾음
            user_career_data = UserCareerAnalysis.objects.filter(user_id=user_id).last()
            
            if user_career_data:
                job_name = user_career_data.job_name
                #return Response({"job_name": job_name}, status=status.HTTP_200_OK)
                return JsonResponse(job_name, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})
            else:
                logging.error("user_career_data error")
                #return Response({"message": "No data found for the given user_id"}, status=status.HTTP_404_NOT_FOUND)
                response_data = {"message": "No data found for the given user_id"}
                return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND, safe=False, json_dumps_params={'ensure_ascii': False})


        except Exception as e:
            #return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            logging.exception(f"An error occurred: {str(e)}")
            response_data = {"message": str(e)}
            return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False, json_dumps_params={'ensure_ascii': False})