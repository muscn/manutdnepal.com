from datetime import timedelta, tzinfo


# Create tzinfo classes, instances of which you tie into a datetime object
class UTC(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        pass


class Kathmandu(tzinfo):
    def utcoffset(self, *dt):
        return timedelta(hours=5.75)

    def tzname(self, dt):
        return "Kathmandu"

    def dst(self, dt):
        pass


# Transform functions
def local_to_utc(date_input):
    """date_input is a datetime object containing a tzinfo

    Returns a datetime object at UTC time.
    """
    tzoffset = date_input.tzinfo.utcoffset()
    date = (date_input - tzoffset).replace(tzinfo=UTC())
    return date


def utc_to_local(date_input):
    """date_input is a datetime object containing a tzinfo

    Returns a datetime object at Manila time.
    """
    local = Kathmandu()
    tzoffset = local.utcoffset()
    date = (date_input + tzoffset).replace(tzinfo=local)
    return date