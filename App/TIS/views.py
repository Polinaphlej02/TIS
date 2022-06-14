from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import DataMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import connection


TOPICS_ID_MAP = {1: 1, 2: 2, 3: 1, 4: 2,
                 5: 3, 6: 1, 7: 2, 8: 3}


def create_panel_struct():
    chapters = Chapter.objects.all()
    topics = Topic.objects.all()

    struct = {}

    for chapter_obj in chapters:
        current_chapter = chapter_obj.chapter_name
        struct[current_chapter] = []
        for topic_obj in topics:
            if topic_obj.id_chapter.id == chapter_obj.id:
                struct[current_chapter].append(topic_obj)

    return struct


@login_required(login_url='/login')
def topic(request, topic_id):
    theory_material_display = TheorMat.objects.filter(id_topic=topic_id)[0].theor_mat
    topic_obj_display = Topic.objects.filter(id=topic_id)[0]
    topic_name_display = topic_obj_display.topic_name
    chapter_id = topic_obj_display.id_chapter.id
    chapter_name_display = Chapter.objects.filter(id=chapter_id)[0].chapter_name

    struct = create_panel_struct()

    context = {"title": "TIS",
               "panel": struct,
               "theor_mat": theory_material_display,
               "chapter_name": chapter_name_display,
               "topic_name": topic_name_display,
               "chapter_num": chapter_id,
               "topic_num": TOPICS_ID_MAP[topic_id]}

    return render(request, template_name='TIS/topic.html', context=context)


@login_required(login_url='/login')
def questions(request, topic_id):
    topic_obj_display = Topic.objects.filter(id=topic_id)[0]
    topic_name_display = topic_obj_display.topic_name
    chapter_id = topic_obj_display.id_chapter.id
    chapter_name_display = Chapter.objects.filter(id=chapter_id)[0].chapter_name

    question_objs = Question.objects.filter(id_topic=topic_id)
    struct = create_panel_struct()

    context = {"title": "TIS",
               "panel": struct,
               "questions": question_objs,
               "chapter_name": chapter_name_display,
               "topic_name": topic_name_display,
               "chapter_num": chapter_id,
               "topic_num": TOPICS_ID_MAP[topic_id]}

    return render(request, template_name='TIS/questions.html', context=context)


class RegisterStudent(CreateView, DataMixin):
    form_class = AddStudent
    template_name = 'TIS/registration.html'
    success_url = "topics/1"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # save the new user first
        form.save()
        # get the username and password
        username = self.request.POST['username']
        password = self.request.POST['password']
        # authenticate user then login
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect("/topics/1")


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'TIS/authorization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("topic", kwargs={"topic_id": 1})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def test_entry(request):
    struct = create_panel_struct()
    context = {"title": "Тест (главная)",
               "panel": struct}

    return render(request, template_name='TIS/test.html', context=context)


@login_required(login_url='/login')
def test(request, question_id):
    question_test = QuestionMini.objects.filter(id=question_id)[0]
    questions_num = len(QuestionMini.objects.all())
    next_question_id, prev_question_id = question_id + 1, question_id - 1
    answers = Answer.objects.filter(id_question=question_id)
    all_stud_answers = AnswerStudent.objects.filter(id_student=request.user.id)
    num_of_stud_answers = len(AnswerStudent.objects.filter(id_question=question_id, id_student=request.user.id))
    stud_answered = False if num_of_stud_answers == 0 else True

    passed_questions = [ans.id_question.id for ans in all_stud_answers]
    passed_questions_map = {}
    for i in range(1, questions_num + 1):
        if i in passed_questions:
            passed_questions_map[i] = "passed"
            continue
        passed_questions_map[i] = "not_passed"

    struct = create_panel_struct()
    if request.method == "POST":
        form_dict = request.POST.copy()
        form_dict["id_question"] = question_id
        form_dict["id_student"] = request.user.id
        form = StudentAnswerForm(form_dict)
        if form.is_valid():
            try:
                form.save()
                if question_id != questions_num:
                    return redirect(f"/test/{question_id + 1}")
                return redirect(f"/test/{question_id}")
            except:
                form.add_error(None, "Ошибка добавления ответа")
    else:
        form = StudentAnswerForm()

    context = {"title": "Тест",
               "panel": struct,
               "question": question_test,
               "questions_num": questions_num,
               "next_question_id": next_question_id,
               "prev_question_id": prev_question_id,
               "answers": answers,
               "stud_answered": stud_answered,
               "passed_questions_map": passed_questions_map,
               "answer_form": form}

    return render(request, template_name='TIS/test_questions.html', context=context)


@login_required(login_url='/login')
def test_current_res(request):
    struct = create_panel_struct()
    cursor = connection.cursor()
    user_id = request.user.id
    questions_num = len(QuestionMini.objects.all())
    stud_answers_num = len(AnswerStudent.objects.filter(id_student=user_id))
    ans_correct_num = None

    if stud_answers_num == 0:
        last_rating_str = Student.objects.filter(id=user_id)[0].last_rating_str
        if last_rating_str is not None:
            ans_correct_num = int(last_rating_str.split(' / ')[0])
    else:
        best_rating_float = Student.objects.filter(id=user_id)[0].best_rating
        best_rating_str = Student.objects.filter(id=user_id)[0].best_rating_str

        join_query = f"""SELECT ta.answer, tas.ans_stud FROM tis_answer as ta INNER JOIN tis_answerstudent as tas 
                         ON ta.id_question_id = tas.id_question_id 
                         WHERE tas.id_student_id = {user_id} AND ta.is_correct = 1"""

        cursor.execute(join_query)
        results = cursor.fetchall()
        ans_correct_num = 0
        for right_ans, stud_ans in results:
            if right_ans == stud_ans:
                ans_correct_num += 1

        last_rating_float = round(ans_correct_num / questions_num * 100, 2)
        last_rating_str = f"{ans_correct_num} / {questions_num}"
        if last_rating_float > best_rating_float:
            best_rating_float = last_rating_float
            best_rating_str = last_rating_str

        update_stud_query = f"""UPDATE tis_student SET best_rating = {best_rating_float}, 
                                best_rating_str = '{best_rating_str}',
                                last_rating_str = '{last_rating_str}' WHERE id = {user_id}"""
        cursor.execute(update_stud_query)

        delete_ans_query = f"""DELETE FROM tis_answerstudent WHERE id_student_id = {user_id}"""
        cursor.execute(delete_ans_query)

    context = {"title": "Результаты теста",
               "panel": struct,
               "ans_correct_num": ans_correct_num,
               "questions_num": questions_num}

    return render(request, template_name='TIS/current_results.html', context=context)


@login_required(login_url='/login')
def rating(request):
    struct = create_panel_struct()
    user_id = request.user.id
    stud_obj = Student.objects.filter(id=user_id)[0]
    best_rating_float = stud_obj.best_rating
    best_rating_str = stud_obj.best_rating_str

    context = {"title": "Рейтинг",
               "panel": struct,
               "best_rating_float": best_rating_float,
               "best_rating_str": best_rating_str}

    return render(request, template_name='TIS/rating.html', context=context)
