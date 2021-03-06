# arc-booker-2.0

## Backstory

The gym at my school is very convenient in the sense that it has decent enough equipment, is close to my house and included in my tuition fees. 

There is one major flaw however... everytime you want to go, you must book a time slot in a specific section. Due to the number of students at school the slots fill extremely quickly.

Last year my solution to this was to create a simple Python script which could automatically book my desired time slot when it released. As my coding skills improved over the summer, I decided to take things to another level this year developing a system of Python scripts allowing for fully customizable time slot selection with a UI! I even setup a Raspberry PI which acted as a server for running these scripts.

Below showcases how I accomplished everything and some images.

**NOTE:** This was accomplished in roughly one week

## Components

### [Booker](https://github.com/trombonee/arc-booker-2.0/blob/main/booker.py)
This file contains the workhorse class responsible for actually checking out time slots from the gym's website. It uses Selenium and Firefox to automate these tasks. The major improvement from last year here was making use of implicit waits for website components to load instead of hardcoding explicit wait times. This greatly reduces the checkout time required for the script.

### [UI Application](https://github.com/trombonee/arc-booker-2.0/tree/main/userdata_app)
This folder contains two Python files. The [Application](https://github.com/trombonee/arc-booker-2.0/blob/main/userdata_app/application.py) file is the UI that can be used to customize booking times on any given day of the week.

Here is a screenshot of it:

![UI](https://raw.githubusercontent.com/trombonee/arc-booker-2.0/main/readme_img/arc-booker-ui.png)

As seen in the image above users can be updated, created and deleted with the UI. One thing to note is that each time a user is modified, an updated configuration file (containing booking information) is pushed to a seperate private repository basically acting like a non-relational database.

These configuration files are then pulled onto my Raspberry PI which handles the remaining tasks.

### [Cron Generator](https://github.com/trombonee/arc-booker-2.0/blob/main/generate_cron.py)
Having a file containing the data about when I'd like to go to the gym is nice and all but without something telling the PI to execute at those desired times, it would be useless. Thats where this script comes in. It automatically generates the cron tasks according the desired booking times and creates a crontab with them.

### [Cron Booker](https://github.com/trombonee/arc-booker-2.0/blob/main/cron_booker.py)
This script is what the cron tasks are told to run. It takes in command line arguments for the user it's booking for, the desired zone, and time. It will then book three days in advance of the desired time.

### [Simple Booking](https://github.com/trombonee/arc-booker-2.0/blob/main/simple_booking.py)
Before creating all the stuff above, I was anxious to put the booker to use so I made this simple booking script. It works by reading a user config JSON file (containing login information and desired gym zone) and will book at the time specified by the constants at the top of the script.

To use this script make your own config file with updated information, update the constants to your desired booking time and finally setup a crontab task to automatically run the script at that booking time. (This script books three days in advance since each time slot comes out 72 hours before its start time)

### [Links](https://github.com/trombonee/arc-booker-2.0/blob/main/links.py)
Dictionaries containing relevant information about booking zones (links, start times, end times)
