from time import sleep
import RPi.GPIO as GPIO

PIN = 40
SLEEP_TIME = 10

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

try:
	while True:
		GPIO.output(PIN, GPIO.HIGH)
		sleep(2)
		GPIO.output(PIN, GPIO.LOW)
		sleep(2)
except:
	# Keyboard interrupt
	GPIO.output(PIN, GPIO.LOW)
