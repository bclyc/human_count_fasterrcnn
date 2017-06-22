from PIL import Image
import numpy as np
import framebox
import matplotlib.pyplot as plt

def boxTu(image,frames):
    #image=Image.open('camera/001/001.rs.jpg');
    #image=np.array(image,dtype=np.uint8);
    #frames=[(139,127,28,58,29.3)]
    for frame in frames:
        boundingbox=framebox.boundingbox();
        boundingbox.read(frame);
        image[boundingbox.TOP:boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT,2]= 255;
        image[boundingbox.TOP:boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT+boundingbox.WIDTH,2]= 255;
        image[boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT:boundingbox.LEFT+boundingbox.WIDTH,2]= 255;
        image[boundingbox.TOP,boundingbox.LEFT:boundingbox.LEFT+boundingbox.WIDTH,2]= 255;



        try:
            image[boundingbox.TOP:boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT-1:boundingbox.LEFT+2,2]= 255;
            image[boundingbox.TOP:boundingbox.TOP+boundingbox.HEIGHT,boundingbox.LEFT+boundingbox.WIDTH-1:boundingbox.LEFT+boundingbox.WIDTH+2,2]= 255;
            image[boundingbox.TOP-1:boundingbox.TOP+2,boundingbox.LEFT:boundingbox.LEFT+boundingbox.WIDTH,2]= 255;
            image[boundingbox.TOP+boundingbox.HEIGHT-1:boundingbox.TOP+boundingbox.HEIGHT+2,boundingbox.LEFT:boundingbox.LEFT+boundingbox.WIDTH,2]= 255;

        except:
            pass;




    return image
#plt.imsave('ssa1.jpg',image);



#boxTu(None,None)