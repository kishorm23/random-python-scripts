#capture image on webcam with OpenCV
import Image;
import cv;
import subprocess
import ImageStat
import time
 
capture = cv.CreateCameraCapture(0)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH, 128)
cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT, 128);
 
if not capture:
                print "Error"
                sys.exit(1)
while 1:                       
        frame = cv.QueryFrame(capture)
        cv.SaveImage("./cam.bmp",frame)
        image =Image.open("./cam.bmp").convert('L')
        stats = ImageStat.Stat(image)
        stats = stats.mean[0]
       
        brightval = hex(int((255 - (stats*1.5))))
        currentval=subprocess.Popen("setpci -s 00:02.0 F4.B",shell=True,stdout=subprocess.PIPE).stdout.read()
        if abs(int(brightval,16) - int(currentval,16)) > 30:
                print int(brightval,16)
                command = "setpci -s 00:02.0 F4.B=" + str(brightval)
                subprocess.Popen(command,shell=True)
        else:
                time.sleep(5)
