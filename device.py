import time
from azure.iot.device import IoTHubDeviceClient
import json
import platform

# These will not work on Windows, so testing must be done on the RPi.
import RPi.GPIO as GPIO
import RGB1602

RED_LED=40
GREEN_LED=38

CONNECTION_STRING = "HostName=oe-iot.azure-devices.net;DeviceId=omar-rpi;SharedAccessKey=IH0lOtSxLo/q3hARsr7xPzp5zmeoYG5yBddYFNclxmM="
NOTIFICATION_KEY = "notification"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# Set the pins to LOW to start with
GPIO.output(RED_LED, GPIO.LOW)
GPIO.output(GREEN_LED, GPIO.LOW)

lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(255,0,0)

def message_handler(message):
    """
    Handles the message from Azure IoT Hub
    """
    GPIO.output(GREEN_LED, GPIO.HIGH)
    lcd.setRGB(255, 255, 255)
    lcd.setCursor(0, 0)
    lcd.printout("new message")

    print("message received")
    message_dict = vars(message)
    
    message_data = message_dict["data"]
    print("message: {}".format(message_data))
    notification_data = json.loads(message_data)
    if NOTIFICATION_KEY in notification_data:
        notification_message = notification_data[NOTIFICATION_KEY]
        time.sleep(2)
        lcd.clear()
        lcd.setCursor(0, 0)
        lcd.printout(str(notification_message))
        message_length = len(notification_message)
        if message_length > 16:
            # only scroll if we need to
            scroll_amount = len(notification_message) - 16 # e.g. 2
            for x in range(scroll_amount): # 0, 1
                time.sleep(0.5)
                lcd.scrollLeft()

        time.sleep(5)

        for x in range(3):
            time.sleep(1)
            GPIO.output(GREEN_LED, GPIO.LOW)
            time.sleep(1)
            GPIO.output(GREEN_LED, GPIO.HIGH)

        lcd.setRGB(0,0,0)
        lcd.clear()
        time.sleep(1)
        GPIO.output(GREEN_LED, GPIO.LOW)

def main():
    print("starting ...")
    GPIO.output(RED_LED, GPIO.HIGH)
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.printout("Starting...")
    client = IoTHubDeviceClient.create_from_connection_string(
        CONNECTION_STRING)
    print("Waiting for messages. Press Ctrl-C to exit")

    try:
        client.on_message_received = message_handler
        client.connect()
        time.sleep(2)
        lcd.clear()
        lcd.setRGB(255,255,255)
        GPIO.output(RED_LED, GPIO.LOW)
        while True:
            time.sleep(10)
#    except OSError: # improper shutdown... start again
#        main()
    except KeyboardInterrupt:
        print("user stopped service")
    finally:
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.HIGH)
        lcd.clear()
        lcd.setRGB(255, 0, 0)
        lcd.setCursor(0,0)
        lcd.printout("Shutting down")
        print("Shutting down")
        client.shutdown()
        time.sleep(2)
        lcd.clear()
        lcd.setRGB(0,0,0)
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(RED_LED, GPIO.LOW)


if __name__ == '__main__':
    main()
