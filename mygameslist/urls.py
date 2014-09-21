from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .app.views import *

urlpatterns = patterns(
    '',
    url(r'^$', 'mygameslist.app.views.home', name='home'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^user/(?P<slug>[\w-]+)/$', UserDetailView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    
    url(r'^(?P<pk>\d+)/detail/$', GameDetailView.as_view(),
        name='game_detail'),
    url(r'^list/(?P<slug>[-_\w]+)/$', GameListByUserView.as_view(),
        name='game_list_by_user'),
    url(r'^(?P<pk>\d+)/entry_create/$', ListEntryCreate.as_view(),
        name='entry_create'),
    # Reviews
    url(r'^(?P<pk>\d+)/review/$', GameReviewCreate.as_view(),
        name='review_create'),
    url(r'^review/(?P<pk>\d+)/update/$', GameReviewUpdate.as_view(),
        name='review_update'),
    # Recommendations
    url(r'^(?P<pk>\d+)/recommend/$', GameRecommendationCreate.as_view(),
        name='recommendation_create'),
)
