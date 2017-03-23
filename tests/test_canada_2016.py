from unittest import TestCase
from fba import Fees
from decimal import Decimal
import json
import os

# Simple class for testing purposes

class FeesTestCanada(TestCase):
    def test_get_fba_fee(self):
        TWOPLACES = Decimal(10) ** -2

        # https://tinyurl.com/mo5qjql
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, 'products/products.json')

        # https://tinyurl.com/ku2zvkm
        with open(json_path, encoding='utf-8') as data_file:
            products = json.load(data_file)

        for product in products:
            item = products[product]
            if 'ca' in item['countries']:
                print("CANDADA " + str(item['description']))
                amazon = AmazonProduct()
                amazon.sales_rank_category = item['category']
                amazon.shipping_width = Decimal(item['dimensions']['cm'][1])
                amazon.shipping_height = Decimal(item['dimensions']['cm'][2])
                amazon.shipping_length = Decimal(item['dimensions']['cm'][0])
                amazon.shipping_weight = Decimal(item['weight']['kg'])

                fees = Fees("CA", 2016)
                fee = fees.get_fba_fee(amazon)
                reference_fee = Decimal(
                    item['totalfulfilment']['cad']).quantize(TWOPLACES)

                print('The type is: ' + str(type(fee)))
                print('Product: ' + item['description'])
                print('Expected fee: ' + str(reference_fee))
                print('Calculated fee: ' + str(fee))

                print(type(fee))

                self.assertEqual(Decimal(reference_fee), fee)
            else:
                print('No CA information for: ' + str(item['description']))


class AmazonProduct(object):
    pass
