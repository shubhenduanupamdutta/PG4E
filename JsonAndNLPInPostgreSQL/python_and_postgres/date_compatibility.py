"""Code to parse email dates in a way that is compatible with PostgreSQL's date handling."""

from datetime import datetime

# https://www.pg4e.com/code/datecompat.py


# Non-dateutil version - we try our best
def parse_mail_date(md: str) -> str | None:
    """Parse a mail date string and return it in ISO format with timezone."""
    pieces = md.split()
    unparsed_date = " ".join(pieces[:4]).strip()

    # Try a bunch of format variations - strptime() is *lame*
    parsed_datetime: datetime | None = None
    for form in [
        "%d %b %Y %H:%M:%S",
        "%d %b %Y %H:%M:%S",
        "%d %b %Y %H:%M",
        "%d %b %Y %H:%M",
        "%d %b %y %H:%M:%S",
        "%d %b %y %H:%M:%S",
        "%d %b %y %H:%M",
        "%d %b %y %H:%M",
    ]:
        try:
            parsed_datetime = datetime.strptime(unparsed_date, form)  # noqa: DTZ007
            break
        except ValueError:
            continue

    if parsed_datetime is None:
        # print 'Bad Date:',md
        return None

    iso = parsed_datetime.isoformat()

    tz = "+0000"
    try:
        tz = pieces[4]
        _ival = int(tz)  # Only want numeric timezone values
        if tz == "-0000":
            tz = "+0000"
        tzh = tz[:3]
        tzm = tz[3:]
        tz = tzh + ":" + tzm
    except (IndexError, ValueError):
        pass

    return iso + tz
