from unittest import TestCase
from fba import Fees
from decimal import Decimal

# Simple class for testing purposes

class FeesTestUnitedStates(TestCase):
    def test_is_media(self):
        fees = Fees()

        test = fees.is_media("Video Games")

        self.assertEqual(test, True)

    def test_get_weight_handling(self):
        """Test weight handling function """

        fees = Fees("US", 2016)

        result = fees.get_weight_handling('large_standard',
                                      'non-media', Decimal('0.22'))

        self.assertEqual(result, 0.96)

    def test_product_size_tier(self):
        """Test product size tier function """

        fees = Fees("US", 2016)

        l = 10.39
        w = 7.09
        h = 2.28
        g = 0.22

        test = fees.get_product_size_tier(l, w, h, g, True)

        self.assertEqual('large_standard', test)

    def test_inpack_dimensions_with_object(self):
        """Call unpack_dimensions with an object"""
        amazon = AmazonProduct()

        amazon.shipping_width = Decimal(10)
        amazon.shipping_height = Decimal(20)
        amazon.shipping_length = Decimal(30)

        fees = Fees("US", 2016)

        feeList = fees.unpack_dimensions(amazon)

        self.assertEqual(feeList, [30, 10, 20])

    def test_unpack_dimensions_with_dict(self):
        """Call unpack_dimensions with dict"""
        amazon = {}

        amazon["shipping_width"] = Decimal(10)
        amazon["shipping_height"] = Decimal(20)
        amazon["shipping_length"] = Decimal(30)

        fees = Fees("US", 2016)

        feeList = fees.unpack_dimensions(amazon)

        self.assertEqual(feeList, [30, 10, 20])

    def test_get_fba_fee(self):
        products = [
            dict(width=5.30, height=0.50, length=6.70, weight=0.16,
                 category='Video Games', fee='1.56'),  # media small standard
            dict(width=6.77, height=0.63, length=7.87, weight=0.31,
                 category='Toy', fee='2.56'),  # small standard
            dict(width=6.77, height=0.63, length=7.87, weight=0.31,
                 category='Apparel', fee='2.96'),  # small standard apparel
            dict(width=11.40, height=0.90, length=14.40, weight=0.45,
                 category='Toy', fee='3.02'),  # large standard
            dict(width=13.00, height=8.30, length=20.30, weight=14.05,
                 category='Toy', fee='11.61'),  # small oversize
            dict(width=32.50, height=21.70, length=40.00, weight=103.00,
                 category='Toy', fee='147.99'),  # special oversize
        ]

        for product in products:
            amazon = AmazonProduct()
            amazon.sales_rank_category = product['category']
            amazon.shipping_width = Decimal(product['width'])
            amazon.shipping_height = Decimal(product['height'])
            amazon.shipping_length = Decimal(product['length'])
            amazon.shipping_weight = Decimal(product['weight'])

            fees = Fees("US", 2016)

            fee = fees.get_fba_fee(amazon)

            print(type(fee))

            self.assertEqual(Decimal(product['fee']), fee)

    def test_get_fba_fee_missing_weight(self):
        """Pass in object missing weight dim."""
        amazon = AmazonProduct()
        amazon.shipping_width = Decimal(10)
        amazon.shipping_height = Decimal(20)
        amazon.shipping_length = Decimal(30)
        amazon.shipping_weight = None

        fees = Fees("US", 2016)

        fee = fees.get_fba_fee(amazon)

        self.assertEqual(False, fee)

    def test_get_fba_fee_missing_dimension(self):
        """Pass in object missing length dim."""
        amazon = AmazonProduct()
        amazon.shipping_width = Decimal(10)
        amazon.shipping_height = Decimal(20)
        amazon.shipping_length = None
        amazon.shipping_weight = Decimal(10)

        fees = Fees("US", 2016)

        fee = fees.get_fba_fee(amazon)

        self.assertEqual(False, fee)

    def test_get_referral_fee(self):
        amazon = AmazonProduct()
        amazon.shipping_width = Decimal(10)
        amazon.shipping_height = Decimal(20)
        amazon.shipping_length = Decimal(30)
        amazon.shipping_weight = Decimal(30)

        fees = Fees("US", 2016)

        fee = fees.get_referral_fee(amazon)

        self.assertEqual(Decimal('0.15'), fee)

    def test_get_monthly_storage_oversize(self):
        amazon = AmazonProduct()

        # oversize inventory
        amazon.shipping_length = l = Decimal(30)
        amazon.shipping_width = w = Decimal(10)
        amazon.shipping_height = h = Decimal(20)
        amazon.shipping_weight = wt = Decimal(30)

        fees = Fees("US", 2016)

        feeList = fees.unpack_dimensions(amazon)

        # Not end of year
        date = '2016-09-01'

        fee = fees.get_monthly_storage(date, l, w, h, wt)

        self.assertEqual(Decimal('1.49'), fee)

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

        fees = Fees("US", 2016)

        feeList = fees.unpack_dimensions(amazon)

        # Not end of year
        date = '2016-03-02'

        fee = fees.get_monthly_storage(date, l, w, h, wt)

        self.assertEqual(Decimal('.08'), fee)




class AmazonProduct(object):
    pass
