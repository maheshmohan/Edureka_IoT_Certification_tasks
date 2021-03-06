import os
import cv2
import numpy as np
from PIL import Image


recognizer=cv2.face.LBPHFaceRecognizer_create()#createLBPHFaceRecognizer()
#path="C:\Users\Automation\Downloads\Compressed\Python_Code_M3\Python_Code\OpenCVDemoCode"

#path = open("E:/OpenCVDemoCode/")

path="/home/pi/edureka_iot_works/M3/images"

def getImagesWithID(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return np.array(IDs), faces

Ids,faces=getImagesWithID(path)
print (Ids)
recognizer.train(faces,Ids)
recognizer.save('trainingData.yml')
cv2.destroyAllWindows()