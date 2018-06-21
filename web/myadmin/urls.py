from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^', views.index,name='myhome_index'),  
    url(r'^', views.index,name='admin_index'),
]
