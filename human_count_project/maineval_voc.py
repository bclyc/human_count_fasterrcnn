#%matplotlib inline

caffe_python_path='fcn/caffe/python'
fcn_prototxt='fcn/deploy.prototxt'
fcn_model='fcn/fcn8s-heavy-pascal.caffemodel'




#Caffe Path
import sys
if caffe_python_path!='':
	sys.path.append(caffe_python_path);

import numpy as np
from PIL import Image
import os
import matplotlib
import matplotlib.pyplot as plt
import caffe

matplotlib.rcParams['figure.figsize']=(20.0,20.0)



def initNet(mode='gpu'):
	if mode=='cpu':
		caffe.set_mode_cpu();
	else:
		caffe.set_device(0);
		caffe.set_mode_gpu();
	# load net
	return caffe.Net(fcn_prototxt, fcn_model, caffe.TEST)

def processImage(net,im):
	#im = Image.open("/home/user/liuhao/liuhao/data/mall_dataset/frames/seq_%06d.jpg" % (2))
	#im = Image.open(imagePath)
	#im = Image.open('/home/user/liuhao/liuhao/data/PASCAL_VOL2010/VOC2010/JPEGImages/2007_000129.jpg')
	#im = Image.open('/home/user/liuhao/liuhao/data/mall_dataset/frames/seq_000003.jpg')
	
	in_ = np.array(im, dtype=np.float32)
	in_ = in_[:,:,::-1]
	in_ -= np.array((104.00698793,116.66876762,122.67891434))
	in_ = in_.transpose((2,0,1))

	# shape for input (data blob is N x C x H x W), set data
	net.blobs['data'].reshape(1, *in_.shape)
	net.blobs['data'].data[...] = in_
	# run net and take argmax for prediction
	net.forward()
	out = net.blobs['score'].data[0]
	return out;

def getArea(prs):
	return prs.argmax(axis=0);

def getPersonArea(prs):
	pparea=prs.argmax(axis=0);
	pparea[pparea!=15]=0
	return pparea;

def getDensity(prs):
	return prs[15,:,:]

def getSoftMaxDensity(prs):
	pexp=np.exp(prs[:,:,:])
	rate=pexp[15,:,:]/np.sum(pexp,axis=0)
	return rate

def mixPicutre1(pic1,pic2,mix1,mix2):
	immix=pic1*mix1+pic2*mix2
	immix[immix>255]=255
	immix=np.uint8(immix)
	plt.imshow(immix)
	return immix

def mixPicutre2(pic1,pic2,axis,mix2):
	pic1=np.uint32(pic1);
	pic1[:,:,axis]=pic1[:,:,axis]+pic2*mix2
	pic1[pic1>255]=255;
	pic1=np.uint8(pic1);
	return pic1;	
