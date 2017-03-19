from unittest import TestCase
from fba import Fees
from decimal import Decimal
import json
import os

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
        # https://tinyurl.com/ly9rh5v
        TWOPLACES = Decimal(10) ** -2

        # https://tinyurl.com/mo5qjql
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, 'products/products.json')

        # https://tinyurl.com/ku2zvkm
        with open(json_path, encoding='utf-8') as data_file:
            products = json.load(data_file)

        for product in products:
            item = products[product]
            amazon = AmazonProduct()
            amazon.sales_rank_category = item['category']
            amazon.shipping_width = Decimal(item['dimensions']['in'][1])
            amazon.shipping_height = Decimal(item['dimensions']['in'][2])
            amazon.shipping_length = Decimal(item['dimensions']['in'][0])
            amazon.shipping_weight = Decimal(item['weight']['lb'])

            fees = Fees("US", 2017)

            fee = fees.get_fba_fee(amazon)

            reference_fee = Decimal(
                item['fulfilmentfee']['usd']).quantize(TWOPLACES)

            print(type(fee))
            print('Product: ' + item['description'])
            print('Expected fee: ' + str(reference_fee))
            print('Calculated fee: ' + str(fee))

            self.assertEqual(reference_fee, fee)

class AmazonProduct(object):
    pass
