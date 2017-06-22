#!/usr/bin/env python
# coding: utf-8
import web
import pickle
import os
import string
import configLoad
import ConfigParser
import time
import codecs
import sys
import shutil

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


urls = ("/", "index",
		"/index\.html", "index",
        "/calibration\.html", "calibration",
        "/mainpage\.html", "show_brief_result",
		"/setmode\.html", "setmode",
		"/cam_history\.html", "cam_history",
        "/cam_history_hour\.html", "cam_history_hour",
        "/cam_history_pics\.html", "cam_history_pics",
        "/alert_unhandled\.html", "alert_unhandled",
        "/alert_history\.html", "alert_history",)

render = web.template.render('templates/')
app = web.application(urls, globals())
points = []

class index:
    def GET(self):

        #files = os.listdir("static/camera")
        #print len(files)
        return render.index()

class calibration:
    def GET(self):
        #__init__
        picurl=''
        taskid=''
        name=''
        subpage=0
        mfiles=[]
        width=640
        height=480
        biaodingdir=''

        configLoad.load_cameras()
        configLoad.load_camera_config()
        i = web.input(subpage="0")
        subpage=int(i.subpage)

        if (subpage<0):
            return "error"

        name = []
        output = {}
        if subpage==0:
            for camera in configLoad.globalConfig['cameras']:
                name.append(camera['uid'])
        elif subpage==1:
            i = web.input(taskid="none")
            taskid = i.taskid
            if (taskid != 'none'):
                mCameraConfig=None
                for camera in configLoad.globalConfig['cameras']:
                    if taskid == camera['uid']:
                        mCameraConfig=camera
                        break
                if mCameraConfig is not None:
                    biaodingdir = mCameraConfig['frame_path']
                    files = os.listdir(biaodingdir)
                    mfiles = ['static/'+ biaodingdir + '/' + mfile for mfile in files if configLoad.source_flag in mfile]
                    #print mCameraConfig['config']['config']
                    width=int(mCameraConfig['config']['config']['width'])
                    height = int(mCameraConfig['config']['config']['height'])
        print biaodingdir
        print name
        output['IImagePath'] = mfiles
        output['taskid'] = taskid
        output['name'] = name
        output['subpage'] = subpage
        output['sumpage'] = len(mfiles)
        output['width'] = width
        output['height'] = height
        output['biaodingdir'] = biaodingdir
        #return "hello"
        return render.calibration(output)

    def POST(self):
        i = web.input(action="")
    # if i.action == "postpoints":
    #     i = web.input(action="", points="")
    #     if i.action == "postpoints":
    #         print "1"
    #         arr = i.points.split(',')
    #         for i in range(0, len(arr)):
    #             arr[i] = int(arr[i])
    #         global flag
    #         global points
    #         for i in range(0, len(arr), 2):
    #             if i < len(arr) - 1:
    #                 a = [arr[i], arr[i + 1]]
    #                 points.append(a)
    #         print points
    #         return 'success'
    #     return "failure"
        if i.action == "Calculation":
            i = web.input(action="",configdir='',points="")
            biaodingdir = i.configdir
            print biaodingdir
            arr = i.points.split(',')
            points = [] #points有二维，第一维为人脚底的纵坐标y，第二维为人的高度h
            Num = 0
            vanish = []
            rate = []
            Ratio = []  #people height/width
            while (Num<len(arr)):
                if arr[Num] == '':
                    Num += 1
                    continue
                if arr[Num+1] > arr[Num+3]:
                    y = int(arr[Num+1])
                else:
                    y = int(arr[Num+3])
                h = abs(( int(arr[Num+1]) - int(arr[Num+3]) ))
                points.append([y,h])
                HeiWid = (1.0 * int(arr[Num+3]) - int(arr[Num+1]))/(int(arr[Num+2]) - int(arr[Num]))
                Ratio.append(abs(HeiWid))
                # print Num
                Num += 4
            print points

            for i in range(0,len(points)):
                for j in range(i+1,len(points)):
                    b = (1.0 * points[i][0] * points[j][1] - points[j][0] * points[i][1]) / (points[j][1] - points[i][1])
                    vanish.append(b)
                if points[i][0] - b==0 or points[j][0] - b==0:
                    continue;
                else:
                    c = (1.0 * points[i][1] / (points[i][0] - b) + points[j][1] / (points[j][0] - b)) / 2
                    rate.append(1.0/c)
            # print vanish
            # print rate
            # print Ratio
            for b in vanish:
                if (b == max(vanish)) | (b == min(vanish)):
                    vanish.remove(b)
            for c in rate:
                if(c == max(rate))|(c == min(rate)):
                    rate.remove(c)
            for d in Ratio:
                if(d == max(Ratio))|(d == min(Ratio)):
                    Ratio.remove(d)
            print vanish
            print rate
            print Ratio

            VanishPointDir = biaodingdir + 'config/vanishpoint'
            print VanishPointDir
            f = file(VanishPointDir, "w")
            li = [str(sum(vanish) / len(vanish))+' '+str(sum(rate) / len(rate))+' '+str(sum(Ratio) / len(Ratio))]
            f.writelines(li)
            f.close()

            # m = len(points)
            # print m
            # matrix = []
            # vanish = []
            # rate = []
            # for i in range(0, m, 2):
            #     j = 1
            #     if points[i][j] > points[i + 1][j]:
            #         b = points[i][j] - points[i + 1][j]
            #         c = [points[i][j], b]
            #         matrix.append(c)
            #     else:
            #         b = points[i + 1][j] - points[i][j]
            #         c = [points[i + 1][j], b]
            #         matrix.append(c)
            # p = len(matrix)
            # for i in range(0, p):
            #     for j in range(i + 1, p):
            #         b = (matrix[i][0] * matrix[j][1] - matrix[j][0] * matrix[i][1]) / (matrix[j][1] - matrix[i][1])
            #         vanish.append(b)
            #         c = (matrix[i][1] / (matrix[i][0] - b) + matrix[j][1] / (matrix[j][0] - b)) / 2
            #         rate.append(c)
            # print vanish
            # print rate
            # f = file("data.txt", "w")
            # li = ["Vanishing point = " + str(sum(vanish) / len(vanish)) + "\n",
            #       "Rate of change = " + str(sum(rate) / len(rate)) + "\n"]
            # f.writelines(li)
            # f.close()
            # outstr = str(sum(vanish) / len(vanish)) + "," + str(sum(rate) / len(rate))
            # return outstr


