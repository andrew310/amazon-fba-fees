from decimal import Decimal

# -- 2017 Changes: --
# https://www.amazon.com/gp/help/customer/display.html?nodeId=201648210

# As of now I don't have any info about fees before these.
STORAGE_CHANGES = ['2016-03-01', '2017-03-01']


def clamp_date(date, changes=STORAGE_CHANGES):
    """Return first date from the right
    which is older than param date."""
    for d in reversed(changes):
        if date >= d:
            return d

    return None


def get_multiplier_2016(std, month):
    """Amazon storage fee multiplier for United States.
    Based on guidelines starting March 1, 2016.
     """

    end_year = month in [11, 12]

    if std:
        return Decimal('0.54') if not end_year else Decimal('2.25')
    else:
        return Decimal('0.43') if not end_year else Decimal('1.15')


def get_multiplier_2017(std, month):
    """Amazon storage fee multiplier for United States.
    Based on guidelines starting March 1, 2017.
     """

    end_year = month in [10, 11, 12]

    if std:
        print(std)
        return Decimal('0.64') if not end_year else Decimal('2.35')
    else:
        return Decimal('0.43') if not end_year else Decimal('1.15')


pods = {
    '2017-03-01': get_multiplier_2017,
    '2016-03-01': get_multiplier_2016,
}


def get_multiplier(date):
    """Returns a multiplier function
    based on date passed in."""

    key = clamp_date(date)

    return pods[key]
