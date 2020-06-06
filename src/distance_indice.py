import cv2
from imutils import paths
import numpy as np
import imutils


def start_end(iter,img_ht,img_wt):
  x1=0
  x2=img_wt
  y2=img_ht-(iter*18*img_ht/(39*39))
  y1=img_ht-(iter*18*img_ht/(39*39))
  

  return x1,y1,x2,y2




def largest(arr,n): 
  
    # Initialize maximum element 
    if len(arr)<1:
      max=0
    else:
      max = cv2.contourArea(arr[0])
    
  
    # Traverse array elements from second 
    # and compare every element with  
    # current max 
    for i in range(1, n): 
        if cv2.contourArea(arr[i]) > max: 
            max = cv2.contourArea(arr[i])
    return max


def find_marker(image):
  	# convert the image to grayscale, blur it, and detect edges
    
    img_ht=image.shape[0]
    img_wt=image.shape[1]

    #selecting roi
    upper_left=(0,25*img_ht/40)    #4/6
    bottom_right=(img_wt,img_ht)

    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(hsv,(7,7),cv2.BORDER_DEFAULT)
    _,thresh = cv2.threshold(blur,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #hsv=cv2.findNonZero(thresh)

    


    #splitting image into 40 parts
    
      #lined_hor_img=cv2.line(thresh,(x1,y1),(x2,y2),(255,255,255),2)
      

    
    #lined_img=cv2.line(thresh,(0,4*img_ht/6),(img_wt,4*img_ht/6),(255,255,255),2)
    #print(thresh[(4*img_ht/6)-1:4*img_ht/6,img_wt/2:img_wt])
    #thresh=cv2.line(thresh,(0,(16*img_ht/20)),(img_wt,16*img_ht/20),(255,255,255),2)    #bottom line
    #thresh=cv2.line(thresh,(0,(13*img_ht/20)),(img_wt,13*img_ht/20),(255,255,255),2)#upper line
    #thresh=cv2.line(thresh,(img_wt/2,0),(img_wt/2,img_ht),(255,255,255),2)  #vertical
    #_,contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image, contours, -1, (0,255,0), 3)

    diff_ht=3*img_ht/20
    diff_wt=img_wt/2

    inc_ht=diff_ht/4
    inc_wt=diff_wt/4

    bottom_ht=16*img_ht/20
    arr = [0,0,0,0]


    for i in range(1,5):
      _,contours,_=cv2.findContours(thresh[bottom_ht-i*inc_ht:bottom_ht-(i-1)*inc_ht,img_wt/2:img_wt],cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      cv2.drawContours(image[bottom_ht-i*inc_ht:bottom_ht-(i-1)*inc_ht,img_wt/2:img_wt] ,contours,-1,(0,255,0),3)
      
      
      
      n=len(contours)
      area= largest(contours,n)  #cv2.contourArea(contours)
      
      arr[4-i] = area/inc_wt*3
    

    
    

    #for i in range(1,40):
    #  cv2.countNonZero()


    
    



    # define range of white color in HSV
    # change it according to your need !
    #lower_white = np.array([0,0,0], dtype=np.uint8)
    #upper_white = np.array([0,0,255], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    #mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(image,image, mask= mask)

    return image, arr



