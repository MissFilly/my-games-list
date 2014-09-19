from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .app.views import UserDetailView, GameDetailView, GameListByUserView, \
    ListEntryCreate

urlpatterns = patterns(
    '',
    url(r'^$', 'mygameslist.app.views.home', name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^user/(?P<slug>[\w-]+)/$', UserDetailView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^game/(?P<pk>\d+)/$', GameDetailView.as_view(), name='game_detail'),
    url(r'^list/(?P<slug>[-_\w]+)/$',
        GameListByUserView.as_view(), name='game_list_by_user'),
    url(r'^add/(?P<pk>\d+)/$', ListEntryCreate.as_view(), name='entry_create'),
)
