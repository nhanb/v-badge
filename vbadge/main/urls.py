from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^manage/(?P<fid>.+)/(?P<token>.+)$', views.manage, name='manage'),
]
