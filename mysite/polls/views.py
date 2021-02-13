from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    #GET방식과 POST방식의 처리
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question' : question,
                'error_message' : '항목을 선택해 주세요',
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # HttpResponseRedirect 는 POST 와 세트 
            # POST로 view 가 호출된 경우에는 HttpResponseRedirect 로 응답한다.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



# 함수형 view
# def index(request) : 
#     # return HttpResponse("토스 가고싶다")
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = {
#     #     'latest_question_list' : latest_question_list,
#     # }
#     # # output = ', '.join([q.question_text for q in latest_question_list])
#     # return HttpResponse(template.render(context,request))
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     return render(request,'polls/index.html', context)

# def detail(request, question_id):
#     # try:
#     #     question  = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("질문이 없음")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request,'polls/detail.html',{'question' : question} )

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question' :question})

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'polls/detail.html', {
#             'question' : question,
#             'error_message' : '항목을 선택해 주세요',
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # HttpResponseRedirect 는 POST 와 세트 
#         # POST로 view 가 호출된 경우에는 HttpResponseRedirect 로 응답한다.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))