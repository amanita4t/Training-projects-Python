from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from .models import Question, Choice
from django.urls import reverse

# Create your views here.
def index(request):
    question = Question.objects.order_by("-pub_date")[:5]
    return render(request, {"question": question})   

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question" : question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk= question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render (
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"you didnt select a choice",
            }
        )
    else:
        selected_choice.vote = F("votes") + 1
        selected_choice.save()

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
