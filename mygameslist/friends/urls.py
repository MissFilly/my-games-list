from django.conf.urls import patterns, include, url
from .views import *

urlpatterns = patterns(
    '',
    url(r'^add/(?P<pk>\d+)/$', FriendRequestView.as_view(),
        name='friend_add'),
    url(r'^requests/$', ReceivedRequestsView.as_view(),
        name='friend_requests'),
    url(r'^requests/(?P<action>[-_\w]+)/(?P<pk>\d+)/$',
        FriendshipRequestAction.as_view(), name='friend_request_action'),
    url(r'^list/$', FriendListView.as_view(),
        name='friend_list'),
    url(r'^delete/(?P<pk>\d+)/$', FriendDeleteView.as_view(),
        name='friend_delete'),
)
