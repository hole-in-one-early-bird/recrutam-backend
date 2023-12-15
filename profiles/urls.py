from django.urls import path
from .views import *

urlpatterns = [
    path('info1/', UserProfileView.as_view(), name='info1'),
    path('info2/', UserInterestView.as_view(), name='info2'),
    path('info3/', UserEducationView.as_view(), name='info3'),
    path('info4/', UserExperienceView.as_view(), name='info4'),
    path('info5/', Info5View.as_view(), name='info5'),
]
