from time import strftime
from app import app


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d.%b %H:%M"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.date.strftime(format)
