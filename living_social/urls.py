from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'data_challenge.views.index'),
                       url(r'success', 'data_challenge.views.success'),
                       url(r'upload', 'data_challenge.views.upload'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout'),
                       url(r'^openid/', include('django_openid_auth.urls'))
    # Examples:
    # url(r'^$', 'living_social.views.home', name='home'),
    # url(r'^living_social/', include('living_social.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
