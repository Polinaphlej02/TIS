from TIS.views import *
from django.urls import path, re_path

urlpatterns = [
    path('authorization/', authorization, name='authorization'),
    path('authorization/registration/', RegisterStudent.as_view(), name='registration'),
    path('topics/<int:topic_id>', main_page, name="topic"),
]