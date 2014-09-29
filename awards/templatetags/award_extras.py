from django import template

register = template.Library()


@register.filter
def verbose_name(object):
    return object._meta.verbose_name


@register.filter
def verbose_name_plural(object):
    return object._meta.verbose_name_plural