source_flag=configLoad.source_flag;
result_flag=configLoad.result_flag;
boundingbox_flag=configLoad.boundingbox_flag
class show_brief_result:
    def GET(self):
        configLoad.load_count_config();
        configLoad.load_cameras();
        configLoad.load_camera_config();
        configLoad.load_mode_config();

        result_to_show=[];
        cam_without_person=[];
        cam_onalarm=[];
        unhandled_num=0;
        clean_flag=int(configLoad.globalConfig['count_config']['default']['cleanflag']);
        hidenotrunning_flag=int(configLoad.globalConfig['count_config']['default']['hidenotrunningflag']);
	


        for camera in configLoad.globalConfig['cameras']:

            if camera.has_key('savedProgress') and camera['savedProgress'].strip()!='':
                cameradata = {};
                cameradata['uid'] = camera['uid'];
                oneImage = camera['savedProgress'];
                #Cam with people
                if os.path.exists(camera['result_person_box_path']  + oneImage.replace(source_flag,boundingbox_flag)):
                    resimage_path = camera['result_personarea_path']  + oneImage.replace(source_flag,result_flag);
                    cameradata['image'] = resimage_path;

                    frames = [];
                    with open(camera['result_person_box_path']  + oneImage.replace(source_flag,boundingbox_flag)) as fframes:
                        for line in fframes:
                            values = line.split(' ');
                            frames.append((int(values[0]), int(values[1]), int(values[2]), int(values[3]), float(values[4])));
                    cameradata['frames'] = frames;
                    result_to_show.append(cameradata);
                #Cam without people
                elif clean_flag == 0:
                    resimage_path = camera['result_personarea_path']  + oneImage;
                    cameradata['image'] = resimage_path;
                    cam_without_person.append(cameradata);

                #Alert pics
                alertUnhandledFolder = 'camera/Alert/unhandled/';
                files = os.listdir(alertUnhandledFolder);
                for file in files:
                    if camera['uid']+'_'+oneImage.replace(source_flag,result_flag) in file:
                        cameraAlert = {};
                        cameraAlert['uid']=camera['uid'];
                        cameraAlert['path']=alertUnhandledFolder+file;
                        cam_onalarm.append(cameraAlert);
                        break;

                #Unhandled pics number
                unhandled_num=len(files);


        result = [result_to_show, cam_without_person, clean_flag, cam_onalarm, hidenotrunning_flag, unhandled_num];
        return render.mainpage(result);

    def POST(self):
        i = web.input(action="")
        if i.action == "setCleanflag":
            i = web.input(action="",flag='')
            cleanflag = i.flag
	    
            try:
                lines=open("count_config",'r').readlines();
                for index,line in enumerate(lines):
                    print index,line
                if "cleanflag" in lines[index]:
                    lines[index]="cleanflag="+cleanflag+"\n";

                open("count_config",'w').writelines(lines)

            except Exception,e:
                    print e
        elif i.action == "setHidenotrunningflag":
            i = web.input(action="",flag='')
            flag = i.flag
	    
            try:
                lines=open("count_config",'r').readlines();
                for index,line in enumerate(lines):
                    print index,line
                if "hidenotrunningflag" in lines[index]:
                    lines[index]="hidenotrunningflag="+flag+"\n";

                open("count_config",'w').writelines(lines)

            except Exception,e:
                print e

        elif i.action == "alert":
            i = web.input(action="", flag='', pic='')
            flag = i.flag;
            pic=i.pic;

            print i.action,flag,pic;

            try:
                alertTFolder = 'camera/Alert/T/';
                alertFFolder = 'camera/Alert/F/';
                if not os.path.exists(alertTFolder):
                    os.makedirs(alertTFolder);
                if not os.path.exists(alertFFolder):
                    os.makedirs(alertFFolder);
                if flag=='T':
                    if os.path.exists(pic):
                        filenamelist=pic.split('/');
                        filename=filenamelist[len(filenamelist)-1];
                        shutil.move(pic,alertTFolder);
                if flag=='F':
                    if os.path.exists(pic):
                        filenamelist=pic.split('/');
                        filename=filenamelist[len(filenamelist)-1];
                        shutil.move(pic,alertFFolder);


            except Exception, e:
                print e


