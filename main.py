import sys
import os
import time
import threading
import ctypes
import tkinter
import serial
import re

from datetime import datetime
from tkinter import END
from dotenv import load_dotenv
from lib.firebase import Firebase
from serial.tools import list_ports

sys.path.insert(1, os.path.abspath(os.path.join(os.getcwd())))

load_dotenv()
ctypes.windll.shcore.SetProcessDpiAwareness(1)

TITLE      = os.getenv("TITLE")
WIDTH      = int(os.getenv("WIDTH"))
HEIGHT     = int(os.getenv("HEIGHT"))
RED        = f'#{os.getenv("RED")}'
GREEN      = f'#{os.getenv("GREEN")}'
WHITE      = f'#{os.getenv("WHITE")}'
ORANGE     = f'#{os.getenv("ORANGE")}'
LIGHT_BLUE = f'#{os.getenv("LIGHT_BLUE")}'
BLUE       = f'#{os.getenv("BLUE")}'
BLACK      = f'#{os.getenv("BLACK")}'
GRAY       = f'#{os.getenv("GRAY")}'

firebase = Firebase()


root = tkinter.Tk()
root.geometry(f'{WIDTH}x{HEIGHT}')
root.title(TITLE)
root.option_add("*Font", 40)
root.resizable(False, False)
root.overrideredirect(False)


def run_time():
    current = datetime.now()
    current = current.replace(microsecond=0)
    current_time.config(text=current)
    time.sleep(1)
    threading.Thread(target=run_time).start()


def get_config():
    config = firebase.get_config()

    in_lenght.insert(0, config[0])
    in_width.insert(0, config[1])


def set_config():
    dl = int(in_lenght.get())
    dw = int(in_width.get())

    firebase.set_config(dl, dw)


def get_data():
    global ser

    dl = int(in_lenght.get())
    dw = int(in_width.get())

    print(dl, dw)

    out_length.delete(0, END)
    out_width.delete(0, END)
    out_height.delete(0, END)
    out_wheels.delete(0, END)
    out_jbb.delete(0, END)
    out_sumbu1.delete(0, END)
    out_sumbu2.delete(0, END)
    out_mst.delete(0, END)

    ser.write((bytes("a", 'utf-8')))

    while True:
        data = str(ser.readline())
        if data != "b\'\'":
            data = re.sub(r"(b'|\\r|\\n')", "", data)

            data = data.split(",")

            print(data)

            lenght = (dl - (int(data[0]) + int(data[1])))
            width = (dw - (int(data[2]) + int(data[3])))
            height = int(os.getenv("HEIGHT_SENSOR")) - int(data[4])

            out_length.insert(0, lenght)
            out_width.insert(0, width)
            out_height.insert(0, height)
            out_wheels.insert(0, data[3])

            break


def upload_data():
    now = datetime.now()

    path = f'{now.year}/{now.month}/{now.day}'
    lenght = int(out_length.get())
    weight = int(out_width.get())
    height = int(out_height.get())
    wheels = int(out_wheels.get())

    firebase.upload_data(path, lenght, weight, height, wheels)


def scan_serial():
    listB.delete(0, 10)
    myList = list_ports.comports()
    for i, serialReady in enumerate(myList):
        listB.insert(i, serialReady)


def connect_serial():
    global ser
    global selectedPort
    for i in listB.curselection():
        selectedItem = listB.get(i)

        # if windows
        if re.search(r"COM", selectedItem) is not None:
            selectedPort = selectedItem[:4]
            print(selectedPort)

        # if linux

    ser = serial.Serial(
        selectedPort,
        115200,
        timeout=0.05
    )
    # root.after(3000, threading.Thread(target=).start)



# FRAME CONTROLLER
DATE = tkinter.Frame(root, bg=ORANGE, width=WIDTH, height=40)
DATE.place(x=0, y=0)

SETTING = tkinter.Frame(root, bg=LIGHT_BLUE, width=WIDTH, height=120)
SETTING.place(x=0, y=40)

BODY = tkinter.Frame(root, bg=GRAY, width=WIDTH, height=320)
BODY.place(x=0, y=160)


# STATIC
tkinter.Label(SETTING, bg=LIGHT_BLUE, fg=BLACK, text="Length of Sensor (LS)").place(x=15, y=25)
tkinter.Label(SETTING, bg=LIGHT_BLUE, fg=BLACK, text="Width of Sensor (WS)").place(x=15, y=55)

tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="Length").place(x=15, y=25)
tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="Width").place(x=15, y=55)
tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="Height").place(x=15, y=85)
tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="Wheels").place(x=15, y=115)

tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="JBB").place(x=245, y=25)
tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="Sumbu 1").place(x=245, y=55)
tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="Sumbu 2").place(x=245, y=85)
tkinter.Label(BODY, bg=GRAY, fg=BLACK, text="MST").place(x=245, y=115)

listB = tkinter.Listbox(BODY, height=3, width=34)

# DINAMIC
current_time = tkinter.Label(DATE, bg=ORANGE, fg=WHITE, text="")

in_lenght = tkinter.Entry(SETTING, width=10)
in_width  = tkinter.Entry(SETTING, width=10)

out_length = tkinter.Entry(BODY, width=10)
out_width  = tkinter.Entry(BODY, width=10)
out_height = tkinter.Entry(BODY, width=10)
out_wheels = tkinter.Entry(BODY, width=10)

out_jbb    = tkinter.Entry(BODY, width=10)
out_sumbu1 = tkinter.Entry(BODY, width=10)
out_sumbu2 = tkinter.Entry(BODY, width=10)
out_mst    = tkinter.Entry(BODY, width=10)

but_load   = tkinter.Button(BODY, width=10, height=2, text="Execute", command=get_data)
but_upload = tkinter.Button(BODY, width=10, height=2, text="Upload", command=upload_data)
but_config = tkinter.Button(SETTING, width=10, height=2, text="Save Config", command=set_config)
but_scan   = tkinter.Button(BODY, text="Scan", width=10, height=2, command=scan_serial)
but_conn   = tkinter.Button(BODY, text="Connect", width=10, height=2, command=connect_serial)


# PLACEMENT
current_time.place(x=810, y=10)
in_lenght.place(x=240, y=25)
in_width.place(x=240, y=55)

out_length.place(x=110, y=25)
out_width.place(x=110, y=55)
out_height.place(x=110, y=85)
out_wheels.place(x=110, y=115)

out_jbb.place(x=330, y=25)
out_sumbu1.place(x=330, y=55)
out_sumbu2.place(x=330, y=85)
out_mst.place(x=330, y=115)

but_load.place(y=200, x=50)
but_upload.place(x=160, y=200)
but_config.place(x=360, y=25)
but_scan.place(x=480, y=200)
but_conn.place(x=600, y=200)

listB.place(x=500, y=25)

run_time()
get_config()
root.mainloop()
