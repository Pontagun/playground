import paho.mqtt.client as mqtt
import struct
import json
import math


def byte_to_float(line):
    data = [int(line[0:2], 16),
            int(line[2:4], 16),
            int(line[4:6], 16),
            int(line[6:8], 16)]
    return struct.unpack('f', bytearray(data)) # This return tuple.


def byte_to_float(line):
    data = [int(line[0:2], 16),
            int(line[2:4], 16),
            int(line[4:6], 16),
            int(line[6:8], 16)]
    return struct.unpack('f', bytearray(data)) # This return tuple.
# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    sensor = json.loads(msg.payload.decode())
    x = byte_to_float(sensor["x"])
    y = byte_to_float(sensor["y"])
    z = byte_to_float(sensor["z"])
    w = byte_to_float(sensor["w"])
    print(math.sqrt((x[0] ** 2) + (y[0] ** 2) + (z[0] ** 2) + (w[0] ** 2)))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.137.1", 50001, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
