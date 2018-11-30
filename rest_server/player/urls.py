from django.conf.urls import url
from .views import Quiz, GetScore

urlpatterns = [
    url(r'quiz$', Quiz.as_view(), name='quiz'),
    url(r'score$', GetScore.as_view(), name='score')
]

