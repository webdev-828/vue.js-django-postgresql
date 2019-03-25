from __future__ import absolute_import

from requests_oauthlib import OAuth1
from django.conf import settings

from celery import shared_task, task

from .models import TwitterProfile
import requests
import time


@task
def get_profile(screen_name):
    """
    Main task in charge to connect with Twitter API to get the profile information.
    """
    try:
        profile = TwitterProfile.objects.get(screen_name=screen_name)
    except TwitterProfile.DoesNotExist:
        return False

    profile.status = TwitterProfile.IN_PROCESS
    profile.save()

    # if settings.DEBUG:
    #    time.sleep(settings.TASK_SLEEP)

    url = '%s/users/show.json?screen_name=%s' % (settings.TWITTER_API_URL, screen_name)
    auth = OAuth1(
        settings.TWITTER_CLIENT_KEY,
        settings.TWITTER_CLIENT_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    r = requests.get(url, auth=auth)
    if (r.status_code == requests.codes.ok):
        data = r.json()
        profile.name = data['name']
        profile.friends_count = data['friends_count']
        profile.followers_count = data['followers_count']
        profile.description = data['description']
        profile.profile_image_url = data['profile_image_url']
        profile.status = TwitterProfile.COMPLETE
        profile.save()

    else:
        # TODO: Add a reason field to store the failure description
        # or maybe we can add more FAILURE states.
        profile.status = TwitterProfile.FAILURE
        profile.save()

    return True


@task
def retry_failures(screen_name):
    """
    This task retry to obtain all twitter accounts that fails by some reason.
    Also retry get twitter accounts
    """
    return ''
