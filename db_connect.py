# Imports firebase libraries in order to connect to the database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

def init():
    # Sets the credentials using the key that firebase generated
    # if the key is in a seperate folder you have to type out the
    # full path to the key
    cred = credentials.Certificate("poker-29f47-firebase-adminsdk-2dx1i-1877cc63ac.json")

    # Connects to the database using the credentials
    firebase_admin.initialize_app(cred)
    return firestore.client()