from .fees import Common
from math import ceil
from decimal import Decimal, ROUND_HALF_UP


class UnitedStates(Common):
    """United states fee calculations
    https://www.amazon.com/gp/aw/help/id=201119390
    """

    def get_order_handling(self, size, media):
        if size in ["small_standard", "large_standard"] and media is False:
            return 1
        else:
            return 0

    def get_pick_and_pack(self, size):
        matrix = [("std", 1.06), ("small", 4.09), ("medium", 5.20),
                  ("large", 8.40), ("special", 10.53)]

        if "standard" in size:
            size = "std"
        else:
            size = size.split('_', 1)[0]

        for item in matrix:
            if item[0] == size:
                return item[1]

    def get_weight_handling(self, tier, media, weight):
        matrix = {
            "small_standard": lambda x: 0.5 * x,
            "large_standard": {
                "media": lambda x: (
                    0.85 if x <= 1 else 1.24 + max((x - 2), 0) * 0.41),
                "non-media": lambda x: (
                    0.96 if x <= 1 else 1.95 + max((x - 2), 0) * 0.39)
                },
            "small_oversize": lambda x: (
                2.06 if x <= 2 else 2.06 + (x - 2) * 0.39),
            "medium_oversize": lambda x: (
                2.73 if x <= 2 else 2.73 + (x - 2) * 0.39),
            "large_oversize": lambda x: (
                63.98 if x <= 90 else 63.98 + (x - 90) * 0.80),
            "special_oversize": lambda x: (
                124.58 if x <= 90 else 124.58 + (x - 90) * 0.92),
             }

        prelim = matrix[tier]
        if isinstance(prelim, dict):
            prelim = prelim[media]

        return prelim(weight)

    def is_standard(self, l, w, h, wt):
        """Dims are in inches, weight in ounces """

        # make sure all are floats
        values = list(map(lambda x: float(x), [l, w, h]))

        values.sort()

        return (values[0] <= 8 and values[1] <= 14
                and values[2] <= 18 and wt <= 20)

    def get_outbound_weight(self, volume, weight, oversize):
        """"Outbound Shipping Weight Calculation
        if package volume is greater than 5184, or if oversize,
        use dim weight if greater than unit weight
        """

        o_weight = weight
        if volume > 5184 or oversize:
            dim_weight = volume / 166
            if dim_weight > weight:
                o_weight = dim_weight

        return o_weight

    def get_product_size_tier(self, length, width, height, weight, media):
        """ Returns string describing product size tier """

        girth = 2 * (width + height) + length

        values = sorted([length, width, height], reverse=True)
        values = values + [girth, weight]

        tiers = [('15 12 .75 n/a .75', 'small_standard'),
                 ('18 14 8 n/a 20', 'large_standard'),
                 ('60 30 n/a 130 70', 'small_oversize'),
                 ('108 n/a n/a 130 150', 'medium_oversize'),
                 ('108 n/a n/a 165 150', 'large_oversize'),
                 ('9999999 n/a n/a 9999999 9999999', 'special_oversize')]

        if media:
            tiers = [('15 12 .75 n/a .875', 'small_standard')] + tiers

        def _compare(m):
            for pair in matrix:
                try:
                    spec = float(pair[1])
                except:
                    spec = None

                if spec is not None and pair[0] > spec:
                    return False

            return True

        for tier in tiers:
            specs = tier[0].split(' ')
            matrix = zip(values, specs)
            if _compare(matrix):
                return tier[1]

    def get_fba_fee(self, amazon):
        requiredDims = ["shipping_weight", "shipping_width",
                        "shipping_height", "shipping_length"]

        category = amazon.__dict__.get('sales_rank_category', '')

        # Ensure we have needed dims
        for d in requiredDims:
            if d not in amazon.__dict__.keys():
                return False
            elif amazon.__dict__[d] is None:
                return False

        weight = amazon.shipping_weight
        width = amazon.shipping_width
        height = amazon.shipping_height
        length = amazon.shipping_length

        # weight is required to calculate the fee
        if weight is None:
            return False

        dim = [width, height, length]

        try:
            dim.sort(reverse=True)
        except TypeError:
            return False

        oversize = not self.is_standard(length, width, height, weight)
        volume = self.get_volume(length, width, height)
        o_weight = self.get_outbound_weight(volume, weight, oversize)

        media = self.is_media(category)
        size = self.get_product_size_tier(length, width, height,
                                          o_weight, media)

        sizes = ["small_oversize", "medium_oversize", "large_oversize"]

        # Redundant? isn't it part of outbound_weight?
        if size in sizes or (not media and weight > 1 and not oversize):
            weight = max(volume / 166, weight)

        if oversize:
            shipping_weight = weight + Decimal('1')
        else:
            shipping_weight = weight + Decimal('.25')

        shipping_weight = ceil(shipping_weight)

        mediaStr = "media" if media else "non-media"
        order_handling = self.get_order_handling(size, media)
        pick_and_pack = self.get_pick_and_pack(size)
        weight_handling = self.get_weight_handling(size, mediaStr,
                                                   shipping_weight)

        # clothing gets $0.40 additional pick and pack fee
        if category == 'Apparel':
            pick_and_pack += 0.40

        fee = order_handling + pick_and_pack + weight_handling
        return Decimal(fee).quantize(Decimal('.02'), rounding=ROUND_HALF_UP)

    def get_monthly_storage(self, month, l, w, h):
        """Returns amazon storage fee for United States """

        volume = self.get_volume(l, w, h)

        if volume is None:
            return None

        cubic_feet = volume / 1728
        size = max(l, w, h) < 60
        end_of_year = month in [11, 12]

        def _get_multiplier(std, endYear):
            if std:
                return Decimal('0.54') if not end_of_year else Decimal('2.25')
            else:
                return Decimal('0.43') if not end_of_year else Decimal('1.15')

        res = Decimal(cubic_feet * _get_multiplier(size, end_of_year))

        return res.quantize(Decimal('.02'), rounding=ROUND_HALF_UP)
