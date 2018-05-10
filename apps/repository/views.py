from django.views.generic.base import TemplateView

class RepositoryView(TemplateView):

    template_name = 'repository.html'

    def get_context_data(self, **kwargs):
        context = super(RepositoryView, self).get_context_data(**kwargs)
        return context
