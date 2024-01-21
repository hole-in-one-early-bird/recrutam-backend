#-- 마이페이지 API --#
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *
from profiles.models import *
from django.http import JsonResponse, HttpResponse

# 찜한 직업 - 추가(POST), 조회(GET), 삭제(DELETE)
class BookmarkJobView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            # UserProfile이 존재하는지 확인
            user_profile = get_object_or_404(UserProfile, id=user_id)

            # mypage 앱의 UserBookmark에서 데이터 조회
            mypage_bookmarks = UserBookmark.objects.filter(user_id=user_profile)
            serializer = UserBookmarkSerializer(mypage_bookmarks, many=True)
            
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})

        except Exception as e:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request, user_id, *args, **kwargs):
        try:
            # UserProfile이 존재하는지 확인
            user_profile = get_object_or_404(UserProfile, id=user_id)

            # JSON 데이터 파싱
            json_data = JSONParser().parse(request)

            # JSON 데이터를 기반으로 UserBookmark에 저장
            UserBookmark.objects.create(
                user_id=user_profile,
                job_name=json_data.get('job_name', ''),
                job_description=json_data.get('job_description', ''),
                related_major=json_data.get('related_major', ''),
                certifications=json_data.get('certifications', ''),
                recommendation_reason=json_data.get('recommendation_reason', '')
            )

            return Response({"message": "Bookmark added successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, user_id, bookmark_id, *args, **kwargs):
        try:
            # UserProfile이 존재하는지 확인
            user_profile = get_object_or_404(UserProfile, id=user_id)

            # jobs 앱의 UserBookmark에서 데이터 가져오기
            bookmark_to_delete = get_object_or_404(UserBookmark, id=bookmark_id, user_id=user_profile)
            bookmark_to_delete.delete()

            response_data = {"message": "Bookmark deleted successfully."}
            return JsonResponse(response_data, status=status.HTTP_200_OK, safe=False, json_dumps_params={'ensure_ascii': False})


        except Exception as e:
            response_data = {"message": str(e)}
            return JsonResponse(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False, json_dumps_params={'ensure_ascii': False})