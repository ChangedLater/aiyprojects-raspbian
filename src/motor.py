import RPi.GPIO as GPIO
from time import sleep  
GPIO.setmode(GPIO.BCM)

class Motor:
    def __init__(self,pin):
        self.pin = pin
        self.cycle = 50
        self.minAngle = 90
        self.maxAngle = 270
        self.centreDuty = 7.5 #the duty cycle for the centre position
        self.dutyShift = 5 #the duty cycle difference to move by 90 degrees

    def start(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin,self.cycle)
        self.pwm.start(self.centreDuty)

    def moveTo(self,angle):
        angle = angle + 180
        if(angle > self.maxAngle):
            angle = self.maxAngle
        if(angle < self.minAngle):
            angle = self.minAngle
        duty = self.centreDuty + (angle-180) * (self.dutyShift/90)
        print(duty)
        self.pwm.ChangeDutyCycle(duty)

    def close(self):
        self.pwm.stop()
        GPIO.cleanup()


def create(pin):
    return Motor(pin)
