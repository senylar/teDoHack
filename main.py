#%%
from PIL import Image, ImageFilter,ImageColor
import numpy as np
import cv2

#%%
import pandas as pd
#%%
tab = pd.read_excel('/Users/gggg/Downloads/фото в стиле ТеДо, расписанные по критериям в файле/Пример оценки критериев в стиле ТеДо.xlsx')



# rgb_colors = [[0,0,0],[0, 44, 98], [0, 76, 137], [0, 104, 169],[60,119,174],[91,155,204],[131,152,174],[147,172,192],[212,215,219],[217,215,216]]
# colors = [[b, g, r] for [r, g, b] in rgb_colors]
# print(colors)
def chek(imPath):
    
    colors = [[0, 0, 0], [98, 44, 0], [137, 76, 0], [169, 104, 0], [174, 119, 60], [204, 155, 91], [174, 152, 131], [192, 172, 147], [219, 215, 212], [216, 215, 217]] # BGR
    tolerance = 50
    bounds = [(np.array([color[0] - tolerance, color[1] - tolerance, color[2] - tolerance]),
               np.array([color[0] + tolerance, color[1] + tolerance, color[2] + tolerance])) for color in colors]

    image = cv2.imread(imPath)
    masks = [cv2.inRange(image, lower_bound, upper_bound) for lower_bound, upper_bound in bounds]

    rez = np.zeros((masks[0].shape[0],masks[0].shape[1]))
    for i in masks:
        rez = np.add(rez,i)
    per = np.count_nonzero(rez)/(masks[0].shape[0] * masks[0].shape[1])

    if per >= 0.7:
        return 1, per
    else:
        return 0, per




#%%
import os
def get_files_in_directory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and not f.startswith('.')]

#%%
#проверка температуры
def chek_temputer(pathIm):
    img = cv2.imread(pathIm)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    average_hue = np.mean(hsv[:,:,0])

    return average_hue
#%%
paths_to_stiled = get_files_in_directory('/Volumes/Zx20/tedohack/Фото в стиле ТеДо')
paths_to_UNstiled = get_files_in_directory('/Volumes/Zx20/tedohack/Фото НЕ в стиле ТеДо')

semp = 20

s = 0
for i in range(semp):
  
    h, per = chek('/Volumes/Zx20/tedohack/Фото в стиле ТеДо/'+paths_to_stiled[i])

    s += h
    print(per,h)
print(s/semp)


s/semp

sU = 0
for i in range(semp):
    

    h, per = chek('/Volumes/Zx20/tedohack/Фото НЕ в стиле ТеДо/'+paths_to_UNstiled[i])

    sU += h
    print(per,h)
print(1-(sU/semp))
