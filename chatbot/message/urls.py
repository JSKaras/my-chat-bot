from django.conf.urls import url
from message import views

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^$', views.response, name='response'),
	url(r'^history/$', views.history_response, name='history'),
]

