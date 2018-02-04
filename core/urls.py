from django.conf.urls import url
from . import views
from .views import FileUploadClass
urlpatterns = [
	url(r'^$', views.home, name='Open Home'),
	url(r'^queryfile$', FileUploadClass.as_view(), name='PDF upload and query'),

]
