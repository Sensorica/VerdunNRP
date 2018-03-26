from django import template

register = template.Library()

@register.inclusion_tag('valueaccounting/chair.html')
def chair(desc, field):
    return {'desc': desc, 'field': field, 'linebreaks': ('\n' in field or '<br' in field)}

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
