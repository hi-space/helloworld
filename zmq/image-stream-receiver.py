import pyrealsense2 as rs
import numpy as np
import cv2
import zmq, sys
import imagezmq

image_hub = imagezmq.ImageHub(open_port='tcp://119.192.209.246:5555', REQ_REP=False)

while True:
    name, image = image_hub.recv_image()
    cv2.imshow("image", image)
    cv2.waitKey(1)