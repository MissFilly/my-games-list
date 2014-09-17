from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .app.views import UserDetailView, GameDetailView

urlpatterns = patterns(
    '',
    url(r'^$', 'mygameslist.app.views.home', name='home'),
    url(r'^user/(?P<slug>[\w-]+)/$', UserDetailView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^game/(?P<pk>\d+)/$', GameDetailView.as_view(), name='game-detail'),
    url(r'^(?P<slug>[-_\w]+)/$', UserDetailView.as_view(), name='user-detail'),
)
