
# TimeIntervalSensor for Apache Airflow

`TimeIntervalSensor` is a custom sensor for Apache Airflow that checks if the current time falls within a specified interval, while also supporting time zones. It's designed to enhance time-sensitive workflows by ensuring that tasks only proceed during the defined time window, making it ideal for business hours, processing windows, and global workflows that rely on multiple time zones.

## 🌟 Features

- **Time Interval Validation**: Define a start and end time, and the sensor will only allow tasks to proceed if the current time falls within that range.
- **Time Zone Support**: The sensor can handle multiple time zones, ensuring that tasks are executed at the correct time, regardless of the region.
- **Seamless Airflow Integration**: Easily integrate the `TimeIntervalSensor` into your DAGs, just like any other Airflow operator or sensor.

## 📦 Installation

You can install the package using `pip`:

```bash
pip install time-interval-sensor
```

## 🚀 Quick Start

Here’s a simple example of how to use `TimeIntervalSensor` in your Airflow DAGs:

```python
from airflow import DAG
from sensors.time_interval_sensor import TimeIntervalSensor
from datetime import datetime, time

default_args = {
    'start_date': datetime(2024, 1, 1),
}

with DAG(dag_id='time_interval_sensor_dag', default_args=default_args, schedule_interval=None) as dag:

    time_check = TimeIntervalSensor(
        task_id='check_time_interval',
        start_time=time(9, 0),  # 9:00 AM
        end_time=time(17, 0),   # 5:00 PM
        time_zone='America/New_York',
        timeout=30,               # Set timeout to 30 seconds
        mode='reschedule',        # Use 'reschedule' mode for the sensor
        poke_interval=5           # Poke every 5 seconds
    )
```

## 💡 Use Cases

- **Business Hours Execution**: Ensure that certain tasks are only run during specific working hours (e.g., 9 AM to 5 PM).
- **Global Time Zone Coordination**: Trigger tasks at the correct time in different time zones, making it easy to manage distributed workflows.
- **Time-Sensitive Processing**: Use the sensor to define a time window for batch jobs or data processing that depends on specific hours.

## 🔧 Parameters

- **start_time**: Start of the time interval (Python `time` object).
- **end_time**: End of the time interval (Python `time` object).
- **time_zone**: The name of the time zone to be used (default: 'UTC').
- **timeout**: Seconds after which task sensor will fail the task if not within time interval
- **mode**: (Optional) If you'd like to free up the worker slot between checks, you can set the mode to reschedule
- **poke_interval**: (Optional) If you want to test repeatedly with the given frequency in seconds 

## 📜 License

This project is licensed under the MIT License.
