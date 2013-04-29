# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Post, Album, Link, ArticleConfig
from opps.core.admin import PublishableAdmin
from opps.images.admin import ContainerImageInline
from opps.sources.admin import ContainerSourceInline

from redactor.widgets import RedactorEditor


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {'content': RedactorEditor()}


class ArticleAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ['get_http_absolute_url', 'short_url']
    raw_id_fields = ['main_image', 'channel']


class PostAdmin(ArticleAdmin):
    form = PostAdminForm
    inlines = [ContainerImageInline, ContainerSourceInline]
    raw_id_fields = ['main_image', 'channel', 'albums']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'title', 'slug', 'get_http_absolute_url',
                       'short_url')}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'content', 'main_image',
                       'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'albums',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class AlbumAdminForm(forms.ModelForm):
    class Meta:
        model = Album


class AlbumAdmin(ArticleAdmin):
    form = AlbumAdminForm
    inlines = [ContainerImageInline]

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'main_image', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class LinkAdmin(ArticleAdmin):
    raw_id_fields = ['containers', 'channel', 'main_image']
    fieldsets = (
        (_(u'Identification'), {
            'fields': ('title', 'slug', 'get_http_absolute_url',
                       'short_url',)}),
        (_(u'Content'), {
            'fields': ('short_title', 'headline', 'url', 'containers',
                       'main_image', 'tags')}),
        (_(u'Relationships'), {
            'fields': ('channel',)}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class ArticleConfigAdmin(PublishableAdmin):
    list_display = ['key', 'key_group', 'channel', 'date_insert',
                    'date_available', 'published']
    list_filter = ["key", 'key_group', "channel", "published"]
    search_fields = ["key", "key_group", "value"]


admin.site.register(Post, PostAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(ArticleConfig, ArticleConfigAdmin)
