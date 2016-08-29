import pyexiv2


# In[5]:

import re
def get_folder(metadata):
    try:
        date = metadata["Exif.Image.DateTime"].value
        date_string = date.strftime('%Y-%m')
    except:
        date_string = 'Date unknown'
    try:
        camera_string = metadata["Exif.Image.Model"].raw_value
        final_string = " ".join([date_string, camera_string])
    except:
        final_string = date_string
        camera_string = ""
    
    if "nexus" in camera_string.lower() or "iphone" in camera_string.lower():
        try:
            final_string = date.strftime('%Y') + " " + camera_string
        except:
            final_string = 'Date unknown' + " " + camera_string
    
    final_string = re.sub('\s+',' ',final_string)
    final_string = re.sub('\s+$','',final_string)
    return final_string


# In[6]:

import os
import shutil
base = r"F:\Digital photos new"
new = r"F:\Digital photos new 2"


import traceback
import sys


counter = 0
for root, subdirs, files in os.walk(base):
    
    files = sorted(files, key=lambda x: ".jpg" not in x.lower())
  
    for f in files:
        counter +=1
        if counter % 200 == 0:
            print counter
        try:
            if "thumbs.db" in f.lower() or "thumbnail" in f.lower():
                continue

            depth = root.count(os.sep) - base.count(os.sep)

            this_file = os.path.join(root,f)
            if ".jpg" in f.lower():
                metadata = pyexiv2.ImageMetadata(this_file)
                metadata.read()
                new_folder = get_folder(metadata)

                try:
                    os.makedirs(os.path.join(new,new_folder))
                except:
                    pass

            if "good" in this_file:
                f = f.replace("good","")
                f = "00good" + f
                f = f.replace(r" .", ".")
            if not os.path.exists(os.path.join(new,new_folder,f)):
                shutil.copy(this_file, os.path.join(new,new_folder,f))
        except Exception, err:
            print "{}".format(this_file)
            print(traceback.format_exc())
