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


class AmazonProduct(object):
    pass
