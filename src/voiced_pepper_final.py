#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import logging

import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
from time import sleep
from pygame import mixer
from datetime import datetime
import RPi.GPIO as GPIO
import motor

import socket
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

mixer.pre_init(44100,-16,2,4096)
mixer.init()
mixer.music.load('/home/pi/google/voice-local/aiyprojects-raspbian/src/cracked_pepper_sir.mp3')
mixer.pause()

listening = False
status_ui = aiy.voicehat.get_status_ui()
status_ui.status('starting')
assistant = aiy.assistant.grpc.get_assistant()
recorder = aiy.audio.get_recorder()
recorder.start()

# setup all gpio and servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
servo = motor.create(17)
servo.start()
servo.moveTo(50)


def main():
    global listening
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
     
    try:
        s.bind(('', 8888))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    s.listen(1)
    
    while True:
        print('Waiting for a connection')
        #wait to accept a connection - blocking call
        conn, addr = s.accept()         
        conn.close()
        listen()
    
    
def listen():
    global status_ui
    global assistant
    global recorder
    offer_pepper()
    d1 = datetime.now()
    d2 = datetime.now()
    while (d2 - d1).seconds < 10:
        status_ui.status('ready')
        status_ui.status('listening')
        print('Listening...')
        text, audio = assistant.recognize()
        if text:
            if text.lower().find('cracked pepper') != -1:
                print('cracking pepper')
                crack_pepper()
            elif text == 'goodbye':
                status_ui.status('stopping')
                print('Bye!')
                break
            else: 
                print('You said "', text, '"')
                offer_pepper()
        d2 = datetime.now()

def crack_pepper():
    global servo
    servo.moveTo(-20)
    GPIO.output(19,GPIO.HIGH)
    sleep(2)
    GPIO.output(19,GPIO.LOW)
    servo.moveTo(50)

def offer_pepper():
    mixer.unpause()
    mixer.music.play()
    mixer.pause()
    sleep(3)

if __name__ == '__main__':
    main()
