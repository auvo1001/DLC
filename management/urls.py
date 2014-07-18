from django.conf.urls import patterns, url
from management import views
from django.conf import settings


urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^add_package/$', views.add_package, name='add_package'),
    url(r'^add_sender/$', views.add_sender, name='add_sender'),
    url(r'^sender/(?P<sender_url>\w+)/add_receiver/$', views.add_receiver, name='add_receiver'),
    url(r'^sender/(?P<sender_url>\w+)/$', views.detail_sender, name='detail_sender'),
    url(r'^sender/(?P<sender_url>\w+)/receiver/(?P<receiver_url>\w+)/$', views.detail_receiver, name='detail_receiver'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^login/$',views.login_view,name='login'),
    )








if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
