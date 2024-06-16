from django import template

import datetime


# Create your custom filters here.
register = template.Library()

@register.filter
def format_date_mmddyy(value):
    if isinstance(value, datetime.date):
        return value.strftime("%m/%d/%Y")
    
    return value


@register.filter
def status_class(value):
    status_classes = {"Low": "status-low", "Moderate": "status-med", "High": "status-high", "Critical": "status-crit"}

    return status_classes.get(str(value), "status-default")
