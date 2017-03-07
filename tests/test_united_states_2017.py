from unittest import TestCase
from fba import Fees
from decimal import Decimal


class FeesTestUnitedStates2017(TestCase):
    def test_is_standard(self):
        amazon = AmazonProduct()

        # Not standard since median side > 14"
        amazon.shipping_length = l = Decimal(16.1)
        amazon.shipping_width = w = Decimal(15.9)
        amazon.shipping_height = h = Decimal(5.4)
        amazon.shipping_weight = wt = Decimal(3.55)

        fees = Fees()

        std = fees.is_standard(l, w, h, wt)

        self.assertEqual(std, False)

    def test_get_monthly_storage_oversize(self):
        amazon = AmazonProduct()
        # Note: Oversize / not end of year hasn't changed since 2016.
        # It is still .43 per cubic foot.

        # Oversize product
        # Cubic feet = 1382.346 / 1728 = 0.799968750
        amazon.shipping_length = l = Decimal(16.1)
        amazon.shipping_width = w = Decimal(15.9)
        amazon.shipping_height = h = Decimal(5.4)
        amazon.shipping_weight = wt = Decimal(3.55)

        fees = Fees()

        feeList = fees.unpack_dimensions(amazon)

        # Not end of year
        date = '2017-03-02'

        fee = fees.get_monthly_storage(date, l, w, h, wt)

        self.assertEqual(Decimal('.34'), fee)

    def test_get_monthly_storage_standard_size(self):
        amazon = AmazonProduct()
        # standard changed from .54 to .64 for not end of year

        # B013WM1DOY
        # Product Dimensions: 12 X 10 X 2 inches
        # Unit Weight: 1.65 pounds
        amazon.shipping_length = l = Decimal(12)
        amazon.shipping_width = w = Decimal(10)
        amazon.shipping_height = h = Decimal(2)
        amazon.shipping_weight = wt = Decimal(1.65)

        fees = Fees()

        feeList = fees.unpack_dimensions(amazon)

        # Not end of year
        date = '2017-03-02'

        fee = fees.get_monthly_storage(date, l, w, h, wt)

        self.assertEqual(Decimal('.09'), fee)

    def test_get_fba_fee(self):
        products = [
            dict(width=5.30, height=0.50, length=6.70, weight=0.16,
                 category='Video Games', fee='2.41'),  # media small standard
            dict(width=6.77, height=0.63, length=7.87, weight=0.31,
                 category='Toy', fee='2.41'),  # small standard
            dict(width=6.77, height=0.63, length=7.87, weight=0.31,
                 category='Apparel', fee='2.81'),  # small standard apparel
            dict(width=11.40, height=0.90, length=14.40, weight=0.45,
                 category='Toy', fee='2.99'),  # large standard
            dict(width=13.00, height=8.30, length=20.30, weight=14.05,
                 category='Toy', fee='12.31'),  # small oversize
            dict(width=32.50, height=21.70, length=40.00, weight=103.00,
                 category='Toy', fee='150.96'),  # special oversize
        ]

        for product in products:
            amazon = AmazonProduct()
            amazon.sales_rank_category = product['category']
            amazon.shipping_width = Decimal(product['width'])
            amazon.shipping_height = Decimal(product['height'])
            amazon.shipping_length = Decimal(product['length'])
            amazon.shipping_weight = Decimal(product['weight'])

            fees = Fees("US", 2017)

            fee = fees.get_fba_fee(amazon)

            print(type(fee))

            self.assertEqual(Decimal(product['fee']), fee)

class AmazonProduct(object):
    pass
