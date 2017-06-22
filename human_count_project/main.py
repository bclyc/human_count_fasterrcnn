import configLoad
import os
# import crash_on_ipy
import CheckNewImage
import NdetectPerson
import maineval_voc
import time
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import boxTu
import glob
import MySQLdb
import ConfigParser

run = True;

net = maineval_voc.initNet();

source_flag = configLoad.source_flag;
result_flag = configLoad.result_flag;
boundingbox_flag = configLoad.boundingbox_flag
inter_time = 0.0;
clean_time = 0.0;

db = MySQLdb.connect("localhost", "root", "lm2323", "people_c")
cursor = db.cursor()

while run:
    configLoad.load_count_config()
    configLoad.load_cameras()
    configLoad.load_camera_config()
    clean_flag = int(configLoad.globalConfig['count_config']['default']['cleanflag']);

    for camera in configLoad.globalConfig['cameras']:
        # check max number;
        # camera
        if not os.path.exists(camera['config_path'] + 'Device.ini'):
            continue;
        mode_config = ConfigParser.ConfigParser();
        mode_config.read(camera['config_path'] + 'Device.ini');

        camUid = camera['uid'].strip()

        ip = mode_config.get('DEVICE', 'ip')
        ip = ip[0:(len(ip) - 2)].strip()
        port = mode_config.get('DEVICE', 'port')
        port = port[0:(len(port) - 2)].strip()
        username = mode_config.get('DEVICE', 'username')
        username = username[0:(len(username) - 2)].strip()
        password = mode_config.get('DEVICE', 'password')
        password = password[0:(len(password) - 2)].strip()
        channel = mode_config.get('DEVICE', 'channel')
        channel = channel[0:(len(channel) - 2)].strip()

        try:
            sql = "select CAMERA_NAME,IP,PORT,CHANNEL,LOGIN_NAME,PASSWORD from cameras where CAMERA_NAME=%s "
            cursor.execute(sql, [camUid]);
            results = cursor.fetchall();
            if len(results) == 0:
                sql = "insert into cameras (CAMERA_NAME,IP,PORT,CHANNEL,LOGIN_NAME,PASSWORD) values(%s,%s,%s,%s,%s,%s) "
                cursor.execute(sql, [camUid, ip, port, channel, username, password]);
            db.commit();
        except:
            print "Error: unable to fetch data"
            db.rollback();
            continue

        try:
            frames_path = camera['frame_path'];
            CheckNewImage.remove_exceed(frames_path, filter=source_flag,
                                        max_threshold=camera['config']['config']['maxPerserveFrameNumber'],
                                        delete_num=camera['config']['config']['deleteNumberWhenExceed']);
            CheckNewImage.remove_exceed(frames_path, filter=result_flag,
                                        max_threshold=camera['config']['config']['maxPerserveFrameNumber'],
                                        delete_num=camera['config']['config']['deleteNumberWhenExceed']);
            CheckNewImage.remove_exceed(frames_path, filter=boundingbox_flag,
                                        max_threshold=camera['config']['config']['maxPerserveFrameNumber'],
                                        delete_num=camera['config']['config']['deleteNumberWhenExceed']);

            if camera.has_key('savedProgress'):
                oneImage = CheckNewImage.get_last_new_image(frames_path, filter=source_flag,
                                                            saved_progress=camera['savedProgress']);
            else:
                oneImage = CheckNewImage.get_last_new_image(frames_path, filter=source_flag);
            if oneImage == '':
                continue;
            originimage = Image.open(frames_path + '/' + oneImage)
            print 'dealing:' + oneImage
            midImage = maineval_voc.processImage(net, originimage)
            # origin = np.array(originimage, dtype=np.uint8)
            originimage = np.array(originimage, dtype=np.uint8);

            density = maineval_voc.getSoftMaxDensity(midImage);
            area = maineval_voc.getPersonArea(midImage);
            mix = maineval_voc.mixPicutre2(originimage, area, 0, 5);

            # plt.imsave(camera['result_softdensity_path']+'/'+oneImage.replace('.source.','.fcn_sm.'),density)
            # plt.imsave(camera['result_personarea_path']+'/'+oneImage.replace('.source.','.fcn_pa.'),area)

            density = density * 255;
            area[area == 15] = 30;

            # densityImage=Image.open(camera['result_softdensity_path']+'/'+oneImage);
            # areaImage=Image.open(camera['result_personarea_path']+'/'+oneImage);
            # print area.shape;
            # print np.max(area);
            # print density.shape;
            # print np.max(density);
            # frames=NdetectPerson.detectPersons(areaImage=areaImage,densityImage=densityImage);
            frames = NdetectPerson.detectPersons(area=area, cameraconfig=camera, density=density);
        except:
            print "error,detect";
            continue;
        try:
            sql = "update cameras set PEOPLE_COUNT=%s,COUNT_DATETIME=%s where CAMERA_NAME=%s "
            cursor.execute(sql, [len(frames), oneImage[0:15], camUid]);
            db.commit();

            if len(frames) > 0:
                image_with_frame = boxTu.boxTu(mix, frames)
                plt.imsave(camera['result_personarea_path'] + '/' + oneImage.replace(source_flag, result_flag),
                           image_with_frame);

                with open(camera['result_person_box_path'] + '/' + oneImage.replace(source_flag, boundingbox_flag),
                          'w') as fframes:
                    for frame in frames:
                        oneline = '';
                        for fvalue in frame:
                            oneline += str(fvalue) + ' ';
                        fframes.writelines(oneline + '\n');

                print frames;
            elif clean_flag == 1:
                os.remove(frames_path + '/' + oneImage)
            camera['savedProgress'] = oneImage;

            if (time.clock() - clean_time > 600.0 or clean_time == 0.0) and clean_flag == 1:
                for filename in glob.glob(camera['result_person_box_path'] + "/*.src.jpg"):
                    os.remove(filename);
                    # print oneImage;
        except:
            db.rollback();
            print "error,rollback";
            continue;

    if time.clock() - clean_time > 600.0 or clean_time == 0.0:
        clean_time = time.clock();

    configLoad.save_camera_config();
    ninter_time = time.clock()
    sleeptime = float(configLoad.globalConfig['count_config']['default']['interval']);
    if ninter_time - inter_time > sleeptime:
        sleeptime = 0
    else:
        sleeptime = sleeptime - (ninter_time - inter_time);
    inter_time = ninter_time;
    # time.sleep(sleeptime);
    time.sleep(0.5);
    print 'one circle is done.'
