import unittest
from num2geotext.int_num_to_geo_text import int_num_to_geo_text


class IntToText(unittest.TestCase):

    def test_int_to_text(self):
        self.assertEqual(int_num_to_geo_text(1), "ერთი")
        self.assertEqual(int_num_to_geo_text(69), "სამოცდაცხრა")
        self.assertEqual(int_num_to_geo_text(543), "ხუთას ორმოცდასამი")
        self.assertEqual(int_num_to_geo_text(1_023), "ათას ოცდასამი")
        self.assertEqual(int_num_to_geo_text(52_160), "ორმოცდათორმეტი ათას ას სამოცი")
        self.assertEqual(int_num_to_geo_text(102_009), "ას ორი ათას ცხრა")
        self.assertEqual(int_num_to_geo_text(3_567_569), "სამი მილიონ ხუთას სამოცდაშვიდი ათას ხუთას სამოცდაცხრა")
        self.assertEqual(int_num_to_geo_text(40_352_900), "ორმოცი მილიონ სამას ორმოცდათორმეტი ათას ცხრაასი")
        self.assertEqual(int_num_to_geo_text(602_000_020), "ექვსას ორი მილიონ ოცი")
        self.assertEqual(int_num_to_geo_text(7_322_060_029), "შვიდი მილიარდ სამას ოცდაორი მილიონ სამოცი ათას ოცდაცხრა")
        self.assertEqual(int_num_to_geo_text(99_102_654_102), "ოთხმოცდაცხრამეტი მილიარდ ას ორი მილიონ ექვსას ორმოცდათოთხმეტი ათას ას ორი")
        self.assertEqual(int_num_to_geo_text(874_947_321_987), "რვაას სამოცდათოთხმეტი მილიარდ ცხრაას ორმოცდაშვიდი მილიონ სამას ოცდაერთი ათას ცხრაას ოთხმოცდაშვიდი")
        self.assertEqual(int_num_to_geo_text(6_245_131_890_163), "ექვსი ტრილიონ ორას ორმოცდახუთი მილიარდ ას ოცდათერთმეტი მილიონ რვაას ოთხმოცდაათი ათას ას სამოცდასამი")
        self.assertEqual(int_num_to_geo_text(32_112_526_341_962), "ოცდათორმეტი ტრილიონ ას თორმეტი მილიარდ ხუთას ოცდაექვსი მილიონ სამას ორმოცდაერთი ათას ცხრაას სამოცდაორი")
        self.assertEqual(int_num_to_geo_text(625_954_023_506_003), "ექვსას ოცდახუთი ტრილიონ ცხრაას ორმოცდათოთხმეტი მილიარდ ოცდასამი მილიონ ხუთას ექვსი ათას სამი")


if __name__ == "__main__":
    unittest.main()
