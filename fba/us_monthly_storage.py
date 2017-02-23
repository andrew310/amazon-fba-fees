def get_multiplier_2016(std, month):
    """Returns amazon storage fee multiplier for United States.
    Based on guidelines starting March 1, 2016.
     """

    end_year = month in [11, 12]

    if std:
        return Decimal('0.54') if not end_year else Decimal('2.25')
    else:
        return Decimal('0.43') if not end_year else Decimal('1.15')


def get_multiplier_2017(std, month):
    """Returns amazon storage fee multiplier for United States.
    Based on guidelines starting March 1, 2017.
     """

    end_year = month in [10, 11, 12]

    if std:
        return Decimal('0.64') if not end_year else Decimal('2.35')
    else:
        return Decimal('0.43') if not end_year else Decimal('1.15')
