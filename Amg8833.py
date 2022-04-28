import time
import amg8833_i2c
import numpy as np
import cv2
from threading import Timer


class Amg8833:
    def __init__(self, min=5, max=40):
        t0 = time.time()
        self.sensor = None
        self.min = min
        self.max = max
        self.img = None
        self.pix_to_read = 64 # read all 64 pixels
        while (time.time()-t0) < 1:  # wait 1sec for sensor to start
            try:
                # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
                self.sensor = amg8833_i2c.AMG8833(addr=0x69)  # start AMG8833
            except:
                self.sensor = amg8833_i2c.AMG8833(addr=0x68)
            finally:
                pass

        time.sleep(0.1)  # wait for sensor to settle
        if self.sensor == None:
            assert("No AMG8833 Found - Check Your Wiring")

        self.timer = Timer(0.1, self._update)
        self.timer.start()

    def read_img(self):
        status, pixels = self.sensor.read_temp(self.pix_to_read)  # read pixels with status
        if status:  # if error in pixel, re-enter loop and try again
            return None
        np_pixels = np.array(pixels)
        np_pixels = np.clip(np_pixels, self.min, self.max)
        np_pixels = (np_pixels - self.min) / (self.max - self.min)
        np_pixels = np.reshape(np_pixels, (8, 8))
        h = np_pixels * (240 / 255)
        hsv = np.zeros((8, 8, 3))
        hsv[:, :, 0] = h
        hsv[:, :, 1] = 1
        hsv[:, :, 2] = 1
        rgb = cv2.cvtColor((hsv * 255).astype(np.uint8), cv2.COLOR_HSV2RGB)
        return rgb
    
    def read_temp(self):
        return self.sensor.read_thermistor()

    def get_img(self):
        return self.img

    def _update(self):
        self.img = self.read_img()
        self.timer = Timer(0.1, self._update)
        self.timer.start()
    
