import ConfigParser
import string
import os
globalConfig = {}
source_flag='.src.jpg';
result_flag='.rs.jpg';
boundingbox_flag='.bbox.txt';

def load_count_config():
    globalConfig['count_config'] = {};
    globalConfig['count_config']['default']={};
    globalConfig['count_config']['default']['interval']='2';
    globalConfig['count_config']['default']['cleanflag']='0';
    globalConfig['count_config']['default']['hidenotrunningflag']='0';
    if os.path.exists('./count_config'):
        count_config = ConfigParser.ConfigParser()
        count_config.read('./count_config')
        for section in count_config.sections():
            if not globalConfig['count_config'].has_key(section):
                globalConfig['count_config'][section] = {};
            for option in count_config.options(section):
                globalConfig['count_config'][section][option] = count_config.get(section, option);
		
def load_cameras():
    globalConfig['cameras'] = [];
    camera_dirs=os.listdir('camera');
    for camera_dir in camera_dirs:
        if os.path.isdir('camera/'+camera_dir) and camera_dir!="Alert" and camera_dir!="Test":
            cameramm = {'uid': camera_dir,
                         'base_path': 'camera/'+camera_dir+'/',
                         'config_path': 'camera/'+camera_dir+'/'+'config/',
                         'frame_path': 'camera/'+camera_dir+'/',
                         'result_softdensity_path': 'camera/'+camera_dir+'/',
                         'result_personarea_path': 'camera/'+camera_dir+'/',
                         'result_person_path': 'camera/'+camera_dir+'/',
                         'result_person_box_path':'camera/'+camera_dir+'/',
			 'run_time':'0000-2359'};
            globalConfig['cameras'].append(cameramm);


def load_camera_config():
    for camera in globalConfig['cameras']:
        configPath = camera['config_path'];

        camera['config'] = {};
        camera['config']['config']={};
        camera['config']['config']['mainBoxThreshold']='5';
        camera['config']['config']['maxBoxNumPerImage']='200';
        camera['config']['config']['showResult']='0';
        camera['config']['config']['areaFilter']='True';
        camera['config']['config']['areaFilterThreshold']='26';
        camera['config']['config']['width']=640;
        camera['config']['config']['height']=480;


        camera['config']['config']['deleteNumberWhenExceed']=1500;
        camera['config']['config']['maxPerserveFrameNumber']=500;
        if os.path.exists(configPath+'baseconfig'):
            #Base config
            baseconfig = ConfigParser.ConfigParser()
            baseconfig.read(configPath+'baseconfig')

            for section in baseconfig.sections():
                if not camera['config'].has_key(section):
                    camera['config'][section] = {};
                for option in baseconfig.options(section):
                    camera['config'][section][option] = baseconfig.get(section, option);

        if os.path.exists(configPath+'vanishpoint'):
            #vanishpoint config
            with open(configPath+'vanishpoint') as vf:
                data=vf.readline().split(' ');
                camera['vanishPoint']=string.atof(data[0].strip());
                camera['rate1']=string.atof(data[1].strip());
                camera['bodyRate']=string.atof(data[2].strip());

        if os.path.exists(configPath+'savedprocess'):
            #savedProgress config
            with open(configPath+'savedprocess') as vf:
                data=vf.readline();
                camera['savedProgress']=data;


def save_camera_config():
    for camera in globalConfig['cameras']:
        configPath = camera['config_path'];
        if camera.has_key('savedProgress'):
            if not os.path.exists(configPath):
                try:
                    os.mkdir(configPath);
                except:
                    pass
            if os.path.exists(configPath):
                #savedProgress config
                with open(configPath+'savedprocess','w') as vf:
                    vf.writelines(camera['savedProgress']);
            else:
                print "ERROR,configPath not exists!";

def load_mode_config():
	for index,camera in enumerate(globalConfig['cameras']):
    		cameraId=camera['uid'];
	    	if os.path.exists('./mode_config'):
			mode_config = ConfigParser.ConfigParser();
			mode_config.read('./mode_config');		
			
			if cameraId in mode_config.options('Default'):
				if len(mode_config.get('Default',cameraId))>4:
					globalConfig['cameras'][index]['run_time'] = mode_config.get('Default', cameraId);


#load_cameras();
#load_camera_config();
