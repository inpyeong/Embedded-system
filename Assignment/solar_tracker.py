import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15


##servo##########################
GPIO.setmode(GPIO.BCM)

pan = 5 #left and right
tilt = 6 #up and down

GPIO.setup(pan, GPIO.OUT)
GPIO.setup(tilt, GPIO.OUT)

pos_center = 5.5

pan = GPIO.PWM(pan, 50)
pan.start(pos_center)

tilt = GPIO.PWM(tilt,50)
tilt.start(pos_center)
#################################

##ADC1115########################
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
#################################


panDutycycle = 5.5
tiltDutycycle = 5.5


while True:
    values = [0]*4
    values[0] = adc.read_adc(0, gain=GAIN) #upleft
    values[1] = adc.read_adc(1, gain=GAIN) #upright
    values[2] = adc.read_adc(2, gain=GAIN) #downleft
    values[3] = adc.read_adc(3, gain=GAIN) #downright
    print(values[0], values[1], values[2], values[3])




     if values[0] - values[1] > 200:    #upleft is lighter than upright
        panDutycycle += 0.05
        time.sleep(0.009)

    if values[2] - values[3] > 200:    #downleft is lighter than downright
        panDutycycle += 0.05
        time.sleep(0.009)

    if values[1] - values[0] > 200:    #upright is lighter than upleft
        panDutycycle -= 0.05
        time.sleep(0.009)

    if values[3] - values[2] > 200:    #downright is lighter than downleft
        panDutycycle -= 0.05
        time.sleep(0.009)




    if values[0] - values[2] > 400:    #upleft is lighter than downleft
        tiltDutycycle += 0.03
        time.sleep(0.01)

    if values[1] - values[3] > 400:    #upright is lighter than downright
        tiltDutycycle += 0.03
        time.sleep(0.01)

    if values[2] - values[0] > 200:    #downleft is lighter than upleft
        tiltDutycycle -= 0.05
        time.sleep(0.01)

    if values[3] - values[1] > 200:    #downright is lighter than upright
        tiltDutycycle -= 0.05
        time.sleep(0.01)



#######################################
 
    if panDutycycle > 9:
        panDutycycle = 9
        time.sleep(0.05)

    if panDutycycle < 2:
        panDutycycle = 2
        time.sleep(0.05)

    if tiltDutycycle > 9:
        tiltDutycycle = 9
        time.sleep(0.05)

    if tiltDutycycle < 2:
        tiltDutycycle = 2
        time.sleep(0.05)

    pan.ChangeDutyCycle(panDutycycle)
    tilt.ChangeDutyCycle(tiltDutycycle)
