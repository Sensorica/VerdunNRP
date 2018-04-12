from django import template
from django.utils.translation import ugettext_lazy as _

register = template.Library()

@register.inclusion_tag('valueaccounting/chair.html')
def chair(desc, field, no_trans=False):
    if not no_trans:
        desc = _(desc)

    linebreaks = False
    try:
        linebreaks = '\n' in field or '<br' in field or '<textarea' in field
    except:
        pass

    return {'desc': desc, 'field': field, 'linebreaks': linebreaks}

@register.simple_tag
def field_as_p(ff, label=''):
    if label:
        label = '<label for="%s">%s</label>' % (ff.auto_id, label)
    else:
        label = ff.label_tag()

    return '<p><div>' + label + '</div><div>' + ff.as_widget() + '</div></p>'

@register.simple_tag
def field_as_div(ff, label=''):
    if label:
        label = '<label for="%s">%s</label>' % (ff.auto_id, label)
    else:
        label = ff.label_tag()

    widget = ff.as_widget()
    pull_right = '<textarea>' not in widget and '<select>' not in widget and '<br' not in widget and 'radio' not in widget
    span = '<span class="pull-right">' if pull_right else '<span>'
    return '<b>' + label + '</b>' + span + ff.as_widget() + '</span>'

@register.simple_tag
def field_as_li(ff, label=''):
    return '<li>' + field_as_div(ff, label) + '</li>'

@register.filter
def tr(txt):
    return _(txt)

@register.filter
def ta(txt, arg):
    return txt + _(arg)

@register.filter
def s(txt):
    if txt.endswith('y'):
        return txt[:-1] + 'ies'
    elif txt.endswith('s'):
        return txt + 'es'
    else:
        return txt + 's'

@register.filter
def img_src(src):
    return '<img src="%s"/>'

@register.filter
def sp(txt, more_txt=''):
    return '%s %s' % (txt, more_txt)
