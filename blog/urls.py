from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^user/get/(?P<identity>[-\w]*)$', views.get_user),
    url(r'^user/get_full/(?P<identity>[-\w]*)$', views.get_full_user),
    url(r'^user/get_all_subscriptions/(?P<identity>[-\w]*)$', views.get_all_subscriptions),
    url(r'^user/find_by_name/(?P<name>\w*)$', views.find_users_by_name),
    url(r'^user/subscribe$', views.subscribe, {'user': '', 'subscriber': ''}),
    url(r'^user/unsubscribe$', views.unsubscribe, {'user': '', 'subscriber': ''}),
    url(r'^user/delete/(?P<identity>[-\w]*)$', views.delete_user),
    url(r'^user/create$', views.create_user),
    url(r'^user/update$', views.update_user),
    url(r'^user/create_post$', views.create_post),
    url(r'^user/update_post$', views.create_post),
    url(r'^user/delete_post/(?P<identity>\d+)$', views.delete_post),
    url(r'^user/comment/create$', views.create_comment),
    url(r'^user/comment/delete/(?P<identity>\d+)$', views.delete_comment),
]
