from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('check_duplicate_username/<str:username>/', check_duplicate_username, name='check_duplicate_username'), #username 중복 검사
    path('check_duplicate_email/<str:email>/', check_duplicate_email, name='check_duplicate_username'), #email 중복 검사
]