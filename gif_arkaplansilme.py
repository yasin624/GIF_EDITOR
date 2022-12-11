import os

import cv2
import numpy as np

#######################################################################  this software is background's clear for gif,video  and image
class gif_background_delete():
    def __init__(self):
        self.limit=20 ##### this code limets frames of the gif
    #################################################################  this code is for background change
    def perde(self,gif,mask,perde,background):
        if background=="black":
            bak=0
        else:
            bak=255
        for s1,h in enumerate(mask):
            for s2,w in enumerate(h):
                if w!=bak:
                    gif[s1,s2]=perde
        return gif

    ################################################################# these is give the clear background of gif,video or img files
    def Delete(self,gif,newsize=False,hsv=False,green_perde=False,dusuk=np.array([0,80,80]),yüksek=np.array([180,255,255]),background="black",threshold=(80,255)):

        if newsize:  ######################################  if you give newsize's value , it gives you a new shape image
            gif=cv2.resize(gif,(int(gif.shape[1]*newsize),int(gif.shape[0]*newsize)))


        if hsv:  ######################################## if you give  the hvs's value  is true ,it return the image with hsv's background,hsv's mask and hsv's revers_mask
            gif_hsv=cv2.cvtColor(gif,cv2.COLOR_BGR2HSV)
            mask=cv2.inRange(gif_hsv,dusuk,yüksek)

            new=np.zeros(gif.shape,dtype=np.uint8)
            new[:,:]=[255,255,255]
            reverse_mask=cv2.bitwise_not(new,new,mask=mask)
            end_img=cv2.bitwise_and(gif,gif,mask=mask)



        else: ######################################## if you give  the hvs's value  is false ,it return the image with threshold's background,threshold's mask and threshold's revers_mask
            gif_gray=cv2.cvtColor(gif,cv2.COLOR_BGR2GRAY)
            ras,mask=cv2.threshold(gif_gray,threshold[0],threshold[1],cv2.THRESH_BINARY)

            new=np.zeros(gif.shape,dtype=np.uint8)
            new[:,:]=[255,255,255]
            end_img=cv2.bitwise_and(gif,gif,mask=mask)
            reverse_mask=cv2.bitwise_not(new,new,mask=mask)
            #cv2.imshow("end_img",np.array(end_img,dtype=np.uint8))


        if green_perde: ######################################## if you give  the green_perde's value  is type  tuple (0,0,0) values  ,it return the image with you want colorful background,colorful mask and colorful revers_mask
            green=self.perde(end_img.copy(),mask,green_perde,background)
            return end_img,mask,green

        return end_img,mask,reverse_mask

    ########################################################### these codes will return you the values in the frame of the gif image,
    # then convert the squares to np.array values and return it to you
    def convert_gif_to_frames(self,src,newsize=False,hsv=False,dusuk=np.array([0,80,80]),yüksek=np.array([180,255,255]),background="black",threshold=(0,255)):
        gif=cv2.VideoCapture(src)

        frame_list = []
        while True:
            try:
                okay, frame = gif.read()


                frame,mask=self.Delete(frame,newsize=newsize,hsv=hsv,dusuk=dusuk,yüksek=yüksek,background=background,threshold=threshold)
                cv2.imshow("frame",frame)
                frame_list.append(frame)
                self.limit-=1

                if cv2.waitKey(500) and ( not okay or self.limit<1):
                    break

            except:
                break

        return np.array(frame_list)


    ####################################  this code , np.array's values saves  file
    def save(self,frames,src):
        say=1
        for i in os.listdir("duzenli_gifler"):
            if i.startswith(src.split(".")[0]):
                if src.split(".")[0]+str(say)+".npy" in i:
                    say+=1
        src=src.split(".")[0]+str(say)

        np.save("duzenli_gifler/"+src,frames)

    ####################################  this code , arrays in  the  file  return  and show you
    def load_and_show(self,src):
        gif=np.load("duzenli_gifler/"+src)
        print(gif.shape)
        while True:
            for i in gif:
                cv2.imshow("src",i)
                cv2.waitKey(100)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                break



if __name__=="__main__" :
    clear=gif_background_delete()
    #frame=clear.convert_gif_to_frames(r"img_and_gift\rasengan5.gif",hsv=False,background="black",threshold=(190,255),newsize=1)
    #clear.save(frame,"rasengan_.npy")



    clear.load_and_show("rasengan_8.npy")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

