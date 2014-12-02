from django.conf.urls import patterns, url
from treegenerator import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^result/$', views.result, name='result'),
	url(r'^multiple_results/$', views.pick_results, name='pick_results'),
    url(r'^ping/$', views.ping, name='ping'),
)

'''url(r'^test/$', views.ete_prototype, name='ete_prototype'),'''

