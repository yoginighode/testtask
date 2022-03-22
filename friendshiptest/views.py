# Create your views here.
import datetime
import random
from ast import literal_eval

from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from .models import Question, QuestionAnswer, UserAnswers, TestPaper, Choice


class QuestionListView(View):

    def get(self, request, *args, **kwargs):
        ids_list = Question.objects.all().values_list('id', flat=True)
        random_ids_list = random.sample(list(ids_list), 5)
        object_list = Question.objects.prefetch_related("question_choice_set").filter(id__in=random_ids_list)
        return render(request, 'home.html', {'object_list': object_list, 'ids_list': list(object_list.values_list('id', flat=True))})

    def post(self, request, *args, **kwargs):
        questions = Question.objects.filter(id__in=literal_eval(request.POST.get("ids_list")))
        user_obj, created = User.objects.get_or_create(
            username=request.POST.get("username"))
        test_paper_obj = TestPaper.objects.create(user=user_obj,submitted_on=datetime.datetime.now())
        test_paper_obj.questions.set(questions)
        for k in request.POST.keys():
            if (k.find('options-')==0):
                keys_ls = k.split("-")
                try:
                    que_obj = Question.objects.get(id=keys_ls[1])
                    ans_obj = UserAnswers.objects.create(
                            question=que_obj, test_paper=test_paper_obj)
                    is_correct_ls = []
                    given_ans_values = request.POST.getlist(k)
                    for given_ans in given_ans_values:
                        ans_idx = given_ans_values.index(given_ans)
                        actual_ans = que_obj.questionanswer.answer.values()[ans_idx].get("text")
                        ccqs = Choice.objects.get(text=given_ans)
                        ans_obj.answer.add(ccqs)
                        if given_ans == actual_ans:
                            is_correct_ls.append(1)
                        else:
                            is_correct_ls.append(0)
                    if all(is_correct_ls):
                        ans_obj.is_correct = True
                    ans_obj.save()
                except Question.DoesNotExist:
                    pass
        return render(request, 'result.html', {"id": test_paper_obj.id})


class ShareQuizView(View):

    def get(self, request, *args, **kwargs):
        tp_obj = TestPaper.objects.get(id=kwargs.get("id"))
        object_list = tp_obj.questions.all()
        return render(request, 'quiz.html', {'object_list': object_list,},)

    def post(self, request, *args, **kwargs):
        tp_obj = TestPaper.objects.get(id=kwargs.get("id"))
        applicat1_ans = tp_obj.useranswers_set.filter(is_correct=True).values_list("question", flat=True)
        applicat2_ans = [int(k.split("-")[1]) for k in request.POST.keys() if k.find('options-')==0]
        a_set = set(applicat1_ans)
        b_set = set(applicat2_ans)
        cnt = 0
        for q_id in (a_set & b_set):
            try:
                que_obj = Question.objects.get(id=q_id)
                given_ans_values = request.POST.getlist('options-'+ str(q_id))
                for given_ans in given_ans_values: 
                    ans_idx = given_ans_values.index(given_ans)
                    actual_ans = que_obj.questionanswer.answer.values()[ans_idx].get("text")
                    if given_ans == actual_ans:
                        cnt += 1
            except Question.DoesNotExist:
                pass
        percentage = (cnt*100/len(applicat1_ans))
        ctx = {'applicant': tp_obj.user.username, "percentage": ("%.2f" % percentage)}
        return render(request, 'success.html', ctx)
