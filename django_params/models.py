# -*- coding: utf-8 -*-
from datetime import date, datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from gettext import gettext as _

DEFAULT_DATE_FORMAT = getattr(settings, 'DJANGO_PARAMS_DATE_FORMAT', '%d.%m.%Y')
DEFAULT_DATETIME_FORMAT = getattr(settings, 'DJANGO_PARAMS_DATETIME_FORMAT', '%d.%m.%Y %H:%M:%S')


class Param(models.Model):
    TYPE_TEXT = 't'
    TYPE_DATE = 'd'
    TYPE_DATETIME = 'dt'
    TYPE_INT = 'i'
    TYPE_CHOICES = (
        (TYPE_TEXT, 'Text'),
        (TYPE_DATE, 'Date'),
        (TYPE_DATETIME, 'DateTime'),
        (TYPE_INT, 'Integer'),
    )
    name = models.CharField(choices=settings.DJANGO_PARAMS_NAME_CHOICES, unique=True, max_length=255)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_TEXT, max_length=10)
    value = models.TextField(blank=True, null=False, default='')

    def __unicode__(self):
        return self.get_name_display()

    def __str__(self):
        return self.__unicode__()

    class Meta:
        app_label = 'django_params'
        verbose_name = _('param')
        verbose_name_plural = _('params')

    def get_value(self):
        return Param.str2val(type=self.type, value=self.value)[1]

    def set_value(self, value):
        self.value = Param.val2str(type=self.type, value=value)[1]
        self.save()

    @staticmethod
    def val2str(type, value):
        if type == Param.TYPE_DATE:
            value = datetime.strftime(value, DEFAULT_DATE_FORMAT)
        elif type == Param.TYPE_DATETIME:
            value = datetime.strftime(value, DEFAULT_DATETIME_FORMAT)
        elif type == Param.TYPE_INT:
            value = str(value)
        return type, value

    @staticmethod
    def str2val(type, value):
        if type == Param.TYPE_DATE:
            if value:
                value = date.fromordinal(datetime.strptime(value, DEFAULT_DATE_FORMAT).toordinal())
            else:
                value = None
        elif type == Param.TYPE_DATETIME:
            if value:
                value = datetime.strptime(value, DEFAULT_DATETIME_FORMAT)
                value = timezone.make_aware(value, timezone.get_default_timezone())
            else:
                value = None
        elif type == Param.TYPE_INT:
            value = int(value)
        return type, value

    @staticmethod
    def get(request, name):
        if not hasattr(request, '_django_params_cache'):
            request._django_params_cache = {p.name: p for p in Param.objects.all()}
        return request._django_params_cache[name] if name in request._django_params_cache else None

    @staticmethod
    def get_one(name, create_if_nothing_with=None):
        """
        Function to get single param by a single query

        :param name: is a name of parameter
        :param create_if_nothing_with: if you want to create param with default value
            if it doesn't exist on the time of your call, specify this param as tuple
            of (<type>, <value>) to create it. For example:
            >> Param.get_one(settings.PARAMS_COPYRIGHT)
            None
            >> Param.get_one(settings.PARAMS_COPYRIGHT, (Param.TYPE_TEXT, '(c)'))
            '(c)'
            >> Param.get_one(settings.PARAMS_COPYRIGHT)
            '(c)'
        :return:
        """
        try:
            return Param.objects.get(name=name)
        except Param.DoesNotExist:
            if create_if_nothing_with is None:
                return None
            else:
                type, val = Param.val2str(*create_if_nothing_with)
                return Param.objects.create(name=name, type=type, value=val)
