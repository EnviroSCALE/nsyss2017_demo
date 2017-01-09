import time
import picamera


def take_picture(pic_name, delay=0):
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(delay)
        camera.capture(pic_name)
        camera.stop_preview()

pic_location = '/home/pi/workshop/camera/image.jpg'
take_picture(pic_location)
