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
import pifacedigitalio as p
from time import sleep
from pygame import mixer

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

mixer.pre_init(44100,-16,2,4096)
mixer.init()
mixer.music.load('/home/pi/google/voice-local/aiyprojects-raspbian/src/cracked_pepper_sir.mp3')
mixer.pause()

piface = p.PiFaceDigital()

x = 0

def main():
    global x
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text:
                if text.lower().find('cracked pepper') != -1:
                    print('cracking pepper')
                    x = 0
                    count = 0
                    piface.leds[0].turn_on()
                    while count < 20:
                        tick()
                        sleep(0.05)
                        print('cracking pepper')
                        count = count + 1 
                    piface.leds[0].turn_off()
                elif text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')
                    break
                else: 
                    print('You said "', text, '"')
                    mixer.unpause()
                    mixer.music.play()
                    mixer.pause()

def tick():
  global x
  x += 1
  if (x&1) > 0:
    piface.leds[2].turn_on()
  if (x&2) > 0:
    piface.leds[3].turn_on()
  if (x&4) > 0:
    piface.leds[4].turn_on()
  if (x&8) > 0:
    piface.leds[5].turn_on()
  if (x&16) > 0:
    piface.leds[6].turn_on()
  if (x&32) > 0:
    piface.leds[7].turn_on()
  sleep(0.1)
  piface.leds[2].turn_off()
  piface.leds[3].turn_off()
  piface.leds[4].turn_off()
  piface.leds[5].turn_off()
  piface.leds[6].turn_off()
  piface.leds[7].turn_off()

if __name__ == '__main__':
    main()
