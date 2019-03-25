from django.conf.urls import url, include

from tastypie.api import Api

from .views import Home
from .resources import TwitterProfileResource

v1_api = Api(api_name='v1')
v1_api.register(TwitterProfileResource())

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^api/', include(v1_api.urls)),
]
