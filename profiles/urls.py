from django.urls import path
from .views import *

urlpatterns = [
    path('info1/', UserProfileView.as_view(), name='info1'),
    path('info2/', UserInterestView.as_view(), name='info2'),
]
