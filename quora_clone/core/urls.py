from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.question_list, name='question_list'),
    path('question/post/', views.post_question, name='post_question'),
    path('question/<uuid:question_id>/', views.question_detail, name='question_detail'),
    path('answer/<uuid:answer_id>/like/', views.like_answer, name='like_answer'),
]
