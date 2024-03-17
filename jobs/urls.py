from django.urls import path
from .views import *

urlpatterns = [
    path('recommendations/<int:user_id>/', SyncProfileDataView.as_view(), name='recommendations'),
    path('career-chatbot/<int:user_id>/', CareerChatbotView.as_view(), name='career_chatbot'),
]