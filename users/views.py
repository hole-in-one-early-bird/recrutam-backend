from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics

from .serializers import RegisterSerializer, LoginSerializer

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from django.http import JsonResponse

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data # validate()의 리턴값인 token을 받아온다.
        return Response({"token": token.key}, status=status.HTTP_200_OK)

# username 중복 검사
def check_duplicate_username(request, username): 
    # username이 이미 존재하는지 확인
    is_duplicate = User.objects.filter(username=username).exists()

    # 결과를 JSON 형태로 반환
    if is_duplicate:
        response_data = {
            'status': 'error',
            'message': '이미 사용 중인 아이디입니다.'
        }
    else:
        response_data = {
            'status': 'success',
            'message': '사용 가능한 아이디입니다.'
        }

    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})

# email 중복 검사
def check_duplicate_email(request, email):
    # email이 이미 존재하는지 확인
    is_duplicate = User.objects.filter(email=email).exists()

    # 결과를 JSON 형태로 반환
    if is_duplicate:
        response_data = {
            'status': 'error',
            'message': '이미 사용 중인 이메일입니다.'
        }
    else:
        response_data = {
            'status': 'success',
            'message': '사용 가능한 이메일입니다.'
        }

    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})