from django.conf.urls import url
from .views import OWQuestion

urlpatterns = [
    url(r'onewordquestion/(?P<slug>[\w-]*)$', OWQuestion.as_view(), name='OWQ_Author'),
]

