
from google.appengine.ext import db

import logging, datetime, calendar


LATEST_N = 50

class TagMood(db.Model):
    
    timestamp = db.DateTimeProperty(auto_now_add=True)
    
    tag = db.StringProperty()
    pos = db.IntegerProperty()
    neg = db.IntegerProperty()
    
    @classmethod
    def get_latest_tag_moods(cls, tag):
        moods = cls.all().filter("tag =", tag).order("-timestamp").fetch(LATEST_N)
        pairs = []
        for mood in moods:
            pair = (mood.pos, mood.neg, (mood.timestamp.microsecond / 1000000.0) + calendar.timegm(mood.timestamp.utctimetuple()))
            pairs.append(pair)
        return pairs

