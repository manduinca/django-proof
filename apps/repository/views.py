from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from apps.repository.models import Organization, Repository
from apps.repository.forms import FormOrganization
import os
import requests


class SearchOrganizationView(TemplateView):

    template_name = 'search_organization.html'
    auth = (os.environ.get('API_GITHUB_USERNAME'),
            os.environ.get('API_GITHUB_PASS'))
    api = 'https://api.github.com/'

    def get(self, request, *args, **kwargs):
        form = FormOrganization()
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = FormOrganization(request.POST)
        if not form.is_valid():
            return self.render_to_response({'form': form})
        data = form.cleaned_data
        organization = self.get_db_organization(data['organization'])
        if not organization:
            organization = self.get_api_organization(data['organization'])
        if not organization:
            return self.render_to_response({'form': form})

        repository_url = reverse('repository', args=(organization.id,))
        return HttpResponseRedirect(repository_url)

    def get_db_organization(self, login):
        try:
            organization = Organization.objects.get(login=login)
        except Organization.DoesNotExist:
            return None
        else:
            return organization

    def get_api_organization(self, login):
        request = requests.get(self.api + 'orgs/' + login, auth=self.auth)
        if request.status_code == 200:
            organization = request.json()
            return self.save_db(organization)
        return None

    def save_db(self, org):
        if 'name' not in org or not org['name']:
            org['name'] = ''
        if 'html_url' not in org or not org['html_url']:
            org['html_url'] = ''
        if 'location' not in org or not org['location']:
            org['location'] = ''
        organization = Organization.objects.create(name = org['name'],
            login = org['login'], url = org['html_url'], location = org['location'],
            created_at = org['created_at'], updated_at = org['updated_at']
        )
        url_repos = self.api + 'orgs/' + org['login'] + '/repos'
        repos = requests.get(url_repos, auth=self.auth).json()
        for repo in repos:
            last_commit_url = repo['commits_url'][:-6] + '/master'
            last_commit = requests.get(last_commit_url, auth=self.auth).json()
            if last_commit:
                last_commit_date = last_commit['commit']['author']['date']
            else:
                last_commit_date = ''
            if 'html_url' not in org or not org['html_url']:
                org['html_url'] = ''
            if 'commits_url' not in org or not org['commits_url']:
                org['commits_url'] = ''
            Repository.objects.create(organization = organization,
                name = repo['name'], github_id = repo['id'],
                url = repo['html_url'], last_commit = last_commit_date,
                commits_url = repo['commits_url'],
                created_at = repo['created_at'],
                updated_at = repo['updated_at']
            )
        return organization


class RepositoryView(TemplateView):

    template_name = 'repository.html'

    def get(self, request, org_id, *args, **kwargs):
        repos = Repository.objects.filter(organization=org_id)
        return self.render_to_response(self.get_context_data(repos = repos))

    def get_context_data(self, **kwargs):
        repos = kwargs.pop('repos')
        context = super(RepositoryView, self).get_context_data(**kwargs)
        context['repositories'] = repos
        return context
