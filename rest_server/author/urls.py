from django.conf.urls import url
from .views import OWQuestion, SCQuestion, MCQuestion

urlpatterns = [
    url(r'onewordquestion/(?P<slug>[\w-]*)$', OWQuestion.as_view(), name='OWQ_Author'),
    url(r'singlechoicequestion/(?P<slug>[\w-]*)$', SCQuestion.as_view(), name='SCQ_Author'),
    url(r'multichoicequestion/(?P<slug>[\w-]*)$', MCQuestion.as_view(), name='MCQ_Author')
]


