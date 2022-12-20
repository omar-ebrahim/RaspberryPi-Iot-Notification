import time
from azure.iot.device import IoTHubDeviceClient

RECEIVED_MESSAGES = 0

CONNECTION_STRING = "HostName=oe-iot.azure-devices.net;DeviceId=omar-rpi;SharedAccessKey=IH0lOtSxLo/q3hARsr7xPzp5zmeoYG5yBddYFNclxmM="

def message_handler(message):
        global RECEIVED_MESSAGES
        RECEIVED_MESSAGES +=1
        print("message received")
        for property in vars(message).items():
                print("    {}".format(property))

def main():
        print("starting ...")
        client =  IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        print("Waiting for messages. Press Ctrl-C to exit")
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
