from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^/', include('thewall.urls')),
    url(r'^awards/', include('awards.urls')),
    url(r'^standalone/', include('standalone_models.urls'))
)
