from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import DataMixin
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect


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
               "topic_name": topic_name_display}

    return render(request, template_name='TIS/topic.html', context=context)


@login_required(login_url='/login')
def questions(request, topic_id):
    topic_obj_display = Topic.objects.filter(id=topic_id)[0]
    topic_name_display = topic_obj_display.topic_name
    chapter_id = topic_obj_display.id_chapter.id
    chapter_name_display = Chapter.objects.filter(id=chapter_id)[0].chapter_name

    questions = Question.objects.filter(id_topic=topic_id)
    struct = create_panel_struct()

    context = {"title": "TIS",
               "panel": struct,
               "questions": questions,
               "chapter_name": chapter_name_display,
               "topic_name": topic_name_display}

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

    context = {"title": "TIS",
               "panel": struct}

    return render(request, template_name='TIS/test.html', context=context)


@login_required(login_url='/login')
def test(request, question_id):
    question_test = QuestionMini.objects.filter(id=question_id)[0]
    questions_num = len(QuestionMini.objects.all())
    next_question_id, prev_question_id = question_id + 1, question_id - 1
    struct = create_panel_struct()
    if request.method == "POST":
        form = StudentAnswerForm(request.POST)
        print(form.fields)
        if form.is_valid():
            try:
                form.save()
            except:
                form.add_error(None, "Ошибка добавления ответа")
    else:
        form = StudentAnswerForm()

    context = {"title": "TIS",
               "panel": struct,
               "question": question_test,
               "questions_num": questions_num,
               "next_question_id": next_question_id,
               "prev_question_id": prev_question_id,
               "answer_form": form}

    return render(request, template_name='TIS/test_questions.html', context=context)
