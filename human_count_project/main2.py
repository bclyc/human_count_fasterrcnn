#coding=utf-8
import configLoad
import os
import shutil
#import crash_on_ipy
import CheckNewImage
#import NdetectPerson
#import maineval_voc
import time
import matplotlib.pyplot as plt
import traceback
from PIL import Image,ImageDraw,ImageFont

print('beginToimport')

import numpy as np
import boxTu
import glob
print('mysqldb')
import MySQLdb
print('configParser')
import ConfigParser
print('endConfigParser')
import cv2
print('endCv2')
import sys
sys.path.append('../py-faster-rcnn/tools/')
print('beginToimport demo2')
import demo2
print('begintoInitNet');
net=demo2.initNet()
print('endInitNet')


run=True;
serverId = "725"
#net=maineval_voc.initNet();

source_flag='.src.jpg';
result_flag='.rs.jpg';
boundingbox_flag='.bbox.txt'
inter_time=0.0;
clean_time=0.0;

db = MySQLdb.connect("192.168.100.241","root","ItiG4LDStbPPhZSXwTJG","people_c",unix_socket="/tmp/mysql.sock");
cursor = db.cursor();

#self-adaption counter
#configLoad.load_cameras();
#cameraNum = len(configLoad.globalConfig['cameras']);
counterProcessed=[];
counterWithP=[];
picSaveMode=[];
picSaveCount=[];

sql0 = "select cameraId,serverType from va_system_server where id=%s and serverType=1 "
cursor.execute(sql0,[serverId]);
results = cursor.fetchall();
cameras = []   
cameraNum = 0
try:
    if len(results)==0:
        print "No server type IA named",serverId        
    else:
        cameras = results[0][0].split(',')
        cameraNum = len(cameras)
except MySQLdb.Error, e:
        print "MySQL Error:%s" % str(e)
        db.rollback();

for i in range(0,cameraNum):
    counterProcessed.append(0);
    counterWithP.append(0);
    picSaveMode.append(0);
    picSaveCount.append(0);    

while run:
    #configLoad.load_count_config();
    #configLoad.load_cameras();
    #configLoad.load_camera_config();
    #clean_flag=int(configLoad.globalConfig['count_config']['default']['cleanflag']);
    
    #get alarm modes
    sql1 = "select modeId,modeName,modeWeek,modeTime,modeCameras,modeFlag from ia_imageanalysis_schedule where modeFlag=1 "
    cursor.execute(sql1,[]);
    results1 = cursor.fetchall();
    modes = results1    

    for camIndex,camera in enumerate(cameras):
        #check max number;
        #camera
#         if not os.path.exists(camera['config_path']+'Device.ini'):
#             continue;
#         mode_config = ConfigParser.ConfigParser();
#         mode_config.read(camera['config_path']+'Device.ini');

#         camUid=camera['uid'].strip();
# 
#         ip=mode_config.get('DEVICE','ip');
#         ip=ip[0:(len(ip)-2)].strip();
#         port=mode_config.get('DEVICE','port');
#         port=port[0:(len(port)-2)].strip();
#         username=mode_config.get('DEVICE','username');
#         username=username[0:(len(username)-2)].strip();
#         password=mode_config.get('DEVICE','password');
#         password=password[0:(len(password)-2)].strip();
#         channel=mode_config.get('DEVICE','channel');
#         channel=channel[0:(len(channel)-2)].strip();
# 
#         try:
#             sql = "select cameraId,cameraIp,cameraPort,cameraChannel,cameraLoginName,cameraLoginPassword from camera where cameraId=%s "
#             cursor.execute(sql,[camUid]);
#             results = cursor.fetchall();
#             if len(results)==0 :
#                 sql = "select ID from cameras order by ID DESC";
#                 cursor.execute(sql);
#                 results = cursor.fetchall();
#                 if len(results)>0:
#                     dbcamid=results[0][0]+1;
#                 else:
#                     dbcamid=100000;
# 
#                 sql = "insert into cameras (CAMERA_NAME,IP,PORT,CHANNEL,LOGIN_NAME,PASSWORD,ID,ID2,ALERT_COUNT) values(%s,%s,%s,%s,%s,%s,%s,%s,%s) "
#                 cursor.execute(sql,[camUid,ip,port,channel,username,password,dbcamid,"0","0"]);
#                 db.commit();
#         except MySQLdb.Error, e:
#             print "MySQL Error:%s" % str(e)
#             db.rollback();


        try:
