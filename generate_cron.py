
from crontab import CronTab
from userdata_app.update_userdata import return_data
from datetime import time

VENV = '/home/lucat/Documents/arc-booker-2.0/.venv/bin/python'
BOOKER = '/home/lucat/Documents/arc-booker-2.0/cron_booker.py'

WEEKDAY_DICT = {
    'Sunday': 4,
    'Monday': 5,
    'Tuesday': 6,
    'Wednesday': 0,
    'Thursday': 1,
    'Friday': 2,
    'Saturday': 3,
}

def update_crontabs() -> None:
    user_data = return_data()

    cron = CronTab(user=True)

    for user, data in user_data.items():
        for day, booking_data in data['bookings'].items():
            if booking_data['zone'] and booking_data['zone'] != 'None':
                cron_time = generate_cron_time(day, booking_data['time'])
                cron_command = generate_cron_command(user, booking_data['zone'], booking_data['time'])

                job = cron.new(command=cron_command)
                job.setall(cron_time)
    
    cron.write()

def generate_cron_time(day: str, time: str) -> str:
    hour, minute = time.split(':')
    
    hour = int(hour)
    minute = int(minute)

    day_digit = WEEKDAY_DICT[day]

    return '{} {} * * {}'.format(minute, hour, day_digit)

def generate_cron_command(user: str, booking_zone: str, booking_time: str) -> str:
    command = '{} {} {} {} {} >> {}.log'.format(VENV, BOOKER, user, booking_zone, booking_time, user)

    return command


if __name__ == '__main__':
    update_crontabs()
