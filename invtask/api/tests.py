from django.test import TestCase

from tastypie.test import ResourceTestCaseMixin

from .models import TwitterProfile
from .tasks import get_profile


class TwitterProfileResourceTest(ResourceTestCaseMixin, TestCase):
    # fixtures = ['test_entries.json']

    def setUp(self):
        super(TwitterProfileResourceTest, self).setUp()

    def test_failure(self):
        # resp = self.api_client.get('/api/v1/profile/__carlos/', format='json')
        # self.assertValidJSONResponse(resp)

        # resp = self.api_client.get('/api/v1/profile/darth-vader/', format='json')
        # self.assertValidJSONResponse(resp)
        TwitterProfile.objects.create(screen_name="___")
        self.assertTrue(get_profile('___'))

    def test_processing(self):
        resp = self.api_client.get('/api/v1/profile/darth_vader/', format='json')
        self.assertValidJSONResponse(resp)
        self.assertEqual(self.deserialize(resp)['message'], 'Processing Request')

    def test_rank_annotation(self):
        TwitterProfile.objects.create(screen_name="u1", followers_count=505)
        TwitterProfile.objects.create(screen_name="u3", followers_count=182)
        TwitterProfile.objects.create(screen_name="u4", followers_count=113)
        TwitterProfile.objects.create(screen_name="u6", followers_count=113)
        TwitterProfile.objects.create(screen_name="u5", followers_count=12)
        TwitterProfile.objects.create(screen_name="u2", followers_count=202)
        qs = TwitterProfile.objects.get_ranked_queryset()
        for item in qs:
            self.assertEqual(item.popularity, item.rank)

        self.assertEqual(qs.first().screen_name, 'u1')
        self.assertEqual(qs.last().screen_name, 'u5')

    def test_popularity(self):
        TwitterProfile.objects.create(screen_name="u1", followers_count=505, status=TwitterProfile.COMPLETE)
        TwitterProfile.objects.create(screen_name="u3", followers_count=182, status=TwitterProfile.COMPLETE)
        TwitterProfile.objects.create(screen_name="u4", followers_count=113, status=TwitterProfile.COMPLETE)
        TwitterProfile.objects.create(screen_name="u6", followers_count=113, status=TwitterProfile.COMPLETE)
        TwitterProfile.objects.create(screen_name="u5", followers_count=12, status=TwitterProfile.COMPLETE)
        TwitterProfile.objects.create(screen_name="u2", followers_count=202, status=TwitterProfile.COMPLETE)
        TwitterProfile.objects.all()

        resp = self.api_client.get('/api/v1/profile/', format='json')
        self.assertValidJSONResponse(resp)

        objects = self.deserialize(resp)['objects']
        self.assertEqual(len(objects), 6)

        self.assertEqual(objects[0]['screen_name'], 'u1')
        self.assertEqual(objects[-1]['screen_name'], 'u5')
