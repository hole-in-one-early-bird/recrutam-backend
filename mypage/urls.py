from django.urls import path
from .views import *

urlpatterns = [
     path('bookmarked-job/<int:user_id>/', BookmarkJobView.as_view(), name='bookmark_job'),
     path('bookmarked-job/<int:user_id>/<int:bookmark_id>/', BookmarkJobView.as_view(), name='delete_bookmark'),
]
