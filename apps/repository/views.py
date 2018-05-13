from django.views.generic.base import TemplateView
import os
import requests

class RepositoryView(TemplateView):

    template_name = 'repository.html'
    username = os.environ.get('API_GITHUB_USERNAME')
    token = os.environ.get('API_GITHUB_PASS')

    def get(self, request, *args, **kwargs):
        auth = (self.username, self.token)
        list_repos = requests.get('https://api.github.com/orgs/githubtraining/repos', auth=auth).json()

        return self.render_to_response(self.get_context_data(list_repos = list_repos))

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)

        auth = (self.username, self.token)
        list_repos = kwargs.pop('list_repos')
        for repo in list_repos:
            commits_url = repo['commits_url'][:-6]
            commits = requests.get(commits_url, auth=auth).json()
            repo['last_commit_date'] = commits[0]['commit']['author']['date']

        context['repositories'] = list_repos

        return context