class setmode:
    def GET(self):
        configLoad.load_cameras();
        configLoad.load_mode_config();
        camera_list=configLoad.globalConfig['cameras'];

        mode_config = ConfigParser.ConfigParser();
        mode_config.read('./mode_config');
        mode_list=[];

        for index,section in enumerate(mode_config.sections()):
            if section!="Default":
                option_list="";
                for option in mode_config.options(section):
                    if option!="runtime" and option!="week":
                        option_list=option_list+option+", ";
                mode_list.append({'mode_name':section,'week':mode_config.get(section,'week'),'run_time':mode_config.get(section,'runtime'),'cameras':option_list});
                print 'mode_name',section,'cameras',option_list;
        data_to_pass=[camera_list,mode_list];
        return render.setmode(data_to_pass);

    def POST(self):
        i = web.input(action="")
        if i.action=="mode_set":
            i = web.input(camera="",plan_name="",run_time="",week="");
            camera=i.camera.encode('utf8');
            camera_id_list=camera.split(',');
            camera_id_list.pop();
            plan_name=i.plan_name;
            plan_name=plan_name.encode('utf8');

            week = i.week;
            week = week.encode('utf8');


            #print "camera_id_list",camera_id_list;
            #print "run_time_list",run_time_list;

            configLoad.load_cameras();
            configLoad.load_mode_config();

            mode_config = ConfigParser.ConfigParser();
            mode_config.read('./mode_config');

            mode_config.add_section(plan_name);
            mode_config.set(plan_name, 'week', i.week);
            mode_config.set(plan_name, 'runtime', i.run_time);
            for camera_id in camera_id_list:
                mode_config.set(plan_name, camera_id, 1);


            print "setmode", plan_name, camera_id, week, i.run_time;

            # with codecs.open('./mode_config', encoding="utf-8-sig" ) as f:
            # mode_config.write(f);
            mode_config.write(codecs.open('./mode_config', 'w', 'utf-8'));

            configLoad.load_cameras();
            configLoad.load_mode_config();
            camera_list = configLoad.globalConfig['cameras'];

            mode_list = [];
            for index, section in enumerate(mode_config.sections()):
                if section != "Default":
                    option_list = "";
                    for option in mode_config.options(section):
                        if option != "runtime" and option != "week":
                            option_list = option_list + option + ", ";
                    mode_list.append({'mode_name': section, 'week': mode_config.get(section, 'week'),
                                      'run_time': mode_config.get(section, 'runtime'), 'cameras': option_list});
                    print 'mode_name', section, 'cameras', option_list;

            data_to_pass = [camera_list, mode_list];
            return render.setmode(data_to_pass);
        if i.action == "mode_delete":
            i = web.input(mode_name="");
            mode_name = i.mode_name;
            print "mode_name", mode_name;
            print isinstance(mode_name, unicode);
            print mode_name.encode('utf8')

            mode_name = mode_name.encode('utf8');
            mode_config = ConfigParser.ConfigParser();
            mode_config.read('./mode_config');

            runtime = mode_config.get(mode_name, 'runtime');
            cameras = mode_config.options(mode_name);



            mode_config.remove_section(mode_name);

            mode_config.write(codecs.open('./mode_config', 'w', 'utf-8'));

            configLoad.load_cameras();
            configLoad.load_mode_config();
            camera_list = configLoad.globalConfig['cameras'];

            mode_list = [];
            for index, section in enumerate(mode_config.sections()):
                if section != "Default":
                    option_list = "";
                    for option in mode_config.options(section):
                        if option != "runtime" and option != "week":
                            option_list = option_list + option + ", ";
                    mode_list.append({'mode_name': section, 'week': mode_config.get(section, 'week'),
                                      'run_time': mode_config.get(section, 'runtime'), 'cameras': option_list});
                    print 'mode_name', section, 'cameras', option_list;

            data_to_pass = [camera_list, mode_list];
            return render.setmode(data_to_pass);


