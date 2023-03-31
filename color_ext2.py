
# !pip install easydev                 #version 0.12.0
# !pip install colormap                #version 1.0.4
# !pip install opencv-python           #version 4.5.5.64
# !pip install colorgram.py            #version 1.2.0
# !pip install extcolors               #version 1.0.0

# !pip install pillow
# !pip install webcolors
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from keras.preprocessing import image
import cv2
import extcolors
import os
from colormap import rgb2hex
import pandas as pd

import urllib.request
from PIL import Image
from webcolors import  hex_to_rgb

from webcolors import CSS3_HEX_TO_NAMES


from scipy.spatial import KDTree
import sys
from rembg import remove

# input_path = 'input.png'
# output_path = 'output.png'

# with open(input_path, 'rb') as i:
#     with open(output_path, 'wb') as o:
#         input = i.read()
#         output = remove(input)
#         o.write(output)


# output_width = 900                   #set the output size
# img = Image.open(input_name)
# wpercent = (output_width/float(img.size[0]))
# hsize = int((float(img.size[1])*float(wpercent)))
# img = img.resize((output_width,hsize), Image.ANTIALIAS)

# #save
# resize_name = 'resize_' + input_name  #the resized image name
# img.save(resize_name)                 #output location can be specified before resize_name

# #read
# plt.figure(figsize=(9, 9))
# img_url = resize_name
# img = plt.imread(img_url)
# plt.imshow(img)
# plt.axis('off')
# plt.show()


file="'F_Kids_Nightwear&Loungewear_RET-12-1E-10-19_colour_detector.csv'"
temp_file=file[:-5]
print(temp_file)


def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    df = pd.DataFrame(zip(df_color_up, df_percent), columns = ['c_code','occurence'])
    return df

#HEX to RGB

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return names[index]



# print(convert_rgb_to_names((190,53,25)))

def extr_color_name(hex_color_list):
    color_list = []
    for color in hex_color_list:
        hex2rgb = hex_to_rgb(color)
        col_list = convert_rgb_to_names((hex2rgb))
        color_list.append(col_list)
      # print(color_list)
    return color_list 


data=pd.read_csv(file)



if temp_file+'processed_img_ids.pickle' in os.listdir():
    try:
        # Try to load the processed ids from a file
        with open(temp_file+"processed_img_ids.pickle", "rb") as f:
            ids = pickle.load(f)
        colours=pd.read_csv(temp_file+'IdsColors.csv').iloc[:,2]
        colours=list(colours)
    except Exception as e:
        # If the file doesn't exist, start with an empty set
        print(e)
        ids = []
        colours=[]
else:
    ids = []
    colours=[]

print(ids,colours)


for i in range(1,len(data)):
    print(len(data))
    try:
        if data['Myntra Product Code'][i] not in ids:
            print('Product no in excel',i)
            urllib.request.urlretrieve(data['Image'][i],"exam3.png")
            img_url = 'exam3.png'
            with open(img_url, 'rb') as inp_image:
                inpu=inp_image.read()
                output = remove(inpu)
                with open(img_url,'wb+') as otpt:
                    otpt.write(output)
            colors_x = extcolors.extract_from_path(img_url, tolerance = 12, limit = 12)
            df_color = color_to_df(colors_x)
            # df_color
            df_color = df_color[0:3]
            new_list = df_color['c_code'].to_list()
            extracted_colors = extr_color_name(new_list)
            if 'black' in extracted_colors:
                extracted_colors.remove('black')
            else:
                extracted_colors=extracted_colors[:2    ]
            if extracted_colors!=[]:
                ids.append(data['Myntra Product Code'][i])
                colours.append(extracted_colors)
                with open(temp_file+"processed_img_ids.pickle", "wb") as f:
                    pickle.dump(list(ids), f)
                df=pd.DataFrame({"Ids":ids,"Colours":colours})
                df.to_csv(temp_file+'IdsColors.csv')
                extracted_colors=[]
        else:
            print('Record Already Processed')
    except:
        print('Error In record')

    #print(extracted_colors)













