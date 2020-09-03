import datetime
import json
from dashboard_api import led_out
import websocket
#from websocket import create_connection
import colorsys
import signal
import time
from threading import Thread
#for downloading messages:



################################################################################
#VAR SETUP:
create_connection = websocket.create_connection
access_token = credentials.pushbullet_token
PB_ws_url = "wss://stream.pushbullet.com/websocket/"+access_token
notification_stream = create_connection(PB_ws_url)
notification_list = []


################################################################################
#start of actual programm.
class DashBoard(object):
    """docstring for DashBoard."""

    def __init__(self):


def display_time(four_digit_time):
    datetoshow = datetime.datetime.today().weekday()
    if datetoshow==4:
        if int(four_digit_time) >= 620 and int(four_digit_time) < 2130:
            brightness = 1
        else:
            brightness = 0
    elif datetoshow==5:
        if int(four_digit_time) >= 1030 and int(four_digit_time) < 2130:
            brightness = 1
        else:
            brightness = 0
    elif datetoshow==6:
        if int(four_digit_time) >= 1030 and int(four_digit_time) < 2115:
            brightness = 1
        else:
            brightness = 0
    else:
        if int(four_digit_time) >= 620 and int(four_digit_time) < 2115:
            brightness = 1
        else:
            brightness = 0
    print(four_digit_time, datetoshow, len(notification_list), brightness)
    output_led.output_time(four_digit_time, datetoshow, len(notification_list), brightness)


def error_file(error_digit):
    try:
        message_to_append = "Error "+error_digit+": "+errors.errors[error_digit]
        message_to_log=str(datetime.datetime.now().strftime("%d/%m/%y - %H:%M")) + "   " + message_to_append + "\n"
        with open("../global_files/fatal-errors.txt","a") as f:
            f.write(message_to_log)
        f.close()
        #file gets uploaded through cronjob
    except:
        display_time("9999")


def get_notifications():
    global notification_stream
    try:
        output =  notification_stream.recv()
        output = json.loads(output)
    except:
        notification_stream = create_connection(PB_ws_url)
        output =  notification_stream.recv()
        output = json.loads(output)

    if output["type"] == "push":
        if output["push"]["type"] == "mirror":
            notification_title = output["push"]["title"]
            notification_content = output["push"]["body"]
            notification_id = output["push"]["notification_id"]
            notification_type = "notification"
            notification_all_content = {"title":notification_title,"content":notification_content,"id":notification_id}
        elif output["push"]["type"] == "dismissal":
            notification_type = "dismissal"
            notification_all_content = output["push"]["notification_id"]
    elif output["type"] == "nop":
        notification_type = "status_test"
        notification_all_content = []
    else:
        with open("../global_files/logs.txt","a") as f:
            f.write(str(datetime.datetime.now().strftime("%d/%m/%y - %H:%M")) + "  unnown notification" + "\n")
        f.close()

    return notification_type,notification_all_content


def run_script():
    previous_time = False
    while True:
        strtimerightformat = str(datetime.datetime.now().time())[0:5]
        four_digit_time = strtimerightformat[0:2]+strtimerightformat[3:]
        if running_var.display_notif_running == False:
                display_time(four_digit_time)
        time.sleep(5)



################################################################################
#Programm flow
time_thread = Thread(target=run_script)
time_thread.start()
print("UP")

while True:
    notification_type,notification_content = get_notifications()
    if notification_type == "notification":
        for _ in range(len(notification_list)):
            if str(notification_content["id"]) in notification_list[_].values():
                del notification_list[_]
        notification_list.append(notification_content)

        notification_thread = Thread(target=output_led.output_notification, args=(notification_content,))
        if running_var.display_notif_running:
            error_file(8)
        else:
            running_var.display_notif_running = True
            notification_thread.start()

    elif notification_type == "dismissal":
        try:
            for _ in range(len(notification_list)):
                if notification_content in notification_list[_].values():
                    del notification_list[_]

        except:
            notification_list = []
