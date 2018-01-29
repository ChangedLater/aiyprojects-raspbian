import pifacedigitalio as p
from random import randint
from time import sleep

piface = p.PiFaceDigital() 

x = 0

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

for count in range(1,63):
  tick()
