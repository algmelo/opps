# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.redirects.models import Redirect

from taggit.managers import TaggableManager
from googl.short import GooglUrlShort

from opps.core.models import BaseConfig
from opps.core.models import Container


class Article(Container):

    headline = models.TextField(_(u"Headline"), null=True, blank=True)
    short_title = models.CharField(
        _(u"Short title"),
        max_length=140,
        null=True, blank=False,
    )
    short_url = models.URLField(
        _("Short URL"),
        null=True, blank=False,
    )
    tags = TaggableManager(blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.get_absolute_url()

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = GooglUrlShort(self.get_http_absolute_url())\
                .short()

    def get_absolute_url(self):
        return "/{0}/{1}".format(self.channel.long_slug, self.slug)

    def get_http_absolute_url(self):
        return "http://{0}/{1}".format(self.channel, self.slug)
    get_http_absolute_url.short_description = 'URL'

    def recommendation(self):
        return [a for a in Article.objects.filter(
            tags__in=self.tags.all()).exclude(pk=self.pk)[:10]]


class Post(Article):
    content = models.TextField(_(u"Content"))
    albums = models.ManyToManyField(
        'articles.Album',
        null=True, blank=True,
        related_name='post_albums',
    )

    def all_images(self):
        imgs = super(Post, self).all_images()

        imgs += [i for a in self.albums.filter(
            published=True, date_available__lte=timezone.now())
            for i in a.images.filter(published=True,
                                     date_available__lte=timezone.now())]
        return list(set(imgs))


class Album(Article):
    def get_absolute_url(self):
        return "/album/{0}/{1}".format(self.channel.long_slug, self.slug)

    def get_http_absolute_url(self):
        protocol, path = "http://{0}/{1}".format(
            self.channel, self.slug).split(self.site.domain)
        return "{0}{1}/album{2}".format(protocol, self.site, path)


class Link(Article):
    url = models.URLField(_(u"URL"), null=True, blank=True)
    containers = models.ForeignKey(
        'core.Container',
        null=True, blank=True,
        related_name='link_container'
    )

    def get_absolute_url(self):
        return "/link/{0}/{1}".format(self.channel.long_slug, self.slug)

    def get_http_absolute_url(self):
        protocol, path = "http://{0}/{1}".format(
            self.channel, self.slug).split(self.site.domain)
        return "{0}{1}/link{2}".format(protocol, self.site, path)

    def clean(self):
        if not self.url and not self.containers:
            raise ValidationError(_('URL field is required.'))

        if self.containers:
            self.url = self.containers.get_http_absolute_url()

    def save(self, *args, **kwargs):
        obj, create = Redirect.objects.get_or_create(
            old_path=self.get_absolute_url(), site=self.site)
        obj.new_path = self.url
        obj.save()
        super(Link, self).save(*args, **kwargs)


class ArticleConfig(BaseConfig):
    """
    Default implementation
    """
    pass
