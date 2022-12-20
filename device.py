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


def message_handler(message):
    """
    Handles the message from Azure IoT Hub
    """
    lcd.setCursor(0, 0)
    lcd.printout("new message")

    print("message received")
    message_dict = vars(message)
    # It has a b' indicating it's a byte array so can't be parsed as valid JSON
    # so convert it to a string, remove the b' and last single-quote and load it as JSON again
    message_data = str(message_dict["data"])
    message_data = message_data[2:len(message_data)-1]
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


def main():
    print("starting ...")
    print(platform.platform())
    client = IoTHubDeviceClient.create_from_connection_string(
        CONNECTION_STRING)
    print("Waiting for messages. Press Ctrl-C to exit")

    lcd.clear()

    try:
        client.on_message_received = message_handler
        client.connect()
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("user stopped service")
    finally:
        print("Shutting down")
        client.shutdown()


if __name__ == '__main__':
    main()
