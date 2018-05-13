from django.db import models


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


class Repository(models.Model):

    organization = models.ForeignKey(
        Organization,
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
