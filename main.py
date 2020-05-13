# -*- coding: utf-8 -*-

from key import *
import requests
import time
import json
import datetime
import googlesearch
import emoji

chat_members = {}
base_url = "https://api.telegram.org/bot" + telegram_api + "/"
chat_id = ""
offset = 0

start_time = datetime.datetime.now()
message_read = 0
message_sent = 0


def bot_print_lorem(params):
    send_message("Lorem ipsum dolor sit amet....")

def bot_print_status(params):
    delta = str(datetime.datetime.now() - start_time)
    message = "<pre>Status: Running \nUptime: " + delta + "\nMessages read: " + str(message_read) + "\nMessages sent: " + str(message_sent) + "</pre>"
    send_message(message)

def bot_show_weather(params):
    if len(params) != 1:
        send_message("Invalid Syntax, please give one parameter, the location")
        return
    send_message("Probably sunny I guess? Yes yes I'm still learning")

def bot_google_search(params):
    if len(params) < 1:
        send_message("Please tell me what to look for")
        return
    param_string = ""
    for word in params:
        param_string += word + "+"
    param_string = param_string[:-1]
    search_url = "https://google.com/search?q=" + param_string
    try:
        res = googlesearch.search(param_string.replace("+"," ") ,num=5,start=0,stop=5)
        send_string = "Google search for <b>" + param_string.replace("+"," ") + "</b>:\n"
        for url in res:
            print(url)
            send_string += url + "\n\n"
        send_string += "Search url:\n" + search_url
    except:
        send_string = "Search url:\n" + search_url
    send_message(send_string)


def bot_print_events(params):
    events = {
        "anniversary" : datetime.date(datetime.datetime.now().year,12,7),
        "valentine's day": datetime.date(datetime.datetime.now().year,2,14),
        "Marine's birthday": datetime.date(datetime.datetime.now().year,8,31),
        "Remy's birthday": datetime.date(datetime.datetime.now().year,3,25),
    }
    send_string = "Upcoming events: \n"
    for key in events:
        delta = events[key] - datetime.date.today()
        if delta < datetime.timedelta(0):
            delta += datetime.timedelta(days = 365)
        send_string += key + ": " + str(delta.days) + " days \n"

    send_message(send_string)


def bot_emojify(params):

    if len(params) < 2:
        send_message(emoji.emojize("Please send a separator as the first argument, and the text afterwards.\nExample:\n/emojify :heart: Example text"))
    sep = params[0]
    emoji_dict = {"a" : ":regional_indicator_symbol_letter_a:","b" : ":regional_indicator_symbol_letter_b:","c" : ":regional_indicator_symbol_letter_c:","d" : ":regional_indicator_symbol_letter_d:","e" : ":regional_indicator_symbol_letter_e:","f" : ":regional_indicator_symbol_letter_f:","g" : ":regional_indicator_symbol_letter_g:","h" : ":regional_indicator_symbol_letter_h:","i" : ":regional_indicator_symbol_letter_i:","j" : ":regional_indicator_symbol_letter_j:","k" : ":regional_indicator_symbol_letter_k:","l" : ":regional_indicator_symbol_letter_l:","m" : ":regional_indicator_symbol_letter_m:","n" : ":regional_indicator_symbol_letter_n:","o" : ":regional_indicator_symbol_letter_o:","p" : ":regional_indicator_symbol_letter_p:","q" : ":regional_indicator_symbol_letter_q:","r" : ":regional_indicator_symbol_letter_r:","s" : ":regional_indicator_symbol_letter_s:","t" : ":regional_indicator_symbol_letter_t:","u" : ":regional_indicator_symbol_letter_u:","v" : ":regional_indicator_symbol_letter_v:","w" : ":regional_indicator_symbol_letter_w:","x" : ":regional_indicator_symbol_letter_x:","y" : ":regional_indicator_symbol_letter_y:","z" : ":regional_indicator_symbol_letter_z:"," " : sep}

    prep_string = ""
    for i in params[1:]:
        prep_string += i.lower() + " "
    out_string = ""
    for i in prep_string[:-1]:
        if i in emoji_dict:
            out_string += emoji_dict[i] + " "
        else:
            out_string += i
    send_message(emoji.emojize(out_string))




commands = {
    "status" : bot_print_status,
    "lorem" : bot_print_lorem,
    "weather" : bot_show_weather,
    "google" : bot_google_search,
    "events" : bot_print_events,
    "emojify" : bot_emojify,
}








def fetch_updates():
    update_url = base_url + "getUpdates"
    data = {"offset":offset}
    result = requests.post(update_url,data=data)
    try:
        result = result.json()["result"]
    except:
        result = ""
    return result

def send_message(message):
    print("SENDING: " + emoji.demojize(message))
    global message_sent
    data = {'chat_id': chat_id, 'text': message, "parse_mode": "HTML"}
    send_url = base_url + "sendMessage"
    r = requests.post(send_url, data=data)
    message_sent += 1

def handle_command(command):
    """Handles commands and stuff, using a bash-like syntax:
    /[command] [argument 1] [argument 2] ...
    """
    full = command.split(" ")
    if full[0] in commands:
        commands[full[0]](full[1:])
    else:
        send_message("Command <code>" + full[0] + "</code> not found. Please try again.")


def handle_result(result):
    """Inspects the message and reacts accordingly. Can easily be extended"""
    print("handling")
    for message_data in result:
        global chat_id
        global offset
        global message_read
        message_read += 1
        offset = message_data["update_id"] + 1
        message = message_data["message"]
        chat_id = message["chat"]["id"]
        author = message["from"]

        if author["id"] not in chat_members:
            chat_members[author["id"]] = author["first_name"] + " " + author["last_name"]
            send_message("Welcome to this chat " + chat_members[author["id"]] + " !")

        if "text" in message:
            print("Chat said: ", emoji.demojize(message["text"]))

            if "entities" in message:
                for entry in message["entities"]:
                    if entry["type"] == "bot_command":
                        handle_command(message["text"][1:])

        elif "photo" in message:
            print("Photo received, what do I do?")





def message_loop():
    while(True):
        result = fetch_updates()
        if len(result) == 0:
            print("Nada")
            time.sleep(5)
        else:
            handle_result(result)
            time.sleep(5)

message_loop()
