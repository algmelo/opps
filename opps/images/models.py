# -*- coding: utf-8 -*-
import uuid
import os
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager

from opps.core.models import Publishable, ContainerThrough, Slugged


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{0}-{1}.{2}".format(uuid.uuid4(), instance.slug, ext)
    d = datetime.now()
    folder = "images/{0}".format(d.strftime("%Y/%m/%d/"))
    return os.path.join(folder, filename)


class TaggedImage(TaggedItemBase):
    """Tag for images """
    content_object = models.ForeignKey('images.Image')
    pass


class Image(Publishable, Slugged):

    title = models.CharField(_(u"Title"), max_length=140, db_index=True)
    image = models.ImageField(upload_to=get_file_path)
    description = models.TextField(_(u"Description"), null=True, blank=True)
    tags = TaggableManager(blank=True, through=TaggedImage)

    source = models.ForeignKey('sources.Source', null=True, blank=True)

    def __unicode__(self):
        return u"{0}".format(self.slug)

    def get_absolute_url(self):
        if self.date_available <= timezone.now() and self.published:
            return self.image.url
        return u""


class ContainerImage(ContainerThrough):
    image = models.ForeignKey(
        'images.Image',
        verbose_name=_(u'Image'),
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.image.title
