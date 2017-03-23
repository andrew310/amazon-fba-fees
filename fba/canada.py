from .fees import Common
from math import ceil
from decimal import Decimal


class Canada(Common):
    """Canadian fee calculations
    https://www.amazon.ca/b/?node=13718757011
    """
    def __init__(self, year=2017):
        self.year = year

    def is_standard(self, l, w, h, g):
        """Dims are in cm, weight in grams """

        # make sure all are floats
        # values = list(map(lambda x: float(x), [l, w, h]))
        values = [
            float(l),
            float(w),
            float(h)
            ]

        # kg = float(g) / 1000
        kg = g

        # values.sort(reverse=True)

        return (values[0] <= 45 and values[1] <= 35
                and values[2] <= 20 and kg <= 9)

    def pick_and_pack(self, standard, media):
        print("STANDARD RESULT: " + str(standard))
        if standard:
            return Decimal('0.90') if media else Decimal('1.55')
        else:
            return Decimal('2.65')

    def weight_handling(self, weight):
        """Leaving out envelopes for now """

        if weight <= 500:
            return Decimal('3.75')

        else:
            # Oversize, 3.75 for first 500g, plus 0.36 for each add'l 500g
            return (Decimal('3.75')
                    + (Decimal('0.37')
                    * ceil((weight - 500)/500)))

    def get_monthly_storage(self, month, l=None, w=None, h=None):
        """Calculated per cubic meter """

        m3 = (l * w * h) / 1000000

        return round(16 * m3, 2) if month <= 9 else round(23 * m3, 2)

    def get_fba_fee(self, amazon):
        """Takes a row from the amazon_products table,
        Calculates the fba fee based on specs found.
        """

        requiredDims = ["shipping_weight", "shipping_width",
                        "shipping_height", "shipping_length"]

        category = amazon.__dict__.get('sales_rank_category', '')

        # Ensure we have needed dims
        for d in requiredDims:
            if d not in amazon.__dict__.keys():
                return False

        weight = amazon.shipping_weight
        width = amazon.shipping_width
        height = amazon.shipping_height
        length = amazon.shipping_length

        # weight is required to calculate the fee
        if weight is None:
            return False

        size = not self.is_standard(length, width, height, weight)
        media = self.is_media(category)

        pnp = self.pick_and_pack(size, media)
        weight_handling = self.weight_handling(weight)

        fee = pnp + weight_handling

        return round(Decimal(fee), 2)