class cam_history:
    def GET(self):
        i = web.input(camuid="");
        camuid = i.camuid;
        configLoad.load_cameras();
        camera_list = configLoad.globalConfig['cameras'];
        theCam={};
        for camera in camera_list:
            if camera['uid']==camuid:
                theCam=camera;
                break;

        camDir=theCam['base_path'];
        hisDir=camDir+ '/history/';


        folders = os.listdir(hisDir);
        folders.sort();
        folders.reverse();


        folder_list=[];
        for folder in folders:
            folderDir=camDir + '/history/'+folder;
            pics=os.listdir(folderDir);
            pics=[x for x in pics if '.jpg' in x];
            pics.sort();
            print folderDir,": ",len(pics),"pics";
            folder_list.append([folderDir,pics,camuid]);

        return render.cam_history(folder_list);

class cam_history_hour:
    def GET(self):
        i = web.input(camuid="",date="");
        camuid = i.camuid;
        date = i.date;
        configLoad.load_cameras();
        camera_list = configLoad.globalConfig['cameras'];
        theCam={};
        for camera in camera_list:
            if camera['uid']==camuid:
                theCam=camera;
                break;

        camDir=theCam['base_path'];
        hisDir=camDir+ '/history/';


        folder_list=[];

        folderDir=hisDir+date;
        pics=os.listdir(folderDir);
        pics=[x for x in pics if '.jpg' in x];
        pics.sort();

        hourList=[];
        for i in range(0,23):
            hourList.append([]);
            hour=str(i);
            hour=hour.zfill(2);
            for pic in pics :
                if hour == pic[9:11]:
                    hourList[i].append(pic);

        print folderDir,": ",len(pics),"pics";

        folder_list.append([folderDir,hourList,camuid]);

        return render.cam_history_hour(folder_list);


