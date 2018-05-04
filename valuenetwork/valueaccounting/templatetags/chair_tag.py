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

    return {'desc': desc, 'field': field, 'linebreaks': linebreaks, 'wrap': False}

@register.inclusion_tag('valueaccounting/chair.html')
def field_as_p(ff, label=''):
    return {'desc': label or ff.label_tag(), 'wrap': 'p', 'field': ff.as_widget(), 'linebreaks': True}

@register.inclusion_tag('valueaccounting/chair.html')
def field_as_div(ff, label=''):
    linebreaks = False
    field = ff.as_widget()
    try:
        linebreaks = '\n' in field or '<br' in field or '<textarea' in field
    except:
        pass
    return {'desc': label or ff.label_tag(), 'field': ff, 'linebreaks': linebreaks, 'wrap': False}

@register.inclusion_tag('valueaccounting/chair.html')
def field_as_li(ff, label=''):
    linebreaks = False
    field = ff.as_widget()
    try:
        linebreaks = '\n' in field or '<br' in field or '<textarea' in field
    except:
        pass
    return {'field': field, 'desc': label or ff.label_tag(), 'wrap': 'li', 'linebreaks': linebreaks}

@register.filter
def tr(txt):
    return _(txt)

@register.filter
def ta(txt, arg):
    return unicode(txt) + _(arg)

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
    return '<img src="%s"/>' % (src,)

@register.filter
def sp(txt, more_txt=''):
    return '%s %s' % (unicode(txt), unicode(more_txt))

@register.filter
def ts(thing):
    return '%d' % (thing,)
