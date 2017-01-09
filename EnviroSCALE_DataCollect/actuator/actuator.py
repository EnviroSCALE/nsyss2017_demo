import paho.mqtt.publish as pub
from socket import *
from time import sleep
import json

def publish(message):
    try:
        msgs = [{'topic': "paho/test/iotBUET/piCONTROL/", 'payload': message},
                ("paho/test/multiple", "multiple 2", 0, False)]
        pub.multiple(msgs, hostname="iot.eclipse.org")
        return True

    except gaierror:
        print ("[MQTT] Publish ERROR." )
        return False

def make_control_json(poweroff, sampling, camera):
    #json_string = '{"power_off": "N", "sampling_rate":"20", "sampling_rate":"20"}'
    d = {
        'power_off': poweroff,
        'sampling_rate': sampling,
        'camera' : camera
        #'tuple': ['abc', '123'],
    }
    jsonstr = json.dumps(d)
    #print(jsonstr)
    return jsonstr
#
# count = 0
# while True:
#     try:
#         count = count + 1
#         json_string = make_control_json("N", count, "N")
#         publish(json_string)
#         print(json_string)
#         sleep(2)
#     except KeyboardInterrupt:
#         break
#
count = 0
while True:
    try:
        count = 10
        json_string = make_control_json("Y", count, "N")
        publish(json_string)
        print(json_string)
        sleep(5)
        break
    except KeyboardInterrupt:
        break
