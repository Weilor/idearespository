from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Questions, Choice
from django.core.urlresolvers import reverse
from django.views import generic

# Create your views here.


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Questions.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Questions
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Questions
    template_name = "polls/results.html"


def index(request):
    latest_question_list = Questions.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context_page = {
        "latest_question_list" : latest_question_list,
    }
    return HttpResponse(template.render(context_page, request))


def detail(request, question_id):
    try:
        question = Questions.objects.get(pk=question_id)
    except Questions.DoesNotExist:
        raise Http404("Question does not exist.")
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"error_message": "you did not pick a choice",
                                                     "question": question})
    else:
        choice.votes += 1
        choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
