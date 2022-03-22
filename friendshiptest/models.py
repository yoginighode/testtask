"""All model will be registered here."""
from django.db import models
from django.contrib.auth.models import User

class QuestionType(models.Model):

    class QUESTION_TYPE:
        T1 = "T1"
        T2 = "T2"

    QUESTION_TYPE_CHOICES = [
        (QUESTION_TYPE.T1, "Single Select"),
        (QUESTION_TYPE.T2, "Multiple Select"),
    ]

    name = models.CharField(
        max_length=15, choices=QUESTION_TYPE_CHOICES, default=QUESTION_TYPE.T1)

    def __str__(self):
        return self.name

class Question(models.Model):

    text = models.TextField()
    que_choice = models.ForeignKey(QuestionType, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text


class Choice(models.Model):

    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_choice_set")

    def __str__(self):
        return self.text

class QuestionAnswer(models.Model):

    question = models.OneToOneField(
        Question, on_delete=models.CASCADE)
    answer = models.ManyToManyField(Choice)

    def __str__(self):
        return self.question.text


class TestPaper(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="test_applicant")
    submitted_on = models.DateTimeField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return "Test Paper of {}".format(self.user.username)


class UserAnswers(models.Model):

    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="user_answered_ques")
    answer = models.ManyToManyField(Choice)
    test_paper = models.ForeignKey(TestPaper, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return "Answer of test_paper - {}".format(self.test_paper.id)
