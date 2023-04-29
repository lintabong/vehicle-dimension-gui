import os
import pyrebase

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class Firebase():
    def __init__(self) -> None:
        FIREBASE_APIKEY          = os.getenv("FIREBASE_APIKEY")
        FIREBASE_AUTHDOMAIN      = os.getenv("FIREBASE_AUTHDOMAIN")
        FIREBASE_DATABASEURL     = os.getenv("FIREBASE_DATABASEURL")
        FIREBASE_PROJECTID       = os.getenv("FIREBASE_PROJECTID")
        FIREBASE_STORAGEBUCKET   = os.getenv("FIREBASE_STORAGEBUCKET")
        FIREBASE_MESSAGESENDERID = os.getenv("FIREBASE_MESSAGESENDERID")
        FIREBASE_APPID           = os.getenv("FIREBASE_APPID")

        firebaseConfig = {
            "apiKey": FIREBASE_APIKEY,
            "authDomain": FIREBASE_AUTHDOMAIN,
            "databaseURL": FIREBASE_DATABASEURL,
            "projectId": FIREBASE_PROJECTID,
            "storageBucket": FIREBASE_STORAGEBUCKET,
            "messagingSenderId": FIREBASE_MESSAGESENDERID,
            "appId": FIREBASE_APPID,
        }

        self.conn = pyrebase.initialize_app(firebaseConfig)
        self.db   = self.conn.database()

    def get_config(self):
        config = self.db.child("config").get().val()

        distance_length = int(config["distance_length"])
        distance_width  = int(config["distance_width"])
        return distance_length, distance_width
    
    def set_config(self, dl, dw):
        data = {
            "distance_length": dl,
            "distance_width": dw
        }

        self.db.child("config").set(data)

    def upload_data(self, path, lenght, weight, height, wheels):
        data = {
            "at": str(datetime.now().replace(microsecond=0)),
            "l": lenght,
            "w": weight,
            "h": height,
            "wheels": wheels,
        }

        self.db.child("dimension").child(path).push(data)
