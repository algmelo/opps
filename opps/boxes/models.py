#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from django.conf import settings
#from django.utils.importlib import import_module
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

from opps.core.models import Publishable, Slugged, ContainerThrough


try:
    OPPS_APPS = tuple([(u"{0}.{1}".format(
        app._meta.app_label, app._meta.object_name), u"{0} - {1}".format(
            app._meta.app_label, app._meta.object_name))
        for app in models.get_models() if 'opps.' in app.__module__])
except ImportError:
    OPPS_APPS = tuple([])


class QuerySet(Publishable):
    name = models.CharField(_(u"Dynamic queryset name"), max_length=140)
    slug = models.SlugField(
        _(u"Slug"),
        db_index=True,
        max_length=150,
        unique=True,
    )

    model = models.CharField(_(u'Model'), max_length=150, choices=OPPS_APPS)
    limit = models.PositiveIntegerField(_(u'Limit'), default=7)
    order = models.CharField(_('Order'), max_length=1, choices=(
        ('-', 'DESC'), ('+', 'ASC')))
    channel = models.ForeignKey(
        'channels.Channel',
        verbose_name=_(u"Channel"),
    )


class BaseBox(Publishable, Slugged):
    name = models.CharField(_(u"Box name"), max_length=140)
    container = models.ForeignKey(
        'core.Container',
        null=True, blank=True,
        help_text=_(u'Only published container'),
        on_delete=models.SET_NULL
    )
    channel = models.ForeignKey(
        'channels.Channel',
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"{0}-{1}".format(self.slug, self.site.name)


class ContainerBox(BaseBox):

    containers = models.ManyToManyField(
        'core.Container',
        null=True, blank=True,
        related_name='containerbox_containers',
        through='boxes.ContainerBoxContainers'
    )
    queryset = models.ForeignKey(
        'boxes.QuerySet',
        null=True, blank=True,
        verbose_name=_(u'Query Set')
    )

    def get_queryset(self):
        _app, _model = self.queryset.model.split('.')
        model = models.get_model(_app, _model)

        queryset = model.objects.filter(published=True,
                                        date_available__lte=timezone.now())
        if self.queryset.channel:
            queryset = queryset.filter(channel=self.queryset.channel)
        queryset = queryset.order_by('{0}id'.format(self.queryset.order))[
            :self.queryset.limit]

        return queryset


class DynamicBox(BaseBox):

    dynamicqueryset = models.ForeignKey(
        'boxes.QuerySet',
        verbose_name=_(u'Query Set')
    )


class ContainerBoxContainers(ContainerThrough):
    containerbox = models.ForeignKey(
        'boxes.ContainerBox',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='containerboxcontainers_containerboxs',
        verbose_name=_(u'Container Box'),
    )

    def __unicode__(self):
        return u"{0}-{1}".format(self.containerbox.slug, self.container.slug)

    def clean(self):

        if not self.container.published:
            raise ValidationError(_(u'Container not published!'))

        if self.container.date_available >= timezone.now():
            raise ValidationError(_(u'Container date available is greater '
                                    u'than today!'))
