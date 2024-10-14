# sensors/time_interval_sensor.py
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime, time
import pytz

class TimeIntervalSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, start_time: time, end_time: time, time_zone: str = 'UTC', timeout: int = 60, *args, **kwargs):
        super().__init__(timeout=timeout, *args, **kwargs)
        self.start_time = start_time
        self.end_time = end_time
        self.time_zone = time_zone

    def poke(self, context, current_time=None):
        # Get the target timezone
        tz = pytz.timezone(self.time_zone)

        # If current_time is provided (for testing), use it; otherwise, get the current time in the target timezone
        if current_time:
            # If current_time is passed in UTC, convert it to the target time zone
            if current_time.tzinfo is not None:
                now = current_time.astimezone(tz).time()
            else:
                now = current_time
        else:
            now = datetime.now(tz).time()

        # Combine today's date with start_time and end_time, localizing them to the target timezone
        today = datetime.now(tz).date()
        start_time_tz = tz.localize(datetime.combine(today, self.start_time)).time()
        end_time_tz = tz.localize(datetime.combine(today, self.end_time)).time()

        # Check if the current time falls within the time interval
        return start_time_tz <= now <= end_time_tz
