from django import template

register = template.Library()

@register.filter
def brief_timedelta(td):
    if not td:
        return "0ч"
    days = td.days
    hours = td.seconds // 3600
    if days:
        return f"{days}д {hours}ч"
    return f"{hours}ч"