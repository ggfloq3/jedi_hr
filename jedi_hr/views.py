from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from jedi_hr.forms import CandidateQuizForm, JediCandidateForm
from jedi_hr.models import Candidate, CandidateAnswer, Jedi


class IndexView(TemplateView):
    template_name = 'jedi_hr/index.html'


class CandidateCreate(CreateView):
    model = Candidate
    fields = ('name', 'age', 'email', 'planet')
    template_name = 'jedi_hr/candidate_create.html'

    def get_success_url(self):
        return reverse('candidate_quiz', args=[self.object.pk])


class CandidateQuiz(FormView):
    form_class = CandidateQuizForm
    template_name = 'jedi_hr/quiz.html'

    def get_success_url(self):
        return reverse('candidate_quiz', args=[self.kwargs['candidate_pk']])

    def get_form_kwargs(self):
        form_kwargs = super(CandidateQuiz, self).get_form_kwargs()
        # передаём в форму кандидата, создаём для него вопросы
        try:
            form_kwargs['candidate'] = Candidate.objects.get(id=self.kwargs['candidate_pk'])
        except Candidate.DoesNotExist:
            raise Http404('candidate not found')
        return form_kwargs

    def form_valid(self, form):
        # создание ответов пользователя
        answers = []
        for x in form.cleaned_data:
            data = {'question_id': int(x.split('_')[1]),
                    'answer': form.cleaned_data[x],
                    'candidate_id': self.kwargs['candidate_pk'], }
            answers.append(CandidateAnswer(**data))
        CandidateAnswer.objects.bulk_create(answers)
        return super(CandidateQuiz, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CandidateQuiz, self).get_context_data(**kwargs)
        context['already_answered'] = Candidate.objects.get(id=self.kwargs['candidate_pk']).candidateanswer_set.exists()
        return context


class JediList(ListView):
    model = Jedi
    template_name = 'jedi_hr/jedi_list.html'

    def get_context_data(self, **kwargs):
        context = super(JediList, self).get_context_data(**kwargs)
        if self.request.GET.get('padawans'):
            context['jedi_list'] = Jedi.objects.annotate(padawan_count=Count('candidate')).filter(padawan_count__gt=1)
        if self.request.GET.get('show_count'):
            context['show_count'] = True
            context['jedi_list'] = Jedi.objects.annotate(padawan_count=Count('candidate'))
        return context


class JediDetail(DetailView):
    model = Jedi
    template_name = 'jedi_hr/jedi_detail.html'

    def get_context_data(self, **kwargs):
        context = super(JediDetail, self).get_context_data(**kwargs)
        context['candidates'] = Candidate.objects.filter(
            planet=self.object.planet, jedi_master__isnull=True).annotate(Count('candidateanswer'))
        return context


class JediCandidate(UpdateView):
    model = Candidate
    pk_url_kwarg = 'candidate_pk'
    template_name = 'jedi_hr/candidate_jedi.html'
    form_class = JediCandidateForm

    def get_success_url(self):
        return reverse('jedi_candidate', args=[self.kwargs['pk'], self.kwargs['candidate_pk']])

    def form_valid(self, form):
        # отправка письма
        # email = EmailMessage('title', 'Вы зачислены', to=[self.object.email])
        # email.send()
        return super(JediCandidate, self).form_valid(form)

    def get_form_kwargs(self):
        form_kwargs = super(JediCandidate, self).get_form_kwargs()
        # передаём jedi_id в форму, для создания скрытого инпута
        form_kwargs['jedi_id'] = self.kwargs['pk']
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(JediCandidate, self).get_context_data(**kwargs)
        context['answers'] = self.object.candidateanswer_set.all().select_related('question')
        return context