class cam_history_pics:
    def GET(self):
        i = web.input(camuid="",date="",hour="");
        camuid = i.camuid;
        date = i.date;
        hour = i.hour;
        configLoad.load_cameras();
        camera_list = configLoad.globalConfig['cameras'];
        theCam={};
        for camera in camera_list:
            if camera['uid']==camuid:
                theCam=camera;
                break;

        camDir=theCam['base_path'];
        hisDir=camDir+ '/history/';


        folder_list=[];

        folderDir=hisDir+date;
        pics=os.listdir(folderDir);
        pics=[x for x in pics if '.jpg' in x];
        pics.sort();

        picList=[];
        hour = str(hour);
        hour = hour.zfill(2);
        for pic in pics:
            if hour == pic[9:11]:
                picList.append(pic);

        print folderDir,": ",len(pics),"pics";

        folder_list.append([folderDir,picList,camuid]);

        return render.cam_history_pics(folder_list);


class alert_unhandled:
    def GET(self):
        try:
            alertUnhandledFolder = 'camera/Alert/unhandled/';
            if not os.path.exists(alertUnhandledFolder):
                os.makedirs(alertUnhandledFolder);
            files = os.listdir(alertUnhandledFolder);

            alert_pics=[];
            for file in files:
                alert_pic={};
                alert_pic['uid'] = file.split('_')[0];
                alert_pic['date'] = file.split('_')[1].split('.')[0];
                alert_pic['path'] = alertUnhandledFolder+file;
                alert_pics.append(alert_pic);

            def comp(x,y):
                if x['date']<y['date']:
                    return 1;
                elif x['date']>y['date']:
                    return -1;
                else:
                    return 0;

            alert_pics.sort(comp);

            return render.alert_unhandled(alert_pics);

        except Exception, e:
            print e


class alert_history:
    def GET(self):
        try:
            alertTFolder = 'camera/Alert/T/';
            alertFFolder = 'camera/Alert/F/';
            if not os.path.exists(alertTFolder):
                os.makedirs(alertTFolder);
            if not os.path.exists(alertFFolder):
                os.makedirs(alertFFolder);
            filesT = os.listdir(alertTFolder);
            filesF = os.listdir(alertFFolder);

            alert_picsT=[];
            for file in filesT:
                alert_pic={};
                alert_pic['uid'] = file.split('_')[0];
                alert_pic['date'] = file.split('_')[1].split('.')[0];
                alert_pic['path'] = alertTFolder+file;
                alert_picsT.append(alert_pic);
            alert_picsF = [];
            for file in filesF:
                alert_pic = {};
                alert_pic['uid'] = file.split('_')[0];
                alert_pic['date'] = file.split('_')[1].split('.')[0];
                alert_pic['path'] = alertFFolder + file;
                alert_picsF.append(alert_pic);

            def comp(x,y):
                if x['date']<y['date']:
                    return 1;
                elif x['date']>y['date']:
                    return -1;
                else:
                    return 0;

            alert_picsT.sort(comp);
            alert_picsF.sort(comp);

            alert_pics = [alert_picsT,alert_picsF];

            return render.alert_history(alert_pics);

        except Exception, e:
            print e


if __name__ == "__main__":
    app.run()
