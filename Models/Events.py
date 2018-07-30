from pymongo import MongoClient
import datetime
import humanize
from bson.objectid import ObjectId
import pymongo


class Events:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.eventsNsit
        self.Users = self.db.users
        self.Events = self.db.events

    def add_event(self, data):
        inserted = self.Events.insert({
            "username": data.username,
            "event-name": data.eventname,
            "society": data.society,
            "venue": data.venue,
            "description": data.desc,
            "duration": data.duration,
            "date": data.date,
            "time": data.time,
            "date_added": datetime.datetime.now(),
            "date_updated": datetime.datetime.now()
        })

    def get_all_events(self, u):
        all_events = self.Events.find({
            "username": u
        }).sort("date_added", pymongo.DESCENDING)
        new_events = []
        for event in all_events:
            event["user"] = self.Users.find_one({"username": event["username"]})
            event["timestamp"] = humanize.naturaltime(datetime.datetime.now() - event["date_added"])
            event["updatestamp"] = humanize.naturaltime(datetime.datetime.now() - event["date_updated"])
            new_events.append(event)
        return new_events

    def get_events_that_can_be_updated(self, u):
        datemask = "%Y-%m-%d"
        events = self.Events.find({
            "username": u
        }).sort("date_added", pymongo.DESCENDING)
        new_events = []
        for event in events:
            event["user"] = self.Users.find_one({"username": event["username"]})
            date = event["date"]
            c_date = datetime.datetime.strptime(date, datemask)
            if c_date >= datetime.datetime.today():
                new_events.append(event)
        return new_events

    def get_event(self, id):
        event = self.Events.find_one({"_id": ObjectId(id)})
        return event

    def upcoming_events(self):
        datemask = "%Y-%m-%d"
        events = self.Events.find().sort("date_added", pymongo.DESCENDING)
        new_events = []
        for event in events:
            event["user"] = self.Users.find_one({"username": event["username"]})
            date = event["date"]
            c_date = datetime.datetime.strptime(date, datemask)
            event["TimeStamp"] = humanize.naturaltime(datetime.datetime.now() - c_date)
            event["ndate"] = humanize.naturaldate(c_date)
            if c_date >= datetime.datetime.today():
                new_events.append(event)
        return new_events

    def recent_events(self):
        datemask = "%Y-%m-%d"
        events = self.Events.find().sort("date_added", pymongo.DESCENDING)
        new_events = []
        for event in events:
            date = event["date"]
            c_date = datetime.datetime.strptime(date, datemask)
            event["TimeStamp"] = humanize.naturaltime(datetime.datetime.now() - c_date)
            event["ndate"] = humanize.naturaldate(c_date)
            if c_date < datetime.datetime.today():
                new_events.append(event)
        return new_events

    def del_post(self, id):
        self.Events.remove({"_id": ObjectId(id)})

    def update_event(self, id, data):
        print(data)
        x = self.Events.find_one({"_id": ObjectId(id)})
        print(x)

        self.Events.update_one({
            "_id": ObjectId(id)},
            {"$set": data})

    def events_all(self):
        datemask = "%Y-%m-%d"
        events = self.Events.find().sort("date_added", pymongo.DESCENDING)
        new_events = []
        for event in events:
            date = event["date"]
            c_date = datetime.datetime.strptime(date, datemask)
            event["TimeStamp"] = humanize.naturaltime(datetime.datetime.now() - c_date)
            event["ndate"] = humanize.naturaldate(c_date)
            new_events.append(event)
        return new_events
