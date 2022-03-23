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
        ids_list = Question.objects.all().values_list('id', flat=True)
        try:
            random_ids_list = random.sample(list(ids_list), settings.TOTAL_TEST_QUESTION)
            object_list = Question.objects.prefetch_related("question_choice_set").filter(id__in=random_ids_list)
        except ValueError:
            object_list = Question.objects.prefetch_related("question_choice_set").all()
        return render(request, 'home.html', {'object_list': object_list})

    def post(self, request, *args, **kwargs):
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
        tp_obj = TestPaper.objects.get(id=kwargs.get("id"))
        question_ids = tp_obj.useranswer_set.all().values_list("question", flat=True).distinct()
        object_list = Question.objects.filter(id__in=question_ids)
        return render(request, 'quiz.html', {'object_list': object_list,},)

    def post(self, request, *args, **kwargs):
        tp_obj = TestPaper.objects.get(id=kwargs.get("id"))
        applicat1_ans = tp_obj.useranswer_set.all().values_list("question", flat=True)
        applicat2_ans = [int(k.split("-")[1]) for k in request.POST.keys() if k.find('options-')==0]
        a_set = set(applicat1_ans)
        b_set = set(applicat2_ans)
        cnt = 0
        for q_id in (a_set & b_set):
            try:
                que_obj = Question.objects.get(id=q_id)
                user_answers = tp_obj.useranswer_set.filter(question=que_obj).values_list("answer__text", flat=True)
                if que_obj.question_type.name == "select":
                    given_ans = request.POST.get('options-'+ str(q_id))
                    if given_ans == user_answers[0]:
                        cnt += 1
                elif que_obj.question_type.name == "multiselect":
                    given_ans_values = request.POST.getlist('options-'+ str(q_id))
                    is_correct_ls = []
                    for given_ans in given_ans_values:
                        if given_ans in user_answers:
                            is_correct_ls.append(1)
                        else:
                            is_correct_ls.append(0)
                    if all(is_correct_ls) and len(given_ans_values) == len(user_answers):
                        cnt += 1
            except Question.DoesNotExist:
                pass
        percentage = (cnt*100/len(set(applicat1_ans)))
        ctx = {'applicant': tp_obj.user.username, "percentage": ("%.2f" % percentage)}
        return render(request, 'success.html', ctx)
