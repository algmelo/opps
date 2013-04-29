#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from django_thumbor import generate_url

from .models import Container


class PublishableAdmin(admin.ModelAdmin):
    """
    Overrides standard admin.ModelAdmin save_model method
    It sets user (author) based on data from requet.
    """
    list_display = ['title', 'channel_name', 'date_available', 'published']
    list_filter = ['date_available', 'published', 'channel_name',
                   'child_class']
    search_fields = ['title', 'slug', 'headline', 'channel_name']
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'pk', None) is None:
            obj.user = get_user_model().objects.get(pk=request.user.pk)
            obj.date_insert = timezone.now()
            obj.site = Site.objects.get(pk=settings.SITE_ID)
        obj.date_update = timezone.now()
        obj.save()


def apply_rules(admin_class, rules):
    """
    To allow overrides of admin rules for opps apps
    it uses the settings.py to load the values

    example of use:

    OPPS_ADMIN_RULES = getattr(settings, 'OPPS_ADMIN_RULES', {})
    promo_admin_rules = OPPS_ADMIN_RULES.get('promos.PromoAdmin')
    if promo_admin_rules:
        PromoAdmin = apply_rules(PromoAdmin, promo_admin_rules)

    example of settings.py

    OPPS_ADMIN_RULES = {
        'promos.PromoAdmin': {
            'fieldsets': (
                (u'Identification', {
                    'fields': ('site', 'title', 'slug')}),
            )
        }
    }
    """

    # apply fieldsets
    fieldsets = rules.get('fieldsets')
    if fieldsets:
        new_items = [(_(item[0]), item[1]) for item in fieldsets]
        admin_class.fieldsets = new_items

    # TODO:
    # apply list_display
    # apply list_filter
    # apply search_fields
    # apply exclude
    # apply raw_id_fields

    return admin_class


class HideContainerAdmin(PublishableAdmin):

    list_display = ['image_thumb', 'title', 'channel_name', 'date_available',
                    'published']
    readonly_fields = ['image_thumb']

    def image_thumb(self, obj):
        if obj.main_image:
            return u'<img width="60px" height="60px" src="{0}" />'.format(
                generate_url(obj.main_image.image.url, width=60, height=60))
        return _(u'No Image')
    image_thumb.short_description = _(u'Thumbnail')
    image_thumb.allow_tags = True

    def get_model_perms(self, *args, **kwargs):
        return {}

    def has_add_permission(self, request):
        return False


admin.site.register(Container, HideContainerAdmin)
