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

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

mixer.pre_init(44100,-16,2,4096)
mixer.init()
mixer.music.load('/home/pi/google/voice-local/aiyprojects-raspbian/src/cracked_pepper_sir.mp3')
mixer.pause()

#outtrack = mixer.Sound('/home/pi/google/voice-local/aiyprojects-raspbian/src/cracked_pepper_sir.mp3')

def main():
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
                    count = 0
                    while count < 20:
                        sleep(0.05)
                        print('cracking pepper')
                        count = count + 1 
                elif text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')
                    break
                else: 
                    print('You said "', text, '"')
                    mixer.unpause()
                    mixer.music.play()
                    mixer.pause()

if __name__ == '__main__':
    main()
