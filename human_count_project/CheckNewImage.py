import os
BaseDIR="";
def compareFileWithChangeTime(x,y):
    stat_x = os.stat(BaseDIR+"/"+x);
    stat_y = os.stat(BaseDIR+"/"+y);
    if stat_x.st_ctime<stat_y.st_ctime:
        return -1;
    elif stat_x.st_ctime>stat_y.st_ctime:
        return 1;
    else:
        return 0;
def getSortedFiles(directory, filter='.source.' ):

    files = os.listdir(directory);
    global BaseDIR;
    BaseDIR=directory;
    files=[x for x in files if filter in x];
   # files.sort(compareFileWithChangeTime);
    files.sort();
    return files;
def get_constant_new_image(directory, filter='.source.' ,saved_progress=None):
    files = getSortedFiles(directory,filter);
    returned_filename = '';
    if len(files) > 0:
        if saved_progress is None and len(files) > 0:
            returned_filename = files[0];
        else:
            for filename in files:
                if cmp(filename, saved_progress) > 0:
                    returned_filename = filename;
                    break;
    return returned_filename;


def get_last_new_image(directory,  filter='.source.' ,saved_progress=None):
  #  print 'here the progress is '+saved_progress;
    files = getSortedFiles(directory,filter);
    returned_filename = '';
    if len(files) > 0:
        if 'Test' in directory:
            if saved_progress is None:
                returned_filename = files[0];
            else:
                for i in range(len(files)):
                    if cmp(files[i], saved_progress) > 0:
                        returned_filename = files[i];
                        break;
        else:
            if saved_progress is None:
                    returned_filename = files[-1];
            else:
                    if cmp(files[-1], saved_progress) > 0:
                        returned_filename = files[-1];
    return returned_filename;
def remove_exceed(directory, filter='.source.', max_threshold=1500,delete_num=500):
    files = getSortedFiles(directory,filter);
    if len(files)>max_threshold:
        for i in range(delete_num):
            try:
                os.remove(directory+'/'+files[i]);
            except:
                pass;

#print get_last_new_image('miaomiao', '000001.jpg')
