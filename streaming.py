from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy


from sets import Set
from datetime import datetime, timedelta

import json, re, time, urllib2

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.



fpos = open("pos.txt", "r")
fneg = open("neg.txt", "r")

pos_words = Set()
for line in fpos:
    if len(line) != 0:
        pos_words.add(line.strip().lower())

neg_words = Set()
for line in fneg:
    if len(line) != 0:
        neg_words.add(line.strip().lower())

def count_pos_neg(words):
    pos, neg = 0, 0
    for w in words:
        if w in pos_words:
            pos += 1
        if w in neg_words:
            neg += 1
    return pos, neg



last_sent = datetime.now()
votes = {"pos": 0, "neg":0}
tag = "bitcoin"

class StdOutListener(StreamListener):
    def on_data(self, data):
        global last_sent, votes
        try:
            data = json.loads(data)
            t = data.get('text')
            print data.get('created_at')
            if not t:
                return True
            text = t.lower()
            now = datetime.now()
            ht = tag
            if ht in text:
                text = re.sub(r'[^\w]', ' ', text)
                words = text.split(" ")
                pos, neg = count_pos_neg(words)
                votes["pos"] += pos
                votes["neg"] += neg
                if last_sent < now - timedelta(seconds=0):
                    query = ""
                    suma = 0
                    for k in votes:
                        query += k + "=" + str(votes[k]) + "&"
                        suma += votes[k]
                        votes[k] = 0
                    last_sent = now
                    query = query[:-1]
                    print query
                    response = urllib2.urlopen('http://localhost:8080/api/vote?' + query)
                    print response.getcode()
                    print response.read()
        except Exception:
            pass
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[tag])
