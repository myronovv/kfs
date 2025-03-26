import unittest
from electrMeter import ElectricityMeter, costMeter


class TestElectricityMeter(unittest.TestCase):
    def setUp(self):
        self.meters = []
        self.day_rate = 1.5
        self.night_rate = 0.9

    def test_update_existing_meter(self):
        self.meters, _ = costMeter(self.meters, "meter1", 100, 50, self.day_rate, self.night_rate)
        self.meters, cost = costMeter(self.meters, "meter1", 150, 70, self.day_rate, self.night_rate)
        self.assertEqual(cost, (150 - 100) * self.day_rate + (70 - 50) * self.night_rate)
        #(150 - 100) * 1.5 + (70 - 50) * 0.9 = 75 + 18 = 93 грн

    def test_new_meter(self):
        self.meters, cost = costMeter(self.meters, "meter2", 200, 100, self.day_rate, self.night_rate)
        self.assertEqual(cost, 0)

    def test_lower_night_readings(self):
        self.meters, _ = costMeter(self.meters, "meter1", 100, 50, self.day_rate, self.night_rate)
        self.meters, cost = costMeter(self.meters, "meter1", 150, 40, self.day_rate, self.night_rate)
        expected_cost = (150 - 100) * self.day_rate + (80) * self.night_rate
        self.assertEqual(cost, expected_cost)

    def test_lower_day_readings(self):
        self.meters, _ = costMeter(self.meters, "meter1", 100, 50, self.day_rate, self.night_rate)
        self.meters, cost = costMeter(self.meters, "meter1", 90, 60, self.day_rate, self.night_rate)
        expected_cost = (100) * self.day_rate + (60 - 50) * self.night_rate
        self.assertEqual(cost, expected_cost)

    def test_lower_day_and_night_readings(self):
        self.meters, _ = costMeter(self.meters, "meter1", 100, 50, self.day_rate, self.night_rate)
        self.meters, cost = costMeter(self.meters, "meter1", 90, 40, self.day_rate, self.night_rate)
        expected_cost = (100) * self.day_rate + (80) * self.night_rate
        self.assertEqual(cost, expected_cost)




if __name__ == "__main__":
    unittest.main()