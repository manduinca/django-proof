from django.views.generic.base import TemplateView
import requests

class RepositoryView(TemplateView):

    template_name = 'repository.html'

    def get(self, request, *args, **kwargs):
        list_repos = requests.get('https://api.github.com/orgs/githubtraining/repos').json()

        return self.render_to_response(self.get_context_data(list_repos = list_repos))

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)

        list_repos = kwargs.pop('list_repos')
        for repo in list_repos:
            commits_url = repo['commits_url'][:-6]
            commits = requests.get(commits_url).json()
            repo['commit'] = commits[0]

        context['repositories'] = list_repos

        return context
