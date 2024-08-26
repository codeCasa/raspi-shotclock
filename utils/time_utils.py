from datetime import datetime, timedelta

def milliseconds_to_datetime(ms, format_string='%Y-%m-%d %I:%M %p'):
    """
    Convert milliseconds to a formatted datetime string.

    :param ms: Number of milliseconds.
    :param format_string: Format string for the output datetime.
    :return: Formatted datetime string.
    """
    # Convert milliseconds to timedelta
    delta = timedelta(milliseconds=ms)
    
    # Base date (epoch)
    base_date = datetime(1970, 1, 1)
    
    # Compute the datetime
    result_date = base_date + delta
    
    # Format the datetime
    formatted_date = result_date.strftime(format_string)
    
    return formatted_date
