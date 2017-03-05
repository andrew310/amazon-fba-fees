from .fees import Common


class UnitedKingdom(Common):
    """UK fee calculations
    https://services.amazon.co.uk/services/fulfilment-by-amazon/pricing.html
    """

    def pickAndPack(self, standard, media):
        return None

    def is_standard(self, l, w, h, g):
        """Dims are in cm, weight in grams """

        # make sure all are floats
        values = list(map(lambda x: float(x), [l, w, h]))

        kg = float(g) / 1000

        values.sort(reverse=True)

        return (values[0] <= 45 and values[1] <= 35
                and values[2] <= 26 and kg <= 12)

    def get_monthly_storage(self, month, l=None, w=None, h=None):
        """Calculated per cubic foot """
        return 0.30 if month <= 9 else 0.40
