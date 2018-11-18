from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from .views import SignUp, GetRole

urlpatterns = [
    url(r'^signup$', SignUp.as_view(), name='signup'),
    url(r'^token$', obtain_jwt_token, name='token'),
    url(r'^get_role', GetRole.as_view(), name='name')
]
