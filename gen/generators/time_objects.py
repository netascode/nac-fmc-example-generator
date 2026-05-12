"""
Time range object generators
"""

import random

WEEKDAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]


def _random_time():
    """Return a random HH:MM string on a 30-minute boundary."""
    hour = random.randint(0, 23)
    minute = random.choice([0, 30])
    return f"{hour:02d}:{minute:02d}"


def _generate_daily_recurrence():
    days = sorted(random.sample(WEEKDAYS, random.randint(1, 5)), key=WEEKDAYS.index)
    start = _random_time()
    end = _random_time()
    if end <= start:
        start, end = "08:00", "17:00"
    return {
        'recurrence_type': 'DAILY_INTERVAL',
        'daily_days': days,
        'daily_start_time': start,
        'daily_end_time': end,
    }


def _generate_range_recurrence():
    start_idx = random.randint(0, 5)
    end_idx = random.randint(start_idx + 1, 6)
    return {
        'recurrence_type': 'RANGE',
        'range_start_day': WEEKDAYS[start_idx],
        'range_start_time': _random_time(),
        'range_end_day': WEEKDAYS[end_idx],
        'range_end_time': _random_time(),
    }


def generate_time_ranges(time_ranges_number):
    """Generate time range objects with sequential names and random recurrences."""
    time_ranges = []
    for i in range(1, time_ranges_number + 1):
        if random.choice([True, False]):
            recurrence = _generate_daily_recurrence()
        else:
            recurrence = _generate_range_recurrence()
        time_ranges.append({
            'name': f'time_range_{i}',
            'recurrences': [recurrence],
        })
    return time_ranges
