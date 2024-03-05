import RPi.GPIO as GPIO
import pigpio
from time import sleep
import keyboard

# Configuracion GPIO
GPIO.setmode(GPIO.BCM)

pi = pigpio.pi()

ESC_GPIO = 18
pi.set_servo_pulsewidth(ESC_GPIO,0)

sleep(0.1)

band = True

while band:
    
    speed = input("velocidad: ")
    
    if speed == "s":
        pi.set_servo_pulsewidth(ESC_GPIO,0)
        print("Programa terminado")
        band = False
    else:
        speed = float(speed)
        pi.set_servo_pulsewidth(ESC_GPIO,speed)
        sleep(0.01)
