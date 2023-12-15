from django.urls import path
from .views import *

urlpatterns = [
    path('recommendations/', SyncProfileDataView.as_view(), name='recommendations'),
    #path('recommendations/', your_view_function, name='recommendations'),
    #path('completion/', completion_request_view, name='completion-request'),
]