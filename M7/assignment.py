import random
import time
from sense_hat import SenseHat

sense = SenseHat()

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=eduhub.azure-devices.net;DeviceId=eduPi;SharedAccessKey=UzxPLCDYYIorfE3gxMQqUZF+3oHgnvsBV089lDtMfMc="

# Define the JSON message to send to IoT Hub.
TEMPERATURE = sense.get_temperature()
HUMIDITY = sense.get_humidity()
PRESSURE = sense.get_pressure()

MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}, "pressure" : {pressure}}}'

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            # Build the message with simulated telemetry values.
            temperature = sense.get_temperature()
            humidity = sense.get_humidity()
            pressure = sense.get_pressure()
            temperature = round(temperature,2)
            humidity = round(humidity,2)
            pressure = round(pressure,2)
            #temperature = (temperature * 1.8)+32  #convert to farenheit
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity, pressure=pressure)
            message = Message(msg_txt_formatted)

            # Add a custom application property to the message.
            # An IoT hub can filter on these properties without access to the message body.
            if temperature > 30:
              message.custom_properties["temperatureAlertHigh"] = "true"
              message.custom_properties["temparatureAlertLow"] = "false"
            elif temparature < 25:
              message.custom_properties["temparatureAlertHigh"] = "false"
              message.custom_properties["temparatureAlertLow"] = "true"
            else:
              message.custom_properties["temperatureAlertHigh"] = "false"
              message.custom_properties["temparatureAlertLow"] = "false"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(15)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()