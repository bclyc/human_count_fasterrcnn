import cv2
import sys
sys.path.append('../py-faster-rcnn/tools/')
import demo2
net=demo2.initNet()

im = cv2.imread('/home/vrlab/human_count/human_count_project/camera/002/20160906-132947.src.jpg')
frame=demo2.processImage(net,im)


import cv2
import sys
sys.path.append('../py-faster-rcnn/tools/')
import demo2
net=demo2.initNet()

im = cv2.imread('/home/vrlab/human_count/py-faster-rcnn/data/demo/004676.jpg')
frame=demo2.processImage(net,im)