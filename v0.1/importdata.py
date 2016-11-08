import numpy as np
from PIL import Image
import os


def fetch_data(plotSettings, loadedData, frameNumber):
    if plotSettings['name'] in loadedData.keys():
        data = loadedData[plotSettings['name']]
    else:
        data = import_data(plotSettings, frameNumber)
        loadedData[plotSettings['name']] = data
    return data


def import_data(plotSettings, frameNumber):
    if plotSettings['data_type'] == 'float':
        fileName = ("%06d" % frameNumber) + '.bin'
        data = (np.fromfile(plotSettings['name'] + os.path.sep + fileName, dtype='f')).reshape(plotSettings['size'])
        return data
    if plotSettings['data_type'] == 'bmp':
        img = Image.open('../Canada-Flag.bmp')
        return np.asarray(img)
    if plotSettings['data_type'] == 'line':
        x = np.linspace(plotSettings['xMin'], plotSettings['xMax'], plotSettings['size'])
        data = np.array([x, np.sin(x)])
        return data
