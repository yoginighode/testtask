"""Register test app models here."""

from django.contrib import admin
from .models import *

admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(QuestionAnswer)
admin.site.register(TestPaper)
admin.site.register(UserAnswers)
