from tkinter import *
from threading import *
from datetime import datetime
import random  
import string 
import time
import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyCOG4GlWY9DFrmsdZlJ2T8H2vNFfzniHro",
    'authDomain': "vechicle-dimension.firebaseapp.com",
    'databaseURL': "https://vechicle-dimension-default-rtdb.firebaseio.com",
    'projectId': "vechicle-dimension",
    'storageBucket': "vechicle-dimension.appspot.com",
    'messagingSenderId': "544081464635",
    'appId': "1:544081464635:web:11477486968eb043d8fb1e",
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
 

def make_id(length):
    result = ''.join((random.choice(string.ascii_letters) for x in range(length)))
    result = "VEH" + result
    return result 


def run_time():
    current = datetime.now()
    current = current.replace(microsecond=0)
    label_time.config(text=current)
    time.sleep(1)
    Thread(target=run_time).start()


def get_config():
    config = db.child("config").get()
    in_lenght.insert(0, config.val()["distance_length"])
    in_width.insert(0, config.val()["distance_width"])


def set_config():
    data = {
        "distance_length": in_lenght.get(),
        "distance_width": in_width.get()
    }
    db.child("config").set(data)


def get_data():
    config = db.child("config").get()
    in_lenght.insert(0, config.val()["distance_length"])
    in_width.insert(0, config.val()["distance_width"])


def upload_data():
    data = {
        "at": str(datetime.now().replace(microsecond=0)),
        "l": out_length.get(),
        "w": out_width.get(),
        "h":out_height.get(),
        "wheels":out_wheels.get(),
    }
    db.child("dimension").child(make_id(12)).set(data)
    out_length.delete(0, END)
    out_width.delete(0, END)
    out_height.delete(0, END)
    out_wheels.delete(0, END)

w = 600
h = 400
root = Tk()
root.geometry(f'{w}x{h}')

root.title("Dimension")

label_time = Label(root, text="sdad")

distance_length = Label(root, text="Length of Sensor (LS)")
distance_width = Label(root, text="Width of Sensor (WS)")
in_lenght = Entry(root, width=20)
in_width = Entry(root, width=20)

button_load = Button(root, width=10, height=2, text="Execute", command=get_data)
button_upload = Button(root, width=10, height=2, text="Upload", command=upload_data)
button_config = Button(root, width=10, height=2, text="Save Config", command=set_config)

label_length = Label(root, text="Length")
label_width = Label(root, text="Width")
label_height = Label(root, text="Height")
label_wheels = Label(root, text="Wheels")

out_length = Entry(root, width=10)
out_width = Entry(root, width=10)
out_height = Entry(root, width=10)
out_wheels = Entry(root, width=10)

out_wb1 = Entry(root, width=10)
out_wb2 = Entry(root, width=10)
out_wb3 = Entry(root, width=10)
out_wb4 = Entry(root, width=10)

distance_length.place(y=20, x=15)
distance_width.place(y=50, x=15)
in_lenght.place(y=20, x=140)
in_width.place(y=50, x=140)

label_time.place(y=10, x=400)

button_load.place(y=300, x=140)
button_upload.place(y=300, x=240)
button_config.place(y=300, x=40)

label_length.place(y=100, x=80)
label_width.place(y=130, x=80)
label_height.place(y=160, x=80)
label_wheels.place(y=190, x=80)
out_length.place(y=100, x=140)
out_width.place(y=130, x=140)
out_height.place(y=160, x=140)
out_wheels.place(y=190, x=140)

out_wb1.place(y=100, x=300)
out_wb2.place(y=130, x=300)
out_wb3.place(y=160, x=300)
out_wb4.place(y=190, x=300)


run_time()
get_config()
root.mainloop()