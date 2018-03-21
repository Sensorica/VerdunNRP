from django import template

register = template.Library()

@register.assignment_tag
def type_exchange_type():
    return "exchange plan"

@register.assignment_tag
def type_exchange():
    return "exchange"

@register.assignment_tag
def type_transfer_type():
    return "transfer"

@register.assignment_tag
def type_transfer():
    return "transfer event"

@register.assignment_tag
def type_event_type():
    return "event"

@register.assignment_tag
def type_event():
    return "event record"

@register.assignment_tag
def type_resource_type():
    return "resource type"

@register.assignment_tag
def type_resource():
    return "resource"

@register.assignment_tag
def type_facet():
    return "quality"

@register.assignment_tag
def type_facet_value():
    return "category"

@register.assignment_tag
def type_agent_type():
    return "agent type"

@register.assignment_tag
def type_agent():
    return "agent"

@register.assignment_tag
def type_agent_association_type():
    return "agent relationship"

@register.assignment_tag
def type_use_case():
    return "usage"

@register.assignment_tag
def type_use_case_event_type():
    return "use event"

@register.assignment_tag
def type_process():
    return "process"

@register.assignment_tag
def type_process_pattern():
    return "process pattern"

@register.assignment_tag
def type_order():
    return "order"

@register.assignment_tag
def type_process_type():
    return "process plan"

@register.assignment_tag
def type_agent_resource_type():
    return "agent resource association"
