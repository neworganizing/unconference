from django.conf.urls import patterns, url
from standalone_models.views import ListOrganizations


urlpatterns = patterns(
    '',
    url(
        r'^/organizations$',
        ListOrganizations.as_view(),
        name="list_organizations"
    )
)
