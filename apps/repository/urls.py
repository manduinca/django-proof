from django.conf.urls import url
from apps.repository.views import RepositoryView, SearchOrganizationView

urlpatterns = [
    url(r'^$', SearchOrganizationView.as_view(), name = 'search-organization'),
    url(r'^repository/(?P<org_id>\d+)/$', RepositoryView.as_view(), name = 'repository')
]
