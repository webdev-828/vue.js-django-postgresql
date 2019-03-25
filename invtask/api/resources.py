from django.conf.urls import url

from tastypie import fields
from tastypie.resources import ModelResource

from .tasks import get_profile
from .models import TwitterProfile


class TwitterProfileResource(ModelResource):
    popularity = fields.IntegerField(readonly=True)

    class Meta:
        queryset = TwitterProfile.objects.all()
        resource_name = 'profile'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<screen_name>\w+)/$" %
                self._meta.resource_name,
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def obj_get(self, bundle, **kwargs):
        try:
            profile = TwitterProfile.objects\
                .get(screen_name=kwargs['screen_name'])
        except TwitterProfile.DoesNotExist:
            profile = TwitterProfile(screen_name=kwargs['screen_name'])
            profile.save()
            get_profile.delay(kwargs['screen_name'])

        return profile

    def dehydrate(self, bundle):
        """
        Return custom message
        """
        if bundle.obj is None:
            bundle.data = {'message': 'Processing Request'}
        elif bundle.obj.status in [TwitterProfile.QUEUED,
                                TwitterProfile.IN_PROCESS]:
            del bundle.data
            bundle.data = {'message': 'Processing Request'}
        elif bundle.obj.status == TwitterProfile.FAILURE:
            del bundle.data
            bundle.data = {'message': 'Error Processing Request'}
        return bundle

    def dehydrate_status(self, bundle):
        """
        Show status description instead of status value
        """
        if bundle.obj:
            return bundle.obj.get_status_display()
        return None

    def dehydrate_popularity(self, bundle):
        """
        Inject popularity field based on user followers_count
        """
        idx = 0
        if bundle.obj:
            idx = TwitterProfile.objects.filter(followers_count__gt=bundle.obj.followers_count).count() + 1
        return idx
