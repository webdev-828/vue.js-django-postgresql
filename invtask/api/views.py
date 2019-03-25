# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.generic import View
from django.conf import settings
from requests_oauthlib import OAuth1

import requests


# http://flower.readthedocs.io/en/latest/api.html
# https://github.com/geduldig/TwitterAPI
# pip install requests-oauthlib
# installed oauthlib-2.0.2 requests-oauthlib-0.8.0
class Home(View):

    def get(self, *args, **kwargs):

        # url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        url = 'https://api.twitter.com/1.1/users/show.json?screen_name=bochenn'
        auth = OAuth1(
            settings.TWITTER_CLIENT_KEY,
            settings.TWITTER_CLIENT_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        r = requests.get(url, auth=auth)
        print(r.status_code)
        if (r.status_code == 200):
            print(r.json())

        response = HttpResponse('<h1>HERNAN</h1>')

        return response
