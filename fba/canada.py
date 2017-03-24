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
        """Dims are in cm, weight in kilograms """

        FOURPLACES = Decimal(10) ** -4

        # make sure all are floats
        values = list(
            map(lambda x: Decimal(float(x)).quantize(FOURPLACES), [l, w, h]))

        kg = Decimal(g).quantize(FOURPLACES)

        if (ceil(values[0]) > 45):
            return False
        if (ceil(values[1]) > 35):
            return False
        if (ceil(values[2]) > 20):
            return False
        if (ceil(kg) > 9):
            return False

        return True

    def is_envelope(self, l, w, h, g):
        """Dims are in cm, weight in kilograms """

        FOURPLACES = Decimal(10) ** -4

        # make sure all are floats
        values = list(
            map(lambda x: Decimal(float(x)).quantize(FOURPLACES), [l, w, h]))

        kg = Decimal(g).quantize(FOURPLACES)


        if (ceil(values[0]) > 38):
            return False
        if (ceil(values[1]) > 27):
            return False
        if (ceil(values[2]) > 2):
            return False
        if (kg > Decimal('0.5')):
            return False

        return True

    def pick_and_pack(self, standard, media):
        if standard:
            return Decimal('0.90') if media else Decimal('1.55')
        else:
            return Decimal('2.65')

    def weight_handling(self, weight):
        """Leaving out envelopes for now """

        # round up to next multiple of 500
        weight_g = ceil((weight * 1000)/500) * 500

        weight_fee  = Decimal('3.75')

        if weight_g < 500:
            return weight_fee
        else:
            return weight_fee + (
                Decimal('0.37') * Decimal(ceil(weight_g/500)))


    def weight_handling_envelope(self, weight):

        # round up to next multiple of 100
        weight_g = ceil((weight * 1000)/100) * 100

        weight_fee  = Decimal('1.90')

        if weight_g <= 100:
            return weight_fee
        else:
            return weight_fee + (
                Decimal('0.25') * Decimal(ceil(weight_g/100)))


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

        size = self.is_standard(length, width, height, weight)
        media = self.is_media(category)

        pnp = self.pick_and_pack(size, media)

        print(
            "ENVELOOOOPE: " + str(self.is_envelope(length, width, height, weight)))

        if(self.is_envelope(length, width, height, weight)):
            weight_handling = self.weight_handling_envelope(weight)
        else:
            weight_handling = self.weight_handling(weight)

        monthly_storage = self.get_monthly_storage(3, length, width, height)

        print('pnp: ' + str(pnp))
        print('wh: ' + str(weight_handling))
        print('monthly_storage: ' + str(monthly_storage))

        fee = pnp + weight_handling + monthly_storage

        return round(Decimal(fee), 2)
