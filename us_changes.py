from dateutil.parser import parse
import datetime

# As of now I don't have any info about fees before these.
STORAGE_CHANGES = ['2016-03-01', '2017-03-01']


def get_current_multiplier(date):
    key = clamp_date(date)

    return key


def clamp_date(date, changes):
    for d in changes:
        if date <= tmp:
            return d

    return None

def pods = {
    '2017-03-01': get_monthly_storage_2017,


}