#             frames_path=camera['frame_path'];
#             CheckNewImage.remove_exceed(frames_path,filter=source_flag,max_threshold=camera['config']['config']['maxPerserveFrameNumber'],delete_num=camera['config']['config']['deleteNumberWhenExceed']);
#             CheckNewImage.remove_exceed(frames_path,filter=result_flag,max_threshold=camera['config']['config']['maxPerserveFrameNumber'],delete_num=camera['config']['config']['deleteNumberWhenExceed']);
#             CheckNewImage.remove_exceed(frames_path,filter=boundingbox_flag,max_threshold=camera['config']['config']['maxPerserveFrameNumber'],delete_num=camera['config']['config']['deleteNumberWhenExceed']);

            frames_path = os.path.join('camera', camera)
            oneImage=CheckNewImage.get_last_new_image(frames_path,filter=source_flag);
            if oneImage=='':
                continue;

            #print 'dealing:' + oneImage

            #midImage=maineval_voc.processImage(net,originimage)
            #origin = np.array(originimage, dtype=np.uint8)
            #originimage=np.array(originimage, dtype=np.uint8);

            #density=maineval_voc.getSoftMaxDensity(midImage);
            #area=maineval_voc.getPersonArea(midImage);
            #mix=maineval_voc.mixPicutre2(originimage,area,0,5);
            imagename_with_path=frames_path + '/' + oneImage;
            #originimage = Image.open()
            im = cv2.imread(imagename_with_path)
            mix = im;
            frames = demo2.processImage(net, im)

            #Save .rs .txt
            if len(frames)>0:
                image_with_frame=boxTu.boxTu(mix,frames);

                font = cv2.cv.InitFont(cv2.cv.CV_C,3, 3, 0, 2, 8);
                cv2.cv.PutText(cv2.cv.fromarray(image_with_frame), str(len(frames))+"people", (30, 40), font, (0, 0, 255))

                cv2.imwrite(imagename_with_path.replace(source_flag,result_flag),image_with_frame);

                with open(imagename_with_path.replace(source_flag,boundingbox_flag),'w') as fframes:
                    for frame in frames:
                        oneline='';
                        for fvalue in frame:
                            oneline+=str(fvalue)+' ';
                        fframes.writelines(oneline+'\n');
            else:
                os.remove(imagename_with_path)

            # Alert or not and save
            alert_flag = 0;
            if len(frames) > 0:
                current_time = time.strftime("%H%M", time.localtime(time.time()));
                current_weekday = time.strftime("%w", time.localtime(time.time()));
                weekCN = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
                current_weekday = weekCN[int(current_weekday)];
                #print "当前时间", current_time;
                #print "当前weekday", current_weekday;
                for mode in modes:
                    try:
                        modeCams=mode[4].split(',')[0:-1]
                        modeWeek=mode[2].split(',')[0:-1]                        
                        if camera in modeCams and current_weekday in modeWeek:
                            modeTime=mode[2].split(',')
                            for time in modeTime:
                                starttime = time[0:4]
                                endtime = time[5:9]
                                if current_time>=starttime and current_time<=endtime:
                                    alert_flag = 1;
                                    break;
                        
                    except:
                        print "mode error:",mode
                        traceback.print_exc()
                    
            if alert_flag == 1:
                print "AlertOn:Camera ",camera['uid'],"person detected";
                alertUnhandledFolder = os.path.join('camera', camera) + '/Alert/unhandled/';
                if not os.path.exists(alertUnhandledFolder):
                    os.makedirs(alertUnhandledFolder);
                #print camera['result_personarea_path'] + '/' + oneImage.replace(source_flag, result_flag);
                if os.path.exists(imagename_with_path.replace(source_flag, result_flag)):
                    shutil.copy(imagename_with_path.replace(source_flag, result_flag),
                                alertUnhandledFolder + '/' + camera + '_' + oneImage.replace(source_flag,
                                                                                                result_flag));
                #save into mysql
                bbox=""
                for frame in frames:
                        for fvalue in frame:
                            bbox += str(fvalue)+'-';
                        bbox = bbox[0:-1]
                        bbox += ','
                bbox = bbox[0:-1]
                sql = "insert into ia_imageanalysis_alarm(cameraId,serverId,imageAnalysisAlarmState,motionAnalysisAlarmTime,motionAnalysisAlarmVpt,addTime)"
                +" value (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql,[camera, serverId, '1', oneImage[0:15], bbox, time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time()))] );
                db.commit();

#                 mode_config = ConfigParser.ConfigParser();
#                 mode_config.read('./mode_config');
# 
#                 for modename in mode_config.sections():
#                     if mode_config.has_option(modename, camera['uid']):
#                         weekday_list = mode_config.get(modename, 'week').split(',');
#                         run_time_list = mode_config.get(modename, 'runtime').split(',');
#                         if current_weekday in weekday_list:
#                             for runtime in run_time_list:
#                                 starttime = runtime[0:4];
#                                 endtime = runtime[5:9];
#                                 if current_time >= starttime and current_time <= endtime:
#                                     alert_flag = 1;
#                                     break;
#                     if alert_flag == 1:
#                         break;

                


            #self-adaption counter
