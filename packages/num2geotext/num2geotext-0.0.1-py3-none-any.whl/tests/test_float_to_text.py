import unittest
from num2geotext.float_num_to_geo_text import custom_round, float_num_to_geo_text



class FloatToText(unittest.TestCase):

    def test_float_to_text(self):
        self.assertEqual(custom_round(2.565, 2), 2.57)
        self.assertEqual(float_num_to_geo_text(0.246), "ნული მთელი, ოცდახუთი მეასედი")
        self.assertEqual(float_num_to_geo_text(13.2), "ცამეტი მთელი, ორი მეათედი")
        self.assertEqual(float_num_to_geo_text(648.193), "ექვსას ორმოცდარვა მთელი, ცხრამეტი მეასედი")
        self.assertEqual(float_num_to_geo_text(4_358.48), "ოთხი ათას სამას ორმოცდათვრამეტი მთელი, ორმოცდარვა მეასედი")
        self.assertEqual(float_num_to_geo_text(67_821.9), "სამოცდაშვიდი ათას რვაას ოცდაერთი მთელი, ცხრა მეათედი")
        self.assertEqual(float_num_to_geo_text(642_143.355), "ექვსას ორმოცდაორი ათას ას ორმოცდასამი მთელი, ოცდათექვსმეტი მეასედი")
        self.assertEqual(float_num_to_geo_text(1_354_982.102), "ერთი მილიონ სამას ორმოცდათოთხმეტი ათას ცხრაას ოთხმოცდაორი მთელი, ერთი მეათედი")
        self.assertEqual(float_num_to_geo_text(36_127_362.2), "ოცდათექვსმეტი მილიონ ას ოცდაშვიდი ათას სამას სამოცდაორი მთელი, ორი მეათედი")
        self.assertEqual(float_num_to_geo_text(437_248_149.76), "ოთხას ოცდაჩვიდმეტი მილიონ ორას ორმოცდარვა ათას ას ორმოცდაცხრა მთელი, სამოცდათექვსმეტი მეასედი")
        self.assertEqual(float_num_to_geo_text(9_424_123_578.10007), "ცხრა მილიარდ ოთხას ოცდაოთხი მილიონ ას ოცდასამი ათას ხუთას სამოცდათვრამეტი მთელი, ერთი მეათედი")
        self.assertEqual(float_num_to_geo_text(29_604_573_127.07), "ოცდაცხრა მილიარდ ექვსას ოთხი მილიონ ხუთას სამოცდაცამეტი ათას ას ოცდაშვიდი მთელი, შვიდი მეასედი")
        self.assertEqual(float_num_to_geo_text(354_000_000_007.12), "სამას ორმოცდათოთხმეტი მილიარდ შვიდი მთელი, თორმეტი მეასედი")
        self.assertEqual(float_num_to_geo_text(1_356_150_020_607.78), "ერთი ტრილიონ სამას ორმოცდათექვსმეტი მილიარდ ას ორმოცდაათი მილიონ ოცი ათას ექვსას შვიდი მთელი, სამოცდათვრამეტი მეასედი")
        self.assertEqual(float_num_to_geo_text(99_999_999_999_999.9999), "ასი ტრილიონი მთელი, ნული მეათედი")
        self.assertEqual(float_num_to_geo_text(944_256_021_357_149.5), "ცხრაას ორმოცდაოთხი ტრილიონ ორას ორმოცდათექვსმეტი მილიარდ ოცდაერთი მილიონ სამას ორმოცდაჩვიდმეტი ათას ას ორმოცდაცხრა მთელი, ხუთი მეათედი")


if __name__ == "__main__":
    unittest.main()