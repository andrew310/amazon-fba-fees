from decimal import Decimal


class Common:
    """Contains methods shared amongst contries."""

    @staticmethod
    def get_referral_fee(amazon):
        return Decimal('0.15')

    @staticmethod
    def is_media(category):
        media = ['Books', 'Music', 'Videos', 'Video Games',
                 'DVDs', 'Software']

        return category in media

    @staticmethod
    def get_volume(length, width, height):
        try:
            vol = length * width * height
        except:
            return None

        return vol

    @staticmethod
    def unpack_decimals(obj, keys):
        """Takes list of keys,
        attemps to extract them from dict and return as decimal.
        Built specifically for lines from an MWS report.
        """

        a = []
        for key in keys:
            a.append((lambda x: Decimal(x) if x != '--' else 0)
                     (obj.get(key, 0)))

        return a

    @staticmethod
    def unpack_or_bust(keys, obj):
        """Returns values from obj or False """

        values = []
        objDict = obj

        # Allow fn to work on objs or dicts
        if not isinstance(obj, dict):
            objDict = obj.__dict__

        objKeys = objDict.keys()

        for key in keys:
            if key in objKeys:
                values.append(Decimal(objDict[key]))
            else:
                return False

        return values

    @classmethod
    def unpack_dimensions(self, amazon):
        keys = ["shipping_length", "shipping_width", "shipping_height"]
        alt_keys = ["longest-side", "median-side", "shortest-side"]

        values = self.unpack_or_bust(keys, amazon) \
            or self.unpack_or_bust(alt_keys, amazon)

        return None if values is False else values
