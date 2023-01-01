import os
import schedule
import time
import sys
from datetime import datetime

# populate this with numbers as strings like so:
# +1XXXYYYZZZZ
# ex: +19990001111
# +1 is always there. idk if this works for other country codes.
recipients = []

# method for formatting numbers when copied off of contacts app on MacOS
def format_numbers(numbers):
    return [x.replace("(", "").replace(")", "").replace(" ", "").replace(
        "-", "").replace("\u202d", "").replace("\u202c", "") for x in numbers]


def send_messages(recipients, message: str):
    for recipient in recipients:
        os.system("osascript sendMessage.applescript {} {}".format(
            recipient, message))


def listen(sleep_duration=5):
    schedule.run_pending()
    print("checking time... {}".format(
        datetime.now().strftime("%H:%M:%S")))
    time.sleep(sleep_duration)


time_to_send = ""
confirmation = ""
msg = ""
time_passed = False

while confirmation not in ["yes", "y"]:
    time_to_send = input(
        "when would you like to send the message? use 24 hour format. e.g. 05:07 for 5:07 am: (XX:YY): ")
    if len(time_to_send) != 5 or time_to_send[2] != ":" or any(c.isalpha() for c in time_to_send):
        raise ValueError(
            'your data is not formatted correctly. please use 24 hour format.')
    confirmation = input(
        f'does this time look correct? {datetime.strptime(time_to_send, "%H:%M").strftime("%I:%M %p")} (y/n): ').lower()


msg = input("what would you like to say to them?: ")

sleep_duration = input(
    "(optional), sleep duration? (how many seconds until it fetches the time again, default is 5 seconds): (num/ENTER): ")

if sleep_duration != "":
    sleep_duration = int(sleep_duration)

schedule.every().day.at(time_to_send).do(
    send_messages, recipients, f"'{msg}'")

while True:
    t = datetime.now().time()
    if sleep_duration != "":
        listen(sleep_duration)
    else:
        listen()
    if (t > datetime.strptime(time_to_send, "%H:%M").time()):
        sys.exit("message has been sent to the number(s). bye!")
