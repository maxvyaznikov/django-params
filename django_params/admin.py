import django
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import widgets

from .models import Param


class TextDateWidget(widgets.AdminDateWidget):
    def decompress(self, value):
        value = Param.str2val(Param.TYPE_DATE, value)[1]
        return super(TextDateWidget, self).decompress(value)


class TextDateTimeWidget(widgets.AdminSplitDateTime):
    def decompress(self, value):
        value = Param.str2val(Param.TYPE_DATETIME, value)[1]
        return super(TextDateTimeWidget, self).decompress(value)

    def value_from_datadict(self, *args, **kwargs):
        value = super(TextDateTimeWidget, self).value_from_datadict(*args, **kwargs)
        return ' '.join(value)


class TextIntegerWidget(widgets.AdminIntegerFieldWidget):
    def decompress(self, value):
        value = Param.str2val(Param.TYPE_INT, value)[1]
        return super(TextIntegerWidget, self).decompress(value)


class ParamAdminAddForm(forms.ModelForm):
    class Meta:
        model = Param
        exclude = ('value',)


class ParamAdminChangeForm(forms.ModelForm):
    class Meta:
        model = Param
        if django.VERSION >= (1, 6):
            fields = '__all__'  # eliminate RemovedInDjango18Warning

    def __init__(self, *args, **kwargs):
        super(ParamAdminChangeForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance'] = kwargs.get('instance') or  self._meta.model()
        if 'value' in self.fields:
            if instance.type == Param.TYPE_DATE:
                self.fields['value'].widget = TextDateWidget()
            elif instance.type == Param.TYPE_DATETIME:
                self.fields['value'].widget = TextDateTimeWidget()
            elif instance.type == Param.TYPE_INT:
                self.fields['value'].widget = TextIntegerWidget()


class ParamAdmin(admin.ModelAdmin):
    form = ParamAdminChangeForm
    add_form = ParamAdminAddForm
    list_display = ('name', 'value', 'type',)
    search_fields = ('name', 'value', 'type',)
    ordering = ('name',)

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def has_add_permission(self, request):  # deny addition
        return settings.DJANGO_PARAMS_HAS_ADD_PERMISSION

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during param creation
        """
        defaults = {}
        if obj is None:  # Add new Param
            defaults['form'] = self.add_form
            self.exclude = self.add_form._meta.exclude
            self.readonly_fields = []
        else:  # Change exists Param
            self.exclude = None
            self.readonly_fields = ('name', 'type',)
        defaults.update(kwargs)
        return super(ParamAdmin, self).get_form(request, obj, **defaults)


admin.site.register(Param, ParamAdmin)

