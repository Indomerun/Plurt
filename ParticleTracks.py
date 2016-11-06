import numpy as np


def bresenham(x,y,x2,y2):
    """Brensenham line algorithm"""
    steep = 0
    coords = []
    dx = abs(x2 - x)
    if (x2 - x) > 0: sx = 1
    else: sx = -1
    dy = abs(y2 - y)
    if (y2 - y) > 0: sy = 1
    else: sy = -1
    if dy > dx:
        steep = 1
        x,y = y,x
        dx,dy = dy,dx
        sx,sy = sy,sx
    d = (2 * dy) - dx
    for i in range(0,dx):
        if steep: coords.append((y,x))
        else: coords.append((x,y))
        while d >= 0:
            y = y + sy
            d = d - (2 * dx)
        x = x + sx
        d = d + (2 * dy)
    return coords


def initializeTrackMatrix(i, data, tracksCutoff, matrixRange):
    trackDataMatrix = np.zeros((1024, 1024))
    trackAlpha = np.zeros((1024, 1024))
    for track in data:
        if (data[track].shape[0] > i) and (data[track][i, 6] > tracksCutoff):
            currentBin = (int(1024 * (data[track][i, 1] - matrixRange[2]) / (matrixRange[3] - matrixRange[2])),
                          int(1024 * (data[track][i, 0] - matrixRange[0]) / (matrixRange[1] - matrixRange[0])))
            trackDataMatrix[currentBin] = data[track][i, 6]
            trackAlpha[currentBin] = 1
    return trackDataMatrix, trackAlpha


def updateTrackMatrix(i, data, trackDataMatrix, trackAlpha, tracksCutoff, matrixRange, tracksFadeFactor):
    trackAlpha *= tracksFadeFactor
    for track in data:
        if (data[track].shape[0] > i) and (data[track][i, 6] > tracksCutoff):
            previousBin = (int(1024 * (data[track][i-1, 1] - matrixRange[2]) / (matrixRange[3] - matrixRange[2])),
                          int(1024 * (data[track][i-1, 0] - matrixRange[0]) / (matrixRange[1] - matrixRange[0])))
            currentBin = (int(1024 * (data[track][i, 1] - matrixRange[2]) / (matrixRange[3] - matrixRange[2])),
                          int(1024 * (data[track][i, 0] - matrixRange[0]) / (matrixRange[1] - matrixRange[0])))

            Bins = bresenham(previousBin[0], previousBin[1], currentBin[0], currentBin[1])
            for bin in Bins:
                trackDataMatrix[bin] = data[track][i, 6]
                trackAlpha[bin] = 1
            trackDataMatrix[currentBin] = data[track][i, 6]
            trackAlpha[currentBin] = 1


def getTrackMatrix(data, i, tracksCutoff, matrixRange, tracksFadeFactor):
    trackDataMatrix, trackAlpha = initializeTrackMatrix(max(0,i-32), data, tracksCutoff, matrixRange)
    for j in range(max(0,i-32)+1, i+1):
        updateTrackMatrix(j, data, trackDataMatrix, trackAlpha, tracksCutoff, matrixRange, tracksFadeFactor)
    return trackDataMatrix, trackAlpha