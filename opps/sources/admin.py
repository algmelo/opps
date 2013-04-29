# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Source, ContainerSource
from opps.core.admin import PublishableAdmin


class SourceAdmin(PublishableAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name']
    list_filter = ['date_available', 'published']
    exclude = ('user',)
    search_fields = ['name', 'slug', 'url']

    fieldsets = (
        (_(u'Identification'), {
            'fields': ('site', 'name', 'slug')}),
        (_(u'Content'), {
            'fields': ('url', 'feed')}),
        (_(u'Publication'), {
            'classes': ('extrapretty'),
            'fields': ('published', 'date_available')}),
    )


class ContainerSourceInline(admin.TabularInline):
    model = ContainerSource
    fk_name = 'container'
    raw_id_fields = ['source']
    actions = None
    extra = 1
    fieldsets = [(None, {
        'classes': ('collapse',),
        'fields': ('source', 'order')})]


admin.site.register(Source, SourceAdmin)
