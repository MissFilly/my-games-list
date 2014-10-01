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
    url(r'^user/(?P<slug>[\w-]+)/$', UserDetailView.as_view(),
        name='user_profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^(?P<pk>\d+)/$', GameDetailView.as_view(),
        name='game_detail'),
    url(r'^(?P<pk>\d+)/reviews/$', GameReviewByGameView.as_view(),
        name='game_review_by_game'),
    url(r'^(?P<pk>\d+)/recommendations/$', GameRecommendationByGame.as_view(),
        name='game_recommendation_by_game'),

    url(r'^list/(?P<slug>[-_\w]+)/$', GameListByUserView.as_view(),
        name='game_list_by_user'),
    url(r'^user/(?P<slug>[-_\w]+)/reviews$', GameReviewByUserView.as_view(),
        name='game_review_by_user'),
    url(r'^user/(?P<slug>[-_\w]+)/recommendations$',
        GameRecommendationByUserView.as_view(),
        name='game_recommendation_by_user'),
    url(r'^(?P<pk>\d+)/entry_create/$', ListEntryCreate.as_view(),
        name='entry_create'),

    url(r'^entry/(?P<pk>\d+)/delete/$', ListEntryDelete.as_view(),
        name='entry_delete'),
    # Reviews
    url(r'^(?P<pk>\d+)/review/$', GameReviewCreate.as_view(),
        name='review_create'),
    url(r'^review/(?P<pk>\d+)/update/$', GameReviewUpdate.as_view(),
        name='review_update'),
    url(r'^review/(?P<pk>\d+)/delete/$', GameReviewDelete.as_view(),
        name='review_delete'),
    # Recommendations
    url(r'^(?P<pk>\d+)/recommend/$', GameRecommendationCreate.as_view(),
        name='recommendation_create'),
    url(r'^recommendation/(?P<pk>\d+)/update/$', GameRecommendationUpdate.as_view(),
        name='recommendation_update'),
)
