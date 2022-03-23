# Create your views here.
import datetime
import random
from ast import literal_eval

from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.conf import settings

from .models import Question, UserAnswer, TestPaper, Choice

class QuestionListView(View):

    def get(self, request, *args, **kwargs):
        """Get the list of random questions."""
        ids_list = Question.objects.all().values_list('id', flat=True)
        try:
            random_ids_list = random.sample(list(ids_list), settings.TOTAL_TEST_QUESTION)
            object_list = Question.objects.prefetch_related("question_choice_set").filter(id__in=random_ids_list)
        except ValueError:
            object_list = Question.objects.prefetch_related("question_choice_set").all()
        return render(request, 'home.html', {'object_list': object_list})

    def post(self, request, *args, **kwargs):
        """Save the questions answer."""
        user_obj, created = User.objects.get_or_create(
            username=request.POST.get("username"))
        test_paper_obj = TestPaper.objects.create(user=user_obj,submitted_on=datetime.datetime.now())
        for k in request.POST.keys():
            if (k.find('options-')==0):
                keys_ls = k.split("-")
                try:
                    que_obj = Question.objects.get(id=keys_ls[1])
                    is_correct_ls = []
                    given_ans_values = request.POST.getlist(k)
                    for given_ans in given_ans_values:
                        actual_ans_ls = que_obj.question_choice_set.all().values_list("text",flat=True)
                        choice_obj = Choice.objects.get(text=given_ans)
                        ans_obj = UserAnswer.objects.create(question=que_obj, test_paper=test_paper_obj, answer=choice_obj)
                except Question.DoesNotExist:
                    pass
        return render(request, 'result.html', {"id": test_paper_obj.id})


class ShareQuizView(View):

    def get(self, request, *args, **kwargs):
        """Get the list of questions of test paper."""
        object_list = self.get_questions_objs(kwargs.get("id"))
        return render(request, 'quiz.html', {'object_list': object_list,},)

    def get_questions_objs(self, test_paper_id):
        """
            Args:
              test_paper_id(int): Test paper id

            Return:
              It will return queryset of Questions

        """
        return Question.objects.filter(user_answered_ques__test_paper_id=test_paper_id).select_related("question_type").distinct()


    def get_user_ans(self, tp_obj, que_obj):
        """
            Args:
              test_paper_id(obj): Test paper Object
              question_id(obj): Question Object

            Return:
              It will return list of answers of question

        """
        user_answers = tp_obj.useranswer_set.filter(question=que_obj).values_list("answer__text", flat=True)
        return user_answers


    def is_matched(self, user_ans, friend_ans):
        """
            Args:
              user_ans(list): User Answer List
              user_ans(str): friend_ans

            Return:
              It will return match_count 1 or 0

        """
        if friend_ans == user_ans[0]:
            return 1
        return 0

    def is_matched_multi(self, user_ans, friend_ans):
        """
            Args:
              user_ans(list): User Answer List
              user_ans(str): friend_ans

            Return:
              It will return match_count 1 or 0

        """
        is_correct_ls = []
        for given_ans in friend_ans:
            if given_ans in user_ans:
                is_correct_ls.append(1)
            else:
                is_correct_ls.append(0)
        if all(is_correct_ls) and len(user_ans) == len(friend_ans):
            return 1
        return 0

    def post(self, request, *args, **kwargs):
        """Method to match the answers with firend answers."""
        match_count = 0
        test_paper = TestPaper.objects.get(id=kwargs.get("id"))
        questions = self.get_questions_objs(test_paper.id)
        for que_obj in questions:
            if que_obj.question_type.name == "select":
                match_count += self.is_matched(self.get_user_ans(test_paper, que_obj), request.POST.get('options-'+ str(que_obj.id)))

            elif que_obj.question_type.name == "multiselect":
                match_count += self.is_matched_multi(self.get_user_ans(test_paper, que_obj), request.POST.getlist('options-'+ str(que_obj.id)))

        percentage = (match_count*100/settings.TOTAL_TEST_QUESTION)
        ctx = {'applicant': test_paper.user.username, "percentage": ("%.2f" % percentage)}
        return render(request, 'success.html', ctx)
