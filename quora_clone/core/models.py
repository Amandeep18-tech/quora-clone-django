import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class QuestionManager(models.Manager):
    def daily_question_count(self, user):
        """
        Get count of today's questions by user
        Parameters
        ----------
        user : User
            User instance
        
        Returns
        -------
        count : int
            Number of questions created today by the user
        """
        return self.filter(user=user, created_at__date=now().date()).count()
    
class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = QuestionManager()
    
    def __str__(self):
        return self.title

class AnswerManager(models.Manager):
    def for_question(self, question):
        """
        Get answers for a given question sorted by created_at
        Parameters
        ----------
        question : Question
            The question instance

        Returns
        -------
        answers : QuerySet
            List of answers ordered by created_at desc
        """
        return self.filter(question=question).order_by("-created_at")
    
class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_answers", blank=True)

    objects = AnswerManager()
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"Answer to: {self.question.title}"
