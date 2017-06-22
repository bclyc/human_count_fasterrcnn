#coding=utf-8
from matplotlib import pyplot as plt
from PIL import Image
from Queue import Queue
import numpy as np


#def detectPersons(area=None, density=None, origin=None, areaImage=None,densityImage=None,originImage=None,vanishPoint=-190, rate1=5, bodyRate=2.75,
#                  mainBoxThreshold=5,
#                  maxBoxNumPerImage=200, showResult=0, areaFilter=True, areaFilterThreshold=26):
def detectPersons(area,cameraconfig, density=None, origin=None, areaImage=None,densityImage=None,originImage=None):


    vanishPoint=-300;
    rate1=5;
    bodyRate=2.75;
    mainBoxThreshold=5,
    maxBoxNumPerImage=200
    #showResult=0
    areaFilter=True
    areaFilterThreshold=26

    '''
    ##For Test
    areaImage = Image.open('area.jpg')
    densityImage = Image.open('density.jpg')
    originImage = Image.open('origin.jpg')


    #   areaImage=areaImage.convert('LA');
    #    dir(np);


    areaImage = np.asarray(areaImage, dtype="uint8")
    ROWS = areaImage.shape[0];
    COLUMNS = areaImage.shape[1];

    area = np.zeros([ROWS, COLUMNS]);
    area = areaImage[:, :, 0] * 0.299 + areaImage[:, :, 1] * 0.587 + areaImage[:, :, 2] * 0.114;



    density = np.asarray(densityImage, dtype='uint8')
    if(originImage is None):
        origin = np.asarray(originImage, dtype='uint8')
    '''
    ROWS = area.shape[0];
    COLUMNS = area.shape[1];
    if cameraconfig.has_key('vanishPoint'):
        print "vanish:"+str(cameraconfig['vanishPoint']);
        vanishPoint=int(cameraconfig['vanishPoint']);
    if cameraconfig.has_key('rate1'):
        rate1=int(cameraconfig['rate1']);
    if cameraconfig.has_key('bodyRate'):
        bodyRate=float(cameraconfig['bodyRate']);
    if cameraconfig.has_key('config'):
        if cameraconfig['config'].has_key('config'):
            if cameraconfig['config'].has_key('mainBoxThreshold'):
                mainBoxThreshold=int(camera['config']['config']['mainBoxThreshold']);
                #mainBoxThreshold = int(camera['config']['config']['mainBoxThreshold']);
    if areaFilter:
        area[area < areaFilterThreshold] = 0;
        area[area >= areaFilterThreshold] = 1;

    flag = np.zeros([ROWS, COLUMNS]);
    sum_sp=ROWS*COLUMNS;
    allframes = [];
    toextend_queue = Queue();
    MFLAG = 0;
    SEARCH_DIRECTION = [(0, -1), (1, -1), (1, 0), (0, 1), (1, 1), (-1, -1), (0, -1), (-1, 1)];
    try:
        for i in range(ROWS):
            for j in range(COLUMNS):
                try:
                    if area[i, j] != 1 or flag[i, j] != 0:
                        continue;
                    toextend_queue.put((i, j));
                    LEFT = j;
                    RIGHT = j;
                    TOP = i;
                    BOTTOM = i;
                    MFLAG = MFLAG + 5;

                    ROW_RANGE = (i - vanishPoint) / (rate1 - 1);
                    COLUMN_RANGE = ROW_RANGE / bodyRate;

                    score = 0.0;
                    spount=0;
                    while not toextend_queue.empty() and spount<sum_sp:
                        spount=spount+1;
                        (PointR, PointC) = toextend_queue.get();
                        for (direct_R,direct_C) in SEARCH_DIRECTION:
                            newPoint_R=PointR+direct_R;
                            newPoint_C=PointC+direct_C;
                            if newPoint_R<0 or newPoint_R>=ROWS:
                                continue;
                            if newPoint_C < 0 or newPoint_C >= COLUMNS:
                                continue;
                            if area[newPoint_R,newPoint_C] !=1 or  flag[newPoint_R,newPoint_C] !=0:
                                continue;
                            if (newPoint_R < BOTTOM - ROW_RANGE):
                                continue;
                            if (newPoint_R > TOP + ROW_RANGE):
                                continue;
                            if (newPoint_C < RIGHT - COLUMN_RANGE):
                                continue;
                            if (newPoint_C > LEFT + COLUMN_RANGE):
                                continue;
                            if (newPoint_R < TOP):
                                TOP = newPoint_R;
                            if (newPoint_R > BOTTOM):
                                BOTTOM = newPoint_R;
                            if (newPoint_C < LEFT):
                                LEFT = newPoint_C;
                            if (newPoint_C > RIGHT):
                                RIGHT = newPoint_C;

                            flag[newPoint_R, newPoint_C] = MFLAG;
                            if(density is not None):
                                score+=density[newPoint_R,newPoint_C];
                            else:
                                score += 150*area[newPoint_R, newPoint_C];
                            toextend_queue.put((newPoint_R,newPoint_C));
                    mscore=score/(ROW_RANGE*ROW_RANGE);
                    if score>0:
                        print "mscore:"+str(score);
                    if(mscore>mainBoxThreshold):
                        allframes.append((LEFT,TOP,RIGHT-LEFT,BOTTOM-TOP,mscore));
                        print (LEFT,TOP,RIGHT-LEFT,BOTTOM-TOP,mscore);
                except:
                    print "something is error,but I am too lazy to check.";
                    break;
    except:
        print "something is error too,but I am too lazy to check.";
    #plt.imsave('output.jpg',origin);
    return allframes;
#detectPersons();
