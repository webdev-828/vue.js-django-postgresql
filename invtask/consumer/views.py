# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from invtask.api.models import TwitterProfile


class Home(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        return {
            'profiles': TwitterProfile.objects.all()
        }
