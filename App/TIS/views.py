from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import DataMixin

from .models import *
from .forms import *
from django.http import HttpResponse


def main_page(request, topic_id):
    chapters = Chapter.objects.all()
    topics = Topic.objects.all()

    theory_material_display = TheorMat.objects.filter(id_topic=topic_id)[0].theor_mat
    topic_obj_display = Topic.objects.filter(id=topic_id)[0]
    topic_name_display = topic_obj_display.topic_name
    chapter_id = topic_obj_display.id_chapter.id
    chapter_name_display = Chapter.objects.filter(id=chapter_id)[0].chapter_name

    struct = {}

    for chapter_obj in chapters:
        current_chapter = chapter_obj.chapter_name
        struct[current_chapter] = []
        for topic_obj in topics:
            if topic_obj.id_chapter.id == chapter_obj.id:
                struct[current_chapter].append(topic_obj)

    context = {"title": "TIS",
               "panel": struct,
               "theor_mat": theory_material_display,
               "chapter_name": chapter_name_display,
               "topic_name": topic_name_display}

    return render(request, template_name='TIS/base_main.html', context=context)


class RegisterStudent(CreateView, DataMixin):
    form_class = AddStudent
    template_name = 'TIS/registration.html'
    success_url = reverse_lazy("authorization")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'TIS/authorization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("registration")
