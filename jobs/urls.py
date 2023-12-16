from django.urls import path
from .views import *

urlpatterns = [
    path('recommendations/', SyncProfileDataView.as_view(), name='recommendations'),
    path('recommendations/<int:user_id>/', SyncProfileDataView.as_view(), name='user-profile-get'),
    path('career-chatbot/', CareerChatbotView.as_view(), name='career_chatbot'),
]