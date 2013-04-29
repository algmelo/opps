# -*- coding: utf-8 -*-
from django.utils import timezone

from opps.core.models import Container
from opps.boxes.models import ContainerBox


def set_context_data(self, SUPER, **kwargs):
    context = super(SUPER, self).get_context_data(**kwargs)

    container = Container.objects.filter(
        site=self.site,
        channel_long_slug__in=self.channel_long_slug,
        date_available__lte=timezone.now(),
        published=True)
    context['posts'] = container.filter(child_class='Post')[:self.limit]
    context['albums'] = container.filter(child_class='Album')[:self.limit]

    context['channel'] = {}
    context['channel']['long_slug'] = self.long_slug
    if self.channel:
        context['channel']['level'] = self.channel.get_level()
        context['channel']['root'] = self.channel.get_root()

    context['containerboxes'] = ContainerBox.objects.filter(
        channel__long_slug=self.long_slug)
    if self.slug:
        context['containerboxes'] = context['containerboxes'].filter(
            container__slug=self.slug)

    return context
