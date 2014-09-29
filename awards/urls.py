from django.conf.urls import patterns, url
from awards.views import SubmitNominee, DisplayNominee

# http://neworganizing.rootscamp.org/awards/<rootscampslug>/<awardtype>/{{
# OR submit OR update }}
# http://neworganizing.rootscamp.org/awards/

urlpatterns = patterns(
    '',
    url(
        r'^edit',
        'awards.views.nominee_update_award',
        name='nominee_update_award'
    ),
    url(
        r'^(?P<unconference>[A-Za-z0-9\-\_]+)/(?P<award>[A-Za-z0-9\-\_]+)?/?$',
        'awards.views.list_award_nominees',
        name='list_award_nominees'
    ),
    url(
        r'^(?P<unconference>[A-Za-z0-9\_\-]+)/(?P<award>[A-Za-z0-9\_\-]+)/'\
        'entry/(?P<slug>[A-Za-z0-9\_\-]+)?/$',
        DisplayNominee.as_view(),
        name='display_nominee'
    ),
    url(
        r"""
            ^(?P<unconference>[A-Za-z0-9\_\-]+)/(?P<award>[A-Za-z0-9\_\-]+)
            /edit/(?P<slug>[A-Za-z0-9\_\-]+)/$
        """,
        'awards.views.nominee_update_award_form',
        name='nominee_update_award_form'
    ),
    url(
        r'^(?P<unconference>[A-Za-z0-9\_\-]+)/(?P<award>[A-Za-z0-9\_\-]+)/submit/$',
        SubmitNominee.as_view(), name='submit_nominee'
    ),
    url(
        r"""
            ^(?P<unconference>[A-Za-z0-9_-]+)?/mvt/entry/?
            (?P<slug>[A-Za-z0-9_-]+)?/$
        """,
        'awards.views.display_mvt', name='view_mvt'
    ),

    # MVC
    url(
        r"""
            ^(?P<unconference>[A-Za-z0-9_-]+)?/mvc/entry/?
            (?P<slug>[A-Za-z0-9_-]+)?/$
        """,
        'awards.views.display_mvc', name='view_mvc'
    ),
)
