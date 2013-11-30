from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'zscore.views.index'),
    url(r'^goal/add/$', 'zscore.views.goalAdd'),
    url(r'^priority/add/$', 'zscore.views.priorityAdd'),
    url(r'^goal/delete/$', 'zscore.views.goalDelete'),
    url(r'^priority/delete/$', 'zscore.views.priorityDelete'),
    url(r'^snapshot/add/$', 'zscore.views.snapshotAdd'),
    url(r'^snapshot/add/$', 'zscore.views.snapshotDelete'),


    # url(r'^$', 'Quantified.views.home', name='home'),
    # url(r'^Quantified/', include('Quantified.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
