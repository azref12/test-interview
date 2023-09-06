from django.conf.urls import url
from user import views

urlpatterns = [
    url (r'user/$', views.UserUpload),
    url (r'user/(?P<pk>[0-9]+)$', views.UserUpdate),
    url (r'delete_user/(?P<pk>[0-9]+)$', views.DeleteUser),
    url (r'fetch/$', views.UserFetch),
    url(r'v1/', views.getKeyApi),
]
