import traceback
from Tkinter import *
import Queue
import threading
import time
import paho.mqtt.client as mqtt
from struct import *
from collections import namedtuple
import sqlite_db
import plotly_connect

#for web-Dashboard
import requests
dweetIO = "https://dweet.io/dweet/for/"
myThingName = "iotEnviroSCALE_BUET"
#myKey = "RaspberryPi2_core_temp"

queue = Queue.Queue()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("paho/test/iotBUET/#")
    client.subscribe("paho/test/iotBUET/bulk_raw/")

#####
##We have different data compaction technique -> this follows technique1=>struct.pack
#####
def on_message(client, userdata, msg):
    try:
        # print("From topic: "+msg.topic+" , received: "+str(unpack('fffffffff', msg.payload)))
        iotBundle = namedtuple('Received', 'time ch4 lpg co2 dust temp humidity lat long cng')
        bb = iotBundle._make(unpack('ifffffffff', msg.payload))
        plotly_connect.draw_to_plotly(bb)
        #time = bb[0]
        #print(time)
        # ch4 = bb[1]
        # lpg = bb[2]
        # co2 = bb[3]
        # dust = bb[4]
        # temp = bb[5]
        # humidity = bb[6]
        # lat = bb[7]
        # long = bb[8]

        tuple = HashedValue("time", bb[0])
        queue.put(tuple)
        tuple = HashedValue("methane", bb[1])
        queue.put(tuple)
        tuple = HashedValue("lpg", bb[2])
        queue.put(tuple)
        tuple = HashedValue("co2", bb[3])
        queue.put(tuple)
        tuple = HashedValue("dust", bb[4])
        queue.put(tuple)
        tuple = HashedValue("temp", bb[5])
        queue.put(tuple)
        tuple = HashedValue("hum", bb[6])
        queue.put(tuple)
        tuple = HashedValue("lat", bb[7])
        queue.put(tuple)
        tuple = HashedValue("long", bb[8])
        queue.put(tuple)
        sqlite_db.insert_in_db(bb[0], bb[1], bb[2], bb[3], bb[4], bb[5], bb[6], bb[7], bb[8])
        print(bb)

        # for web-Dashboard
        rqsString = dweetIO + myThingName + '?' + 'Time' + '= ' + str(bb[0]) + '& CH4' + '= ' + "{0:.2f}".format(
            bb[1]) + '& LPG' + '= ' + "{0:.2f}".format(bb[2]) + '& CO2' + '= ' + "{0:.2f}".format(
            bb[3]) + '& Dust' + '= ' + "{0:.2f}".format(bb[4]) + '& Temparature' + '= ' + "{0:.2f}".format(
            bb[5]) + '& Humidity' + '= ' + str(bb[6]) + '& Lat' + '= ' + str(bb[7]) + '& Long' + '= ' + str(bb[8])
        rqs = requests.get(rqsString)
        print(rqsString)

    except:
        traceback.print_exc()
        print("From topic: " + msg.topic + " INVALID DATA")

        tuple = HashedValue("time", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("methane", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("lpg", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("co2", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("dust", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("temp", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("hum", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("lat", "INVALID")
        queue.put(tuple)
        tuple = HashedValue("long", "INVALID")
        queue.put(tuple)
        


class HashedValue:
    def __init__(self, key, value):
        self.key = key
        self. value = value

class Dashboard:
    def __init__(self, master, queue, end_command):
        self.queue = queue
        self.master = master
        master.title("Dashboard")

        self.label = Label(master, text="Live readings from PI")
        self.dummy_label1 = Label(master, text=" ")
        self.dummy_label2 = Label(master, text=" ")
        self.dummy_label3 = Label(master, text=" ")
        self.dummy_label4 = Label(master, text=" ")
        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.close_button = Button(master, text="Close", command=end_command)

        self.temp_label = Label(master, text=' Temparature         ',)
        self.temp_entry = Label(master, text = "reading...", relief = "sunken")

        self.humidity_label = Label(master, text='       Humidity      ')
        self.hum_entry = Label(master, text = "reading..." , relief = "sunken")

        self.longitude_label = Label(master, text="       Longitude      ")
        self.longitude_entry = Label(master, text = "reading...", relief = "sunken")

        self.lat_label = Label(master, text = "       Lattitude       ")
        self.lat_entry = Label(master, text = "reading...", relief = "sunken")

        self.dust_label = Label(master, text = "       Dust value      ")
        self.dust_entry = Label(master, text = "reading...", relief = "sunken")

        self.methane_label = Label(master, text = "        Methane        ")
        self.methane_text = Label(master, text = "reading...", relief = "sunken")

        self.time_label = Label(master, text = "        Timestamp        ")
        self.time_text = Label(master, text = "reading...", relief = "sunken")

        self.lpg_label = Label(master, text = "        LPG value        ")
        self.lpg_text = Label(master, text = "reading...", relief = "sunken")

        self.co2_label = Label(master, text = "            CO2            ")
        self.co2_text = Label(master, text = "reading...", relief = "sunken")

        # alignments
        self.label.grid(row = 0, column = 4, sticky=W)
        self.dummy_label1.grid(row = 1)
        self.dummy_label2.grid(row = 2)
        self.temp_label.grid(row=3)
        self.humidity_label.grid(row=3, column=1)
        self.lat_label.grid(row = 3, column = 2)
        self.longitude_label.grid(row=3, column=3)
        self.dust_label.grid(row=3, column=4)
        self.lpg_label.grid(row = 3, column = 5)
        self.co2_label.grid(row=3, column=6)
        self.methane_label.grid(row=3, column=7)
        self.time_label.grid(row=3, column=8)
        self.temp_entry.grid(row=4)
        self.hum_entry.grid(row=4,column=1)
        self.lat_entry.grid(row=4, column=2)
        self.longitude_entry.grid(row=4, column=3)
        self.dust_entry.grid(row=4, column=4)
        self.lpg_text.grid(row=4, column=5)
        self.co2_text.grid(row=4, column=6)
        self.methane_text.grid(row=4, column=7)
        self.time_text.grid(row=4, column=8)
        self.dummy_label3.grid(row = 5, column = 1)
        self.dummy_label4.grid(row = 6, column = 1)

        #self.greet_button.grid(row=5)
        self.close_button.grid(row=7, column=8)

    def greet(self):
        print("Greetings!")

    def update_values(self):
        while self.queue.qsize() > 0:
            try:
                y = self.queue.get(0)
                if y.key == "long":
                    self.longitude_entry.__setitem__("text", y.value)
                elif y.key == "lat":
                    self.lat_entry.__setitem__("text", y.value)
                elif y.key == "temp":
                    self.temp_entry.__setitem__("text", y.value)
                elif y.key == "hum":
                    self.hum_entry.__setitem__("text", y.value)
                elif y.key == "dust":
                    self.dust_entry.__setitem__("text", y.value)
                elif y.key == "time":
                    self.time_text.__setitem__("text", y.value)
                elif y.key == "lpg":
                    self.lpg_text.__setitem__("text", y.value)
                elif y.key == "co2":
                    self.co2_text.__setitem__("text", y.value)
                elif y.key == "methane":
                    self.methane_text.__setitem__("text", y.value)
                else:
                    pass
            except Queue.Empty:
                break

class ThreadedClient:
    def __init__(self, master, queue):
        self.master = master
        self.queue = queue
        self.gui = Dashboard(master, self.queue, self.end_application)

        # mqtt client set up
        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("iot.eclipse.org", 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        # end client set up

        self.running = 1
        self.client_thread = threading.Thread(target = self.client.loop_start)
        self.client_thread.start()
        self.periodic_call()
        #self.client.loop_forever()

    def periodic_call(self):
        self.gui.update_values()
        if not self.running:
            self.master.destroy()
            self.client.loop_stop(True)
            import sys
            sys.exit(0)
        self.master.after(1, self.periodic_call)

    def end_application(self):
        self.running = 0

root = Tk()
client = ThreadedClient(root, queue)
root.mainloop()
