from pymongo import MongoClient
import bcrypt


class RegisterModel:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.eventsNsit
        self.Users = self.db.users

    def insert_user(self, data):
        hashedPw = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        id = self.Users.insert({
            "Full Name": data.name,
            "username": data.username,
            "email": data.email,
            "password": hashedPw
        })
        # print("uid is", id)

    def check_username(self, data):
        x = self.Users.find({"username": data.username}).count()

        if x == 0:
            return True

        else:
            return False
