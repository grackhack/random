from time import strftime
from app import app


@app.template_filter('formatdatetime')
def format_datetime(value, format="%H:%M"):
    """Format a date time to (Default %d.%b_): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.date.strftime(format)


@app.template_filter('only_date')
def only_date(value, format="%Y-%m-%d"):
    """Format a date time to (Default): YYYY-MM-DD"""
    if value is None:
        return ""
    return value.strftime(format)

@app.template_filter('human_date')
def human_date(value, format="%d.%m.%Y"):
    """Format a date time to (Default): DD.MM.YYYY"""
    if value is None:
        return ""
    return value.strftime(format)


@app.template_filter('is_numeric')
def is_digit(value):
    if str(value).isdigit():
        return True
    return False


@app.template_filter('hex_color')
def hex_color(value):
    return "%0.2X" % (255 - int(value) * 5)


@app.template_filter('rounded')
def rounded(value):
    return round(value, 2)
