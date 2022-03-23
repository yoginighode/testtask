"""All model will be registered here."""
from django.db import models
from django.contrib.auth.models import User

class QuestionType(models.Model):
    class QUESTION_TYPE:
        SELECT = "select"
        MULTISELECT = "multiselect"

    QUESTION_TYPE_CHOICES = [
        (QUESTION_TYPE.SELECT, "Single Select"),
        (QUESTION_TYPE.MULTISELECT, "Multiple Select"),
    ]

    name = models.CharField(
        max_length=15, choices=QUESTION_TYPE_CHOICES, default=QUESTION_TYPE.SELECT)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.TextField()
    question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Choice(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_choice_set")

    def __str__(self):
        return self.text

class TestPaper(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="test_applicant")
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Test Paper of {}".format(self.user.username)


class UserAnswer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="user_answered_ques")
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    test_paper = models.ForeignKey(TestPaper, on_delete=models.CASCADE)

    def __str__(self):
        return "Answer of test_paper - {}".format(self.test_paper.id)
