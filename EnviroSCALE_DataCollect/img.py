'''
import pyimgur

#CLIENT_ID = "590fb9c0a0217f7"
CLIENT_ID = "a4bcb5f77bbdb68"
PATH = "image.jpg"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)
'''

import webbrowser
import pyimgur
CLIENT_ID = "a4bcb5f77bbdb68"
CLIENT_SECRET = "13ad6a014e53f23318254054f83ba30c9d54f65f"
# Needed for step 2 and 3
im = pyimgur.Imgur(CLIENT_ID, CLIENT_SECRET)
#auth_url = im.authorization_url('pin')
#webbrowser.open(auth_url)
#pin = raw_input("What is the pin? ")


#im.exchange_pin(pin)
#im.create_album("An authorized album", "Cool stuff!")
#im.refresh_access_token()
# Python 3x
#pin = raw_input("What is the pin? ") # Python 2x


import time

PATH = "image.jpg"
IMAGE_IDS = ["iot123"]
im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)

new_album = im.create_album("AQBox")
time.sleep(2)
#assert not len(new_album.images)
new_album.add_images([uploaded_image.title])
new_album.refresh()
#assert len(new_album.images) == len(IMAGE_IDS)
#new_album.delete()





HOST_ECLIPSE = "iot.eclipse.org"
HOST_IQUEUE = "iqueue.ics.uci.edu"

import paho.mqtt.publish as pub
import traceback

def publish_link_app(value, hostname =  "iot.eclipse.org", event = "photo", device_id="74da382afd91" ):
    try:
        topic = "iotBUET/" + device_id + "/" + event
        pub.single(topic, payload="link", hostname=hostname, port=1883)
        return True
    except:
        print ("error")
        traceback.print_exc()
        return False


