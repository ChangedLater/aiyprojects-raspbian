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
        self.currentAngle = 180

    def start(self):
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin,self.cycle)
        self.pwm.start(self.centreDuty)

    def _moveTo(self,angle):
        duty = self.centreDuty + (angle-180) * (self.dutyShift/90)
        print(duty)
        self.pwm.ChangeDutyCycle(duty)
        self.currentAngle = angle

    def moveTo(self,angle):
        newAngle = angle + 180
        if(newAngle > self.maxAngle):
            newAngle = self.maxAngle
        if(newAngle < self.minAngle):
            newAngle = self.minAngle
        direction = 1
        if( newAngle < self.currentAngle ):
            direction = -1
        while( newAngle != self.currentAngle ):
            step = min( abs(newAngle - self.currentAngle), 10) 
            self._moveTo( self.currentAngle + direction * step)
            sleep(0.2)        

    def close(self):
        self.pwm.stop()
        GPIO.cleanup()


def create(pin):
    return Motor(pin)