#             saveEveryNPic=0;
#             saveflag=0;
#             counterProcessed[camIndex]=counterProcessed[camIndex]+1;
#             picSaveCount[camIndex]=picSaveCount[camIndex]+1;
#             if len(frames)>0:
#                 counterWithP[camIndex]=counterWithP[camIndex]+1;
# 
#             if picSaveMode[camIndex]==0:
#                 saveEveryNPic = 1;
#             elif picSaveMode[camIndex]==1:
#                 saveEveryNPic = 15;
#             elif picSaveMode[camIndex]==2:
#                 saveEveryNPic = 40;
#             elif picSaveMode[camIndex]==3:
#                 saveEveryNPic = 60;
# 
#             if picSaveCount[camIndex]>=saveEveryNPic:
#                 saveflag=1;
# 
# 
#             if counterProcessed[camIndex]>=60:
#                 if counterWithP[camIndex]<=5:
#                     if picSaveMode[camIndex]!=0:
#                          print "Cam",camUid,"changing savemode from ",picSaveMode[camIndex],"to",0;
#                     picSaveMode[camIndex] = 0;
#                 elif counterWithP[camIndex]>5 and counterWithP[camIndex]<=20:
#                     if picSaveMode[camIndex]!=1:
#                          print "Cam",camUid,"changing savemode from ",picSaveMode[camIndex],"to",1;
#                     picSaveMode[camIndex] = 1;
#                 elif counterWithP[camIndex]>20 and counterWithP[camIndex]<=40:
#                     if picSaveMode[camIndex]!=2:
#                          print "Cam",camUid,"changing savemode from ",picSaveMode[camIndex],"to",2;
#                     picSaveMode[camIndex] = 2;
#                 elif counterWithP[camIndex]>40 and counterWithP[camIndex]<=60:
#                     if picSaveMode[camIndex]!=3:
#                          print "Cam",camUid,"changing savemode from ",picSaveMode[camIndex],"to",3;
#                     picSaveMode[camIndex] = 3;
#                 counterProcessed[camIndex] = 0;
#                 counterWithP[camIndex] = 0;


#             #SQL table update
#             sql = "update cameras set PEOPLE_COUNT=%s,COUNT_DATETIME=%s where CAMERA_NAME=%s "
#             cursor.execute(sql,[len(frames),oneImage[0:15],camUid]);
#             db.commit();
# 
#             #make history folder
#             if not os.path.exists(camera['result_personarea_path']+'/history'):
#                 os.makedirs(camera['result_personarea_path']+'/history')
# 
#             if len(frames) > 0:
# 
#                 # frames;
# 
#                 #save into date folders
#                 if saveflag == 1 or alert_flag == 1:
#                     picSaveCount[camIndex] = 0;
# 
#                     dateString=oneImage[0:8];
#                     dateFolder=camera['result_personarea_path']+'/history/'+dateString;
#                     if not os.path.exists(dateFolder):
#                         os.makedirs(dateFolder)
#                     shutil.copy(camera['result_personarea_path']+'/'+oneImage.replace(source_flag,result_flag), dateFolder+'/'+oneImage.replace(source_flag,result_flag));
#                     shutil.copy(camera['result_personarea_path']+'/'+oneImage.replace(source_flag,boundingbox_flag), dateFolder+'/'+oneImage.replace(source_flag,boundingbox_flag));
# 
#                     folders=os.listdir(camera['result_personarea_path']+'/history/');
#                     folders.sort();
#                     if len(folders) > 15:
#                         for i in range(1):
#                             try:
#                                 shutil.rmtree(camera['result_personarea_path']+'/history/'+ folders[i]);
#                             except:
#                                 pass;
# 
#             elif clean_flag==1:
#                 os.remove(frames_path+'/'+oneImage)
#             camera['savedProgress']=oneImage;
# 
#             if (time.clock()-clean_time>600.0 or clean_time==0.0) and clean_flag==1:
#                 for filename in glob.glob(camera['result_person_box_path']+"/*.src.jpg"):
#                     os.remove(filename);



        except NameError:
            db.rollback();
            print "error,rollback";
            continue;

    if time.clock()-clean_time>600.0 or clean_time==0.0:
        clean_time=time.clock();

    #configLoad.save_camera_config();
    ninter_time=time.clock()
    sleeptime=float(configLoad.globalConfig['count_config']['default']['interval']);
    sleeptime=0.1;
    if ninter_time-inter_time>sleeptime:
        sleeptime=0
    else:
        sleeptime=sleeptime-(ninter_time-inter_time);
    inter_time=ninter_time;
    #sleep time
    time.sleep(0.5);
    print 'one circle is done.'
