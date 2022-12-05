import cv2
import numpy as np

class window():
    def __init__(self):
        pass

    ##########################################  new image menu
    def new_image_menu(self,img,menu="",menu_value=np.array({})):

        if menu=="main_menu":  #################################  main_menu
            new_soz={}
            for k,v in menu_value.item().items():
                img = cv2.rectangle(img, (v[0],0),(v[1],50),(255, 255, 255),-1)##########################  backround color for color menu
                cv2.putText(img,k, (v[0]+10,30), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1)#############  title for color menu
                new_soz[k]=[(v[0],0),(v[1],50)]########################################################## save location color
            return img,new_soz
        ########################################################################################################################
        else:

            img = cv2.rectangle(img, (880,0),(930,50), (255, 255, 255),-1) ############################# backround color  for new image button
            cv2.putText(img, "|||", (895,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0),2)############# name  for new image button
            return img
    #############################################################################################################################

    ##############################   measure fps and print to main image
    def FPS(self,img,time,prev_frame_time,org=(500,30)):
        #################################### fps
        fps = 1/(time-prev_frame_time)
        prev_frame_time=time
        cv2.putText(img, "FPS : "+str(int(fps)), org=(org[0]-140,30), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(100, 255, 0),thickness=1)

        return img,prev_frame_time
    ############################################################################################################

    def reklam(self,img,org=(500,500),color=(0,255,0)):
        img[-20:,-450:]=np.array(img[-20:,-450:]/4,dtype=np.uint8)################### main images darkening
        img=cv2.putText(img, text= " Tum haklari saklidir @ 2022 | yalcinyazilimcilik ", org=(org[0]-450,org[1]-7),
                             fontFace= cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.65, color=(0,255,0),
                             thickness=1)
        return img