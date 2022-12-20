import time
from azure.iot.device import IoTHubDeviceClient
import json
import platform

# These will not work on Windows, so testing must be done on the RPi.
import RPi.GPIO as GPIO
import RGB1602

CONNECTION_STRING = "HostName=oe-iot.azure-devices.net;DeviceId=omar-rpi;SharedAccessKey=IH0lOtSxLo/q3hARsr7xPzp5zmeoYG5yBddYFNclxmM="
NOTIFICATION_KEY = "notification"

lcd = RGB1602.RGB1602(16, 2)
lcd.setRGB(255,0,0)

def message_handler(message):
    """
    Handles the message from Azure IoT Hub
    """
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
                time.sleep(1)
                lcd.scrollLeft()

        time.sleep(5)
#        lcd.clear()
        lcd.setRGB(0,0,0)


def main():
    print("starting ...")
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
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("user stopped service")
    finally:
        lcd.clear()
        lcd.setRGB(255, 0, 0)
        lcd.setCursor(0,0)
        lcd.printout("Shutting down")
        print("Shutting down")
        client.shutdown()
        time.sleep(2)
        lcd.clear()
        lcd.setRGB(0,0,0)


if __name__ == '__main__':
    main()
