# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from opps.core.models import Publishable, ContainerThrough, Slugged


class Source(Publishable, Slugged):

    name = models.CharField(_(u"Name"), max_length=255)
    url = models.URLField(_(u'URL'), max_length=200, blank=True, null=True)
    feed = models.URLField(_(u'Feed URL'), max_length=200, blank=True,
                           null=True)

    def __unicode__(self):
        return self.slug


class ContainerSource(ContainerThrough):
    source = models.ForeignKey(
        'sources.Source',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_(u'Source'),
    )

    def __unicode__(self):
        return self.source.slug
