from django.conf.urls import url, include

from invtask.consumer.views import Home

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^', include('invtask.api.urls')),
]
