import os
import cv2
import json
import glob
import os.path
import argparse
import numpy as np
from time import sleep
from datetime import time, datetime

from backgroundSubstractorClass import ObjectCenters

parser = argparse.ArgumentParser(description='Add folder to process')
parser.add_argument('-f', '--checkFolder', default = None, type=str, help="Add path to the folder to check")

parser.add_argument('-k', '--kmeansclusters', default = None, type=str, help="K number")

args = parser.parse_args()

if args.checkFolder != None:
    rutaDeTrabajo = args.checkFolder
    print('Ruta a limpiar: {}'.format(rutaDeTrabajo))
else:
    print('No se introdujo folder a revisar')

if args.kmeansclusters != None:
    K = args.kmeansclusters
else:
    K = 4
print('K = {}'.format(K))

if __name__ == '__main__':
    dirs = [d for d in os.listdir(rutaDeTrabajo) if os.path.isdir(os.path.join(rutaDeTrabajo, d))]
    dirs = sorted(dirs)
    print('Found {} folders to check'.format(len(dirs)))

    for index in range(len(dirs)):
        if 'debug' in dirs[index]:
            del dirs[index]

    print('Found {} non debug folders to check'.format(len(dirs)))
    print('Training background substractor')
    vacio = True
    numeroVideo = 0
    contador = 0
    video = [file for file in os.listdir(rutaDeTrabajo+'/'+dirs[numeroVideo]) if '.mp4' in file ]
    miCamara = cv2.VideoCapture(rutaDeTrabajo+'/'+dirs[numeroVideo]+'/'+video[0])
    detector = ObjectCenters()
    while vacio:
        ret, frameFlujo = miCamara.read()
        if ret:
            centros = detector.getForeground(frameFlujo)
            cv2.imshow('Background Training', frameFlujo)
            ch = 0xFF & cv2.waitKey(1)
            if ch == ord('q'):
                break
        else:
            numeroVideo += 1
            video = [file for file in os.listdir(rutaDeTrabajo+'/'+dirs[numeroVideo]) if '.mp4' in file ]
            miCamara = cv2.VideoCapture(rutaDeTrabajo+'/'+dirs[numeroVideo]+'/'+video[0])
            print('Pasando video')
            continue
        if len(centros) != 0:
            vacio = False
            print('Background cargado exitosamente')
        contador += 1
        if numeroVideo > 10:
            break
    cv2.destroyAllWindows()
    # Ahora que esta cargado:
    numeroVideo = 0
    video = [file for file in os.listdir(rutaDeTrabajo+'/'+dirs[numeroVideo]) if '.mp4' in file ]
    miCamara = cv2.VideoCapture(rutaDeTrabajo+'/'+dirs[numeroVideo]+'/'+video[0])
    while True:
        if numeroVideo == len(dirs):
            break
        ret, frameFlujo = miCamara.read()
        if ret:
            centros = detector.getForeground(frameFlujo)
            for point in centros:
                frameFlujo = cv2.circle(frameFlujo,tuple(point),5,(255,255,255))
            cv2.imshow('Video Analisys', frameFlujo)
            ch = 0xFF & cv2.waitKey(125)
            if ch == ord('q'):
                break
        else:
            numeroVideo += 1
            video = [file for file in os.listdir(rutaDeTrabajo+'/'+dirs[numeroVideo]) if '.mp4' in file ]
            miCamara = cv2.VideoCapture(rutaDeTrabajo+'/'+dirs[numeroVideo]+'/'+video[0])
            print('Pasando video')
            continue
        
    #miCamara = cv2.VideoCapture(0)