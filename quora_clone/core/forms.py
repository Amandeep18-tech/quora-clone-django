from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import Question, Answer

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']

    def clean_body(self):
        body = self.cleaned_data.get("body")
        if len(body) < 10:
            raise ValidationError("Question body must be at least 10 characters long.")
        return body

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

    def clean_body(self):
        body = self.cleaned_data.get("body")
        if len(body) < 10:
            raise ValidationError("Answer must be at least 10 characters long.")
        return body
