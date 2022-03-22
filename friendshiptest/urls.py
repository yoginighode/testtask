"""All app urls."""
from django.urls import path
from .views import QuestionListView, ShareQuizView

app_name = "quiz"
urlpatterns = [
	path('', QuestionListView.as_view(), name='home'),
	path('share-quiz/<int:id>/', ShareQuizView.as_view(), name='share-quiz'),
]
