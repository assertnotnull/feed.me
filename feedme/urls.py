from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'appfeedme.views.index', name='index'),
    url(r'^search/(?P<category>.*)/(?P<location>.*)', 'appfeedme.views.search', name='search'),
    url(r'^search-wajam/(?P<resturant>.*)$', 'appfeedme.views.search_wajam', name='search_wajam'),
)
