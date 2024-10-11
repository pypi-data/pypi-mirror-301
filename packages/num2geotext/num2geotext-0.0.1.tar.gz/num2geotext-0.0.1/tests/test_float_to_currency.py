import unittest
from num2geotext.float_num_to_geo_currency import *


class FloatToCurrency(unittest.TestCase):

    def test_float_to_currency(self):
        self.assertEqual(float_num_to_geo_currency(0.365), "ოცდაჩვიდმეტი თეთრი")
        self.assertEqual(float_num_to_geo_currency(4.2), "ოთხი ლარი და ოცი თეთრი")
        self.assertEqual(float_num_to_geo_currency(17.254), "ჩვიდმეტი ლარი და ოცდახუთი თეთრი")
        self.assertEqual(float_num_to_geo_currency(356.8), "სამას ორმოცდათექვსმეტი ლარი და ოთხმოცი თეთრი")
        self.assertEqual(float_num_to_geo_currency(3_106.4449), "სამი ათას ას ექვსი ლარი და ორმოცდაოთხი თეთრი")
        self.assertEqual(float_num_to_geo_currency(10_006.05), "ათი ათას ექვსი ლარი და ხუთი თეთრი")
        self.assertEqual(float_num_to_geo_currency(325_459.4), "სამას ოცდახუთი ათას ოთხას ორმოცდაცხრამეტი ლარი და ორმოცი თეთრი")
        self.assertEqual(float_num_to_geo_currency(4_512_100.25), "ოთხი მილიონ ხუთას თორმეტი ათას ასი ლარი და ოცდახუთი თეთრი")
        self.assertEqual(float_num_to_geo_currency(68_124_432.3), "სამოცდარვა მილიონ ას ოცდაოთხი ათას ოთხას ოცდათორმეტი ლარი და ოცდაათი თეთრი")
        self.assertEqual(float_num_to_geo_currency(325_000_000.999), "სამას ოცდახუთი მილიონ ერთი ლარი და ნული თეთრი")
        self.assertEqual(float_num_to_geo_currency(1_815_030_020.9), "ერთი მილიარდ რვაას თხუთმეტი მილიონ ოცდაათი ათას ოცი ლარი და ოთხმოცდაათი თეთრი")
        self.assertEqual(float_num_to_geo_currency(15_834_230_110.5), "თხუთმეტი მილიარდ რვაას ოცდათოთხმეტი მილიონ ორას ოცდაათი ათას ას ათი ლარი და ორმოცდაათი თეთრი")
        self.assertEqual(float_num_to_geo_currency(332_214_110_160.23), "სამას ოცდათორმეტი მილიარდ ორას თოთხმეტი მილიონ ას ათი ათას ას სამოცი ლარი და ოცდასამი თეთრი")
        self.assertEqual(float_num_to_geo_currency(6_452_323_784_001.9223), "ექვსი ტრილიონ ოთხას ორმოცდათორმეტი მილიარდ სამას ოცდასამი მილიონ შვიდას ოთხმოცდაოთხი ათას ერთი ლარი და ოთხმოცდათორმეტი თეთრი")
        self.assertEqual(float_num_to_geo_currency(10_000_000_000_000.001), "ათი ტრილიონი ლარი და ნული თეთრი")
        self.assertEqual(float_num_to_geo_currency(100_020_001_030_004.22), "ასი ტრილიონ ოცი მილიარდ ერთი მილიონ ოცდაათი ათას ოთხი ლარი და ოცდაორი თეთრი")

