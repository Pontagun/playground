# python3.6

import random
import struct
from paho.mqtt import client as mqtt_client
import json
import math

broker = '192.168.137.1'
port = 50001
topic = "sensors"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'


# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        sensor = json.loads(msg.payload.decode())
        x = byte_to_float(sensor["x"])
        y = byte_to_float(sensor["y"])
        z = byte_to_float(sensor["z"])
        w = byte_to_float(sensor["w"])
        print(math.sqrt((x[0] ** 2) + (y[0] ** 2) + (z[0] ** 2) + (w[0] ** 2)))
        # print(x, y, z, w)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


def byte_to_float(line):
    data = [int(line[0:2], 16),
            int(line[2:4], 16),
            int(line[4:6], 16),
            int(line[6:8], 16)]
    return struct.unpack('f', bytearray(data)) # This return tuple.


if __name__ == '__main__':
    run()
