from ctypes import *

so_file = "./my-robot.a"

darknet = CDLL(so_file)

net_init = darknet.myrobot_init_detection("cfg/coco.data", "cfg/yolov3-tiny.cfg", "yolov3-tiny.weights")
darknet.myrobot_detection(net_init, "./mypic.jpg", 0.5, 0.5);
darknet.myrobot_clean_detection(res_init);