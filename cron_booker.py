
import sys
from booker import Booker
from datetime import datetime, timedelta, time
from userdata_app.update_userdata import return_data

script = sys.argv[0]
user = sys.argv[1]
booking_zone = sys.argv[2]
booking_time = sys.argv[3]


booking_day = datetime.date(datetime.now() + timedelta(days=3))

hour, minute = booking_time.split(':')

time_object = time(int(hour), int(minute))

user_data = return_data()

specific_user = user_data[user]

booker = Booker(booking_day, time_object, specific_user['username'], specific_user['password'], booking_zone)
print(str(datetime.now()), 'Begining booking for {}'.format(user))
booker.book()






