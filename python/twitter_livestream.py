#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Prasanna Venkadesh
License: Free Software (GPL V3)

Running this program will listen for the tweets on User's timeline using Twitters Streaming API.
If there are any retweets or favorites on the tweet of the user,
a buzzer beep will be played on the Arduino connected with the
computer.
"""


# import required modules
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from time import sleep
import serial
import json
import sys


# establish a serial connection to arduino board
try:
    serial_port = sys.argv[1]
    baud_rate = 115200
    arduino_serial_connection = serial.Serial(serial_port, baud_rate)
    print "Connection establised on %s" % serial_port
    arduino_serial_connection.write('99')
except IndexError:
    print "No Arduino device port specified. Exit"
    sys.exit()
except BaseException, be:
    print be.message
    sys.exit()


# variables required for twitter authentication
access_token = 'YOUR_ACCESS_TOKEN_HERE'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET_HERE'
consumer_key = 'YOUR_CONSUMER_KEY_HERE'
consumer_secret = 'YOUR_CONSUMER_SECRET_HERE'
screen_name = 'YOUR_TWITTER_HANDLE_WITHOUT_@_SYMBOL_HERE'


class StdOutListener(StreamListener):

    def play_sound(self):
        # plays a beep on Arduino to notify the user
        arduino_serial_connection.write('1')
        sleep(4)
        arduino_serial_connection.write('99')

    def on_data(self, data):

        json_data = json.loads(data)

        try:
            if json_data.get('entities'):
                for user in json_data.get('entities').get('user_mentions'):
                    if user.get('screen_name') == screen_name:
                        print "You have a RT / MENTION"
                        print json_data.get('text')
                        self.play_sound()
            elif json_data.get('event'):
                if json_data.get('target').get('screen_name') == screen_name:
                    print "%s (%s) has %sd," % (json_data.get('source').get('name'),
                                                json_data.get('source').get('screen_name'),
                                                json_data.get('event'))
                    print json_data.get('target_object').get('text')
                    self.play_sound()

        except BaseException, be:
            print be.message

        return True

    def on_error(self, status):
        print "Error: %s" % status


if __name__ == '__main__':

    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    stream.userstream()
