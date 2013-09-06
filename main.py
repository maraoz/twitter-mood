#!/usr/bin/env python


import webapp2, jinja2, os, hashlib, logging, urllib
import json
import datetime
from random import randint

from google.appengine.api import urlfetch
from google.appengine.ext import db

from model import TagMood


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])


tags = ["bitcoin"]

class JsonAPIHandler(webapp2.RequestHandler):
    def post(self):
        self.get()
    def get(self):
        resp = self.handle()
        self.response.headers['Content-Type'] = "application/json"
        dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        self.response.write(json.dumps(resp, default=dthandler))


class BootstrapHandler(JsonAPIHandler):
    def handle(self):
        db.delete(TagMood.all())
        return {"success":True}

class LatestHandler(JsonAPIHandler):
    def handle(self):
        return TagMood.get_latest_tag_moods(tags[0])

class VoteHandler(JsonAPIHandler):
    def handle(self):
        mood = TagMood(tag=tags[0], pos=0, neg=0)
        mood.pos = long(self.request.get("pos"))
        mood.neg = long(self.request.get("neg"))
        mood.put()
        return {"success":True}



app = webapp2.WSGIApplication([
    ('/api/bootstrap', BootstrapHandler),
    ('/api/latest', LatestHandler),
    ('/api/vote', VoteHandler)
], debug=True)

