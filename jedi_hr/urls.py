from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from jedi_hr.views import IndexView, CandidateCreate, CandidateQuiz, JediList, JediDetail, JediCandidate

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^candidate_new/$', CandidateCreate.as_view(), name='candidate_new'),
    url(r'^candidate_quiz/(?P<candidate_pk>[^/]+)/$', CandidateQuiz.as_view(), name='candidate_quiz'),
    url(r'^jedi_list/$', JediList.as_view(), name='jedi_list'),
    url(r'^jedi/(?P<pk>[^/]+)/$', JediDetail.as_view(), name='jedi_detail'),
    url(r'^jedi/(?P<pk>[^/]+)/candidate/(?P<candidate_pk>[^/]+)/$', JediCandidate.as_view(), name='jedi_candidate'),
]
