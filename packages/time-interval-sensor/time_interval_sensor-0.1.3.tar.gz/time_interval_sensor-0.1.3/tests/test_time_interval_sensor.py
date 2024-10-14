import unittest
from sensors.time_interval_sensor import TimeIntervalSensor
from datetime import time, datetime
import pytz

class TestTimeIntervalSensor(unittest.TestCase):

    def test_within_interval(self):
        # Initialize sensor with a time interval
        sensor = TimeIntervalSensor(
            start_time=time(10, 0), 
            end_time=time(12, 0), 
            time_zone='UTC', 
            task_id='test_task'
        )

        # Test with a current time that falls within the interval (e.g., 11:00 AM UTC)
        current_time = datetime(2024, 1, 1, 11, 0, tzinfo=pytz.UTC).time()
        self.assertTrue(sensor.poke({}, current_time=current_time))

    def test_outside_interval(self):
        # Initialize sensor with a time interval
        sensor = TimeIntervalSensor(
            start_time=time(17, 0), 
            end_time=time(18, 0), 
            time_zone='UTC', 
            task_id='test_task'
        )

        # Test with a current time outside the interval (e.g., 9:00 AM UTC)
        current_time = datetime(2024, 1, 1, 9, 0, tzinfo=pytz.UTC).time()
        self.assertFalse(sensor.poke({}, current_time=current_time))

    def test_within_interval_different_time_zone(self):
        # Initialize sensor with a time interval for America/New_York (UTC-5)
        sensor = TimeIntervalSensor(
            start_time=time(10, 0), 
            end_time=time(12, 0), 
            time_zone='America/New_York', 
            task_id='test_task'
        )

        # The current time is 11:00 AM New York time (UTC-5), which corresponds to 16:00 UTC
        current_time = datetime(2024, 1, 1, 16, 0, tzinfo=pytz.UTC)

        # Assert that poke() returns True since 11:00 AM New York time falls within the range
        self.assertTrue(sensor.poke({}, current_time=current_time))



if __name__ == '__main__':
    unittest.main()
