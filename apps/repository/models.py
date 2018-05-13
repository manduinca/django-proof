from django.db import models
from django.utils.translation import ugettext_lazy as _


class Organization(models.Model):

    name = models.CharField(
        max_length=100,
    )

    login = models.CharField(
        max_length=100,
    )

    url = models.URLField()

    location = models.CharField(
        max_length=200,
    )

    created_at = models.DateTimeField()

    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'organization'
        indexes = [
            models.Index(fields=['login'])
        ]
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')


class Repository(models.Model):

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
    )

    github_id = models.PositiveIntegerField()

    name = models.CharField(
        max_length = 100,
    )

    url = models.URLField()

    last_commit = models.DateTimeField()

    commits_url = models.URLField()

    created_at = models.DateTimeField()

    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'repository'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_commit'])
        ]
        verbose_name = _('repository')
        verbose_name_plural = _('repositories')
