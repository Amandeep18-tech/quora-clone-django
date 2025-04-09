from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, QuestionForm, AnswerForm
from .models import Question, Answer
from django.utils.timezone import now

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("question_list")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("question_list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def question_list(request):
    questions = Question.objects.all().order_by("-created_at")
    return render(request, "question_list.html", {"questions": questions})


@login_required
def post_question(request):
    if Question.objects.daily_question_count(request.user) >= 5:
        return render(request, "basic_message.html", {
            "message": "You’ve reached the daily limit of 5 questions."
        })

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect("question_list")
    else:
        form = QuestionForm()
    return render(request, "post_question.html", {"form": form})

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.for_question(question)

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            return redirect("question_detail", question_id=question_id)
    else:
        form = AnswerForm()

    return render(request, "question_detail.html", {
        "question": question,
        "answers": answers,
        "form": form
    })

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    if answer.user == request.user:
        return render(request, "basic_message.html", {
            "message": "You cannot like your own answer."
        })

    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)

    return redirect("question_detail", question_id=answer.question.id)