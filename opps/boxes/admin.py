#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import QuerySet, DynamicBox, ContainerBox, ContainerBoxContainers
from opps.core.admin import PublishableAdmin


class QuerySetAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    raw_id_fields = ['channel']
    exclude = ('user',)

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Rules'), {
            'fields': ('model', 'order', 'limit', 'channel')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class DynamicBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    exclude = ('user',)
    raw_id_fields = ['channel', 'container', 'dynamicqueryset']
    search_fields = ['name', 'slug']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'container', 'dynamicqueryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class ContainerBoxContainersInline(admin.TabularInline):
    model = ContainerBoxContainers
    fk_name = 'containerbox'
    raw_id_fields = ['container']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('container', 'order')})]


class ContainerBoxAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ["name"]}
    list_display = ['name', 'date_available', 'published']
    list_filter = ['date_available', 'published']
    inlines = [ContainerBoxContainersInline]
    raw_id_fields = ['channel', 'container', 'queryset']
    search_fields = ['name', 'slug']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Relationships'), {
            'fields': ('channel', 'container', 'queryset')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


admin.site.register(QuerySet, QuerySetAdmin)
admin.site.register(DynamicBox, DynamicBoxAdmin)
admin.site.register(ContainerBox, ContainerBoxAdmin)
