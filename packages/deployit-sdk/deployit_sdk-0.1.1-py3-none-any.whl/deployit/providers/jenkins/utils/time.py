from datetime import datetime, timedelta, timezone


def convert_timestamp(unix_time):
    """
    Convert a Unix timestamp to a human-readable time string.

    Parameters
    ----------
    unix_time : int
        The Unix timestamp.

    Returns
    -------
    str
        The human-readable time string.
    """
    utc_time = datetime.fromtimestamp(unix_time / 1000, tz=timezone.utc)
    utc_3_time = utc_time - timedelta(hours=3)  # UTC-3
    return utc_3_time.strftime("%Y-%m-%d %H:%M:%S")


def convert_duration(duration_ms):
    """
    Convert a duration in milliseconds to a human-readable duration string.

    Parameters
    ----------
    duration_ms : int
        The duration in milliseconds.

    Returns
    -------
    str
        The human-readable duration string.
    """
    minutes, seconds = divmod(duration_ms // 1000, 60)
    return f"{minutes}m {seconds}s"
