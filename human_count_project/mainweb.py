import web
import configLoad
from PIL import Image
render= web.template.render('./')
urls = (
    '/','index'
)
source_flag=configLoad.source_flag;
result_flag=configLoad.result_flag;
boundingbox_flag=configLoad.boundingbox_flag
class index:
    def GET(self):
        configLoad.load_cameras();
        configLoad.load_camera_config();
        result_to_show=[];
        for camera in configLoad.globalConfig['cameras']:
            frames_path=camera['frame_path'];

            if camera.has_key('savedProgress'):
                cameradata={};
                cameradata['uid']=camera['uid'];
                oneImage=camera['savedProgress'];
                resimage_path=camera['result_personarea_path']+'/'+oneImage.replace(source_flag,result_flag);
                #resimage = Image.open(camera['result_personarea_path']+'/'+oneImage.replace(source_flag,result_flag))
                cameradata['image']=resimage_path;
                frames=[];
                with open(camera['result_person_box_path']+'/'+oneImage.replace(source_flag,boundingbox_flag)) as fframes:
                    for line in fframes:
                        values=line.split(' ');
                        frames.append((int(values[0]),int(values[1]),int(values[2]),int(values[3]),float(values[4])));
                cameradata['frames']=frames;
                result_to_show.append(cameradata);
        return render.mainpage(result_to_show);


if __name__=='__main__':
    app=web.application(urls,globals());
    app.run();