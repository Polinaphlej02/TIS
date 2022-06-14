from TIS.views import *
from django.urls import path, re_path

urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('registration/', RegisterStudent.as_view(), name='registration'),
    path('topics/<int:topic_id>', topic, name='topic'),
    path('topics/<int:topic_id>/questions', questions, name='questions'),
    path('testentry/', test_entry, name='test_entry'),
    path('test/<int:question_id>', test, name='test'),
    path('test/current_results', test_current_res, name='test_current_res'),
    path('test/rating', test_current_res, name='student_rating')
]