from django.conf.urls import patterns, include, url
from django.contrib import admin
from .app.views import UserProfileDetail

urlpatterns = patterns(
    '',
    url(r'^$', 'mygameslist.app.views.home', name='home'),
    url(r'^user/(?P<slug>[\w-]+)/$', UserProfileDetail.as_view()),
    url(r'^admin/', include(admin.site.urls)),
)
