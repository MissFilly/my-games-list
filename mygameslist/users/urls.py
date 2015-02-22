from django.conf.urls import patterns, url
from .views import UserDetailView, UserReviewsView, UserRecommendationsView, UserProfileUpdate

urlpatterns = patterns(
    '',
    url(r'^(?P<slug>[\w-]+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/reviews/$', UserReviewsView.as_view(), name='reviews'),
    url(r'^(?P<slug>[\w-]+)/recommendations/$', UserRecommendationsView.as_view(), name='recommendations'),
    url(r'^profile/edit/$', UserProfileUpdate.as_view(), name='profile_update'),
)