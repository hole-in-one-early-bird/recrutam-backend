from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('info1/', UserProfileView.as_view(), name='info1'),
]
