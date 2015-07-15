from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from pinax.teams.models import Team

from lms.team_utils import create_teams


class Organization(models.Model):

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    administrators_team = models.ForeignKey(Team,
                                            help_text="To contain users who administer the organization.")

    def __unicode__(self):
        return self.name

    @classmethod
    def create(cls, created_by, name, slug, access):
        """
        See: https://docs.djangoproject.com/en/1.8/ref/models/instances/ for
        the reason why I'm doing this.

        The use case is simply, that upon instantiation of an Organization the
        expected administrators_team is also generated on-the-fly.
        """
        org = cls(created_by=created_by, name=name, slug=slug)
        return create_teams(org, created_by, access)
