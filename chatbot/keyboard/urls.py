from django.conf.urls import url
from keyboard import views

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.response),
]

