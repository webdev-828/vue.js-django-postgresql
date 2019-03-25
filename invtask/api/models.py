# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TwitterProfileManager(models.Manager):
    """ QuerySet manager for TwitterProfile class to add non-database fields.

    A @property in the model cannot be used because QuerySets (eg. return
    value from .all()) are directly tied to the database Fields -
    this does not include @property attributes.
    Instead we need Inject an annotated field.

    Annotated field is calculated as this:
    SELECT
        tp.screen_name,
        tp.followers_count,
        (SELECT count(*) + 1 FROM twitter_profile ttp WHERE ttp.followers_count > tp.followers_count) AS popularity
    FROM twitter_profile tp;
    """

    def get_ranked_queryset(self):
        """ Annotate a calculated rank field based on followers_count  """

        qs = super(TwitterProfileManager, self).get_queryset()
        qs = qs.extra(
            select={'rank': 'SELECT COUNT(*) + 1 FROM twitter_profile tp WHERE tp.followers_count > "twitter_profile".followers_count'})
        qs = qs.extra(order_by=['rank'])
        # print(qs.query)

        return qs


class TwitterProfile(models.Model):
    """
    User profile from Twitter is represented by this model.
    This will be filled in with response from Twitter API.

    screen_name is required. Other fields are optional.
    status options are:
        -   0.Queued: The profile is in queue waiting for processing
        -   1.In Process: The profile was requested to Twitter
        -   2.Complete: The profile is available
        -   3.Unavailable: The profile was suspended or deactivated in twitter
        -   4.Failure: Ups, something went wrong. Retry
    """
    QUEUED, IN_PROCESS, COMPLETE, UNAVAILABLE, FAILURE = range(5)

    STATUS_CHOICES = (
        (QUEUED, 'Queued'),
        (IN_PROCESS, 'In Process'),
        (COMPLETE, 'Complete'),
        (UNAVAILABLE, 'Unavailable'),
        (FAILURE, 'Failure'),
    )

    status = models.SmallIntegerField(
        _('Status'), choices=STATUS_CHOICES, default=QUEUED)
    created_at = models.DateTimeField(_('Created'), auto_now_add=True)
    screen_name = models.CharField(
        _('Screen name'),
        max_length=50,
        unique=True)
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))
    profile_image_url = models.URLField(_('Image'), max_length=300, null=True)
    followers_count = models.PositiveIntegerField(_('Followers'), default=0)
    friends_count = models.PositiveIntegerField(_('Friends'), default=0)
    # use custom manager
    objects = TwitterProfileManager()

    class Meta:
        db_table = 'twitter_profile'
        ordering = ['-followers_count', ]

    @property
    def popularity(self):
        return TwitterProfile.objects.filter(followers_count__gt=self.followers_count).count() + 1

    def status_class(self):
        classes = ['warning', 'warning', 'success', 'danger', 'danger']
        assert len(classes) == len(self.STATUS_CHOICES)
        return classes[self.status]

    def __unicode__(self):
        return self.name
