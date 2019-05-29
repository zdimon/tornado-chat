#!/usr/bin/env python
import redis
print('Testing redis connection')
redis_client = redis.Redis(host='localhost', port=6379, db=0)
channel = 'chat-channel'
print("Sending message to channel %s" % channel)
out = redis_client.publish( channel , 'my data')
print(out)