#!/usr/bin/python
import os
import json
import requests
import timeit
import time
#import datetime
from datetime import datetime
import rospy
import socket
import commands
import string
from threading import Thread
from  robot_msgs.msg import panoramicCapture
from  vr_msgs.msg import PanoramaStatus, ControllerCommand
import ConfigParser
import osc

__major_version__ = '1'
__minor_version__ = '0'
__change_version__ = '0'
__version__ = '.'.join((__major_version__,
                        __minor_version__,
                        __change_version__))

def panoStatus(status):
    global commandPub, capturePub, cnt
    if status.status == 15:
        cmd = ControllerCommand()
        cmd.command = "save-panorama/" + format(cnt - 1, '08d')
        time.sleep(1)
        commandPub.publish(cmd)
    if status.status == 2:
        cap = panoramicCapture()
        cap.requestedPrefix =  g_output_file + format(cnt, '08d') + "/test-"
        cnt = cnt + 1
        print(cap)
        capturePub.publish(cap)


if __name__ == '__main__':
    global commandPub, capturePub
    global cnt
    global g_output_file
    g_output_file = '/home/aibee/data/new-neck-test/' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '/'
    print('save file in ', g_output_file)
    cnt = 0

    rospy.init_node('new_neck_unit_test', anonymous=True)
    rospy.Subscriber("/panoramicStatus", PanoramaStatus, panoStatus, queue_size=10)
    commandPub = rospy.Publisher('/command', ControllerCommand, queue_size=10)
    capturePub = rospy.Publisher('/panoramicCapture', panoramicCapture, queue_size=1)

    print("new neck test start...")

#    rospy.spinonce()
    cap = panoramicCapture()
    cap.requestedPrefix = "/home/aibee/data/new-neck-test/" + format(cnt, '08d') + "/test-"
    print(cap.requestedPrefix)
    print(cap)
    print(capturePub)
    cnt = cnt + 1
    capturePub.publish(cap)
    print("pub...")


    rospy.spin()
