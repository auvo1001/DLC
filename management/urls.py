from django.conf.urls import patterns, url
from management import views
from django.conf import settings


urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
    url(r'^add_package/$', views.add_package, name='add_package'),
    url(r'^reorder_package/(?P<sender_url>\w+)/(?P<receiver_url>\w+)/$', views.reorder_package, name='reorder_package'),
    url(r'^sender/edit_sender/(?P<sender_url>\w+)/$', views.edit_sender, name='edit_sender'),
    url(r'^receiver/edit_receiver/(?P<receiver_url>\w+)/$', views.edit_receiver, name='edit_receiver'),
    url(r'^package/edit_package/(?P<package_url>\w+)/$', views.edit_package, name='edit_package'),
    url(r'^sender/(?P<sender_url>\w+)/$', views.detail_sender, name='detail_sender'),
    url(r'^receiver/(?P<receiver_url>\w+)/$', views.detail_receiver, name='detail_receiver'),
    url(r'^package/(?P<package_url>\w+)/$', views.detail_package, name='detail_package'),
    url(r'^test/$', views.report_lab, name='report_lab'),
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^login/$',views.login_view,name='login'),
    url(r'search/$',views.search,name='search'),
    )








if settings.DEBUG:
        urlpatterns += patterns(
                'django.views.static',
                (r'media/(?P<path>.*)',
                'serve',
                {'document_root': settings.MEDIA_ROOT}), )
