from django.conf.urls import url
from apps.repository.views import RepositoryView

urlpatterns = [
    url(r'^repository', RepositoryView.as_view(), name = 'repository')
]
