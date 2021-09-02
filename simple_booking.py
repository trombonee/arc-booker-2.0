from datetime import datetime, time, date, timedelta
import threading
import json

from booker import Booker
import logging

CONFIG_FILE = 'user_config.json'
ZONE = 'lower-squatrack'
HOUR = 7
MINUTE = 45

logging.basicConfig(
        format= '%(asctime)s %(levelname)-8s %(message)s',
        filename='booking.log', 
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def main() -> None:
    userdata = load_userdata()

    booking_day = datetime.date(datetime.now() + timedelta(days=3))

    booking_time = time(HOUR, MINUTE)

    threads = []
    for user, data in userdata.items():
        thread = threading.Thread(target=booking_thread, args=(user, data, booking_day, booking_time, ZONE))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()


def booking_thread(user: str, data: dict, booking_day: date, booking_time: time, zone: str='lower-squatrack') -> None:
    logging.info('Begining booking for {} on thread {}'.format(user, threading.current_thread()))
    booker = Booker(booking_day, booking_time, data['username'], data['password'], zone)
    booker.book()



def load_userdata(config_filepath: str='user_config.json') -> dict:
    with open(config_filepath, 'r') as f:
        userdata = json.load(f)
    
    return userdata


if __name__ == '__main__':
    main()