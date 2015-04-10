# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models
from django.utils.formats import get_format
from django.conf import settings
from gettext import gettext as _


class Param(models.Model):
    TYPE_TEXT = 't'
    TYPE_DATE = 'd'
    TYPE_INT = 'i'
    TYPE_CHOICES = (
        (TYPE_TEXT, 'Text'),
        (TYPE_DATE, 'Date'),
        (TYPE_INT, 'Integer'),
    )
    name = models.CharField(choices=settings.DJANGO_PARAMS_NAME_CHOICES, unique=True, max_length=255)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_TEXT, max_length=10)
    value = models.TextField(blank=True, null=False, default='')

    def __unicode__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _('param')
        verbose_name_plural = _('params')

    def get_value(self):
        if self.type == Param.TYPE_DATE:
            if self.value:
                fmt = get_format('DATE_INPUT_FORMATS')[0]
                return date.fromordinal(datetime.strptime(self.value, fmt).toordinal())
                # return datetime.strptime(self.value, fmt)
            else:
                return None
        elif self.type == Param.TYPE_INT:
            return int(self.value)
        else:
            return self.value

    @staticmethod
    def get(request, name):
        if not hasattr(request, '_django_params_cache'):
            request._django_params_cache = {p.name: p for p in Param.objects.all()}
        return request._django_params_cache[name] if name in request._django_params_cache else None

    @staticmethod
    def get_one(name):
        try:
            return Param.objects.get(name=name)
        except Param.DoesNotExist:
            return None
