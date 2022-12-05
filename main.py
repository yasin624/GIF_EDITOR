#########################################################################################  LİBRARY APPEND
import datetime
from typing import Tuple
import parameters as prt

import cv2,time,os
import numpy as np #matematic library
import mediapipe as mp
from face_function import FACE_FUNCTİON as FF

######################################### image menu

#####################################################################################################



class frame(FF):
    def __init__(self):
        super().__init__()
        self.mp_face_mesh = mp.solutions.face_mesh
        self.cam=cv2.VideoCapture(0) ############################ take image from wepcam

        self.fps=1
        self.LEFT_IRIS = prt._LEFT_IRIS
        self.RIGHT_IRIS = prt._RIGHT_IRIS
        self.LEFT_EYE=prt._LEFT_EYE
        self.RIGHT_EYE=prt._RIGHT_EYE

        self.looked_me_size=0

        self.FACE_W=prt._FACE_W
        self.FACE_H=prt._FACE_H

        self.eye_up_down_points=prt._eye_up_down_points
        self.eye_left_right_points=prt._eye_left_right_points

        self.fps_stabil=0
        self.prev_frame_time=0 ################################## for  fist time fps

        self.memory_faces=[]
        self.memory_index=0
        #[[0,[300,500],100]]

    def video_capture(self):

        with self.mp_face_mesh.FaceMesh(max_num_faces=prt._TRACKİNG_FACE, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
            while True:
                ret, frame = self.cam.read()
                img_h, img_w = prt._İMAGE_SİZE
                frame=cv2.resize(frame,(img_w*2,img_h*2))
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   #Mediapipe precisa do formato de cores RGB mas o OpenCV usa o BGR

                results = face_mesh.process(rgb_frame)

                memory_saved=[]

                if results.multi_face_landmarks:
                    face_meshs=self.FACE_MESH(results=results,img_shape=frame.shape[:2])
                    #mesh_points=np.array([np.multiply([p.x, p.y], [img_w*2, img_h*2]).astype(int) for p in results.multi_face_landmarks[0].landmark])

                    for which_face,mesh_points in enumerate(face_meshs):


                        frame=self.draw_circle(frame,mesh_points,full=True,color=(0,0,255))



                        frame=self.FOR(frame,mesh_points,self.LEFT_EYE,radius=2)
                        frame=self.FOR(frame,mesh_points,self.RIGHT_EYE,radius=2)

                        center_right,center_left,r_radius,l_radius=self.pupil_dedection(mesh_points,self.LEFT_IRIS,self.RIGHT_IRIS)

                        cv2.circle(frame, center_left, int(l_radius), (255, 0, 0), -1, cv2.LINE_AA)
                        cv2.circle(frame, center_right, int(r_radius), (255, 0, 0), -1, cv2.LINE_AA)

                        frame=self.FOR(frame,mesh_points,self.LEFT_IRIS,radius=3,thickness=-1)
                        frame=self.FOR(frame,mesh_points,self.RIGHT_IRIS,radius=3,thickness=-1)

                        ###########################################################  contour lines

                        frame=self.draw_line(frame,mesh_points,self.FACE_W)
                        face_wight=self.find_center_two_point(mesh_points[self.FACE_W[0]],mesh_points[self.FACE_W[1]])

                        frame=self.draw_line(frame,mesh_points,self.FACE_H)
                        face_height=self.find_center_two_point(mesh_points[self.FACE_H[0]],mesh_points[self.FACE_H[1]])

                        frame=self.draw_line(frame,mesh_points,[self.LEFT_IRIS[1],self.RIGHT_IRIS[1]],color=(128, 0, 128))

                        irises_b_width=self.find_center_two_point(mesh_points[self.LEFT_IRIS[1]],mesh_points[self.RIGHT_IRIS[1]])

                        frame=self.draw_line(frame,mesh_points,self.eye_left_right_points[0],color=(0, 255, 255))
                        frame=self.draw_line(frame,mesh_points,self.eye_left_right_points[1],color=(0, 255, 255))
                        l_eye_widht=self.find_center_two_point(mesh_points[self.eye_left_right_points[0][0]],mesh_points[self.eye_left_right_points[0][1]])
                        r_eye_widht=self.find_center_two_point(mesh_points[self.eye_left_right_points[1][0]],mesh_points[self.eye_left_right_points[1][1]])

                        frame=self.draw_line(frame,mesh_points,self.eye_up_down_points[0],color=(0, 255, 255))
                        frame=self.draw_line(frame,mesh_points,self.eye_up_down_points[1],color=(0, 255, 255))
                        l_eye_height=self.find_center_two_point(mesh_points[self.eye_up_down_points[0][0]],mesh_points[self.eye_up_down_points[0][1]])
                        r_eye_height=self.find_center_two_point(mesh_points[self.eye_up_down_points[1][0]],mesh_points[self.eye_up_down_points[1][1]])

                        l_eye_proportion=int((l_eye_height/l_eye_widht)*100)
                        r_eye_proportion=int((r_eye_height/r_eye_widht)*100)

                        frame=self.draw_text(frame,[[450,50]],"DID LOOKED AT ME : ",size=1,color=prt.color.Kmor,thickness=4)
                        frame=self.draw_text(frame,[[450,90]],"HOW MANY: ",size=1,color=prt.color.Kmor,thickness=4)






                        e_f_widht_proportion=int((irises_b_width/face_wight)*100)

                        face_proportion=int((face_wight/face_height)*100)


                        #####################################################################   contuor colculations

                        frame,center_pointer,d_up,d_down,d_left,d_right,turn_left,turn_up,left_look,up_look=self.contuor_center_point([mesh_points[i] for i in self.FACE_H],
                                                                                                                                      [mesh_points[i] for i in self.FACE_W],
                                                                                                                                      frame,img_shape=(img_w,img_h))




                        frame=self.draw_circle(frame,[center_pointer],radius=8,color=(255,0,0),thickness=-1)

                        frame=self.draw_circle(frame,[center_pointer],radius=int(prt._center_redius/self.fps),color=prt.color.blue,thickness=3)


                        inside,this_face_index=None,None

                        ###############################################################################3   whose face is this
                        if self.fps_stabil<10:
                            self.fps_stabil+=1
                        else:
                            print(face_wight,center_pointer)
                            self.memory_index,self.memory_faces,memory_saved,inside,this_face_index,frame=self.same_face_controls(self.memory_index,self.memory_faces,memory_saved,
                                                                                                                mesh_points,center_pointer,frame,face_wight)





                        if l_eye_proportion>prt._eyes_open or r_eye_proportion>prt._eyes_open:
                            print("inside : ",inside)
                            #time.sleep(0.2)
                            frame=self.draw_text(frame,[[20,50]],"GOZ ACIK",size=2,color=(0,255,0))

                            #print("#"*100,"\n")
                            ##print("face_wight : ",face_wight ," :  face_height  :  ",face_height,"  :  irises_b_width  :  ",irises_b_width )
                            #print("l_eye_widht : ",l_eye_widht ," :  r_eye_widht  :  ",r_eye_widht,"  :  l_eye_height  :  ",l_eye_height,"  :  r_eye_height  :  ",r_eye_height )
                            #print("l_eye_proportion : ",l_eye_proportion ," :  r_eye_proportion  :  ",r_eye_proportion,"  :  e_f_widht_proportion  :  ",e_f_widht_proportion,"  :  face_proportion  :  ",face_proportion )
                            #print("#"*80,"\n")


                            ###########  ratio of eye center point to eye width
                            eye_center_points=[self.LEFT_IRIS[1],self.RIGHT_IRIS[1]]
                            eye_width=[]


                            face_width=face_wight
                            img_height,img_width=prt._İMAGE_SİZE
                            iris_oran,looking_me,direction=self.looking_me(left_look,
                                                                  mesh_points,
                                                                  eye_center_points,
                                                                  self.eye_left_right_points,
                                                                  turn_left,face_width,img_width)
                            iris_oran_up,looking_me_up,direction_up=self.looking_me_u_d(up_look,
                                                                            mesh_points,
                                                                            eye_center_points,
                                                                            self.eye_up_down_points,
                                                                            center_pointer,
                                                                            turn_up,face_height,img_height)


                            #print(inside,this_face_index)
                            #self.control_eye(looking_me_up) and sonra eklenecek

                            if  self.control_eye(looking_me) and inside!=None and this_face_index!=None:
                                #print("burda")
                                frame=self.draw_text(frame,[[615,50]]," YES ",size=1,color=prt.color.Yesil,thickness=6)
                                #print("insideeeeeee : ",inside)
                                if inside==False or self.memory_faces[this_face_index][-1]==False:
                                    #print("burada : ",int(self.memory_faces[this_face_index][-2]))
                                    if int(self.memory_faces[this_face_index][-2])>319:
                                        print("adam farklı  : ",inside,int(self.memory_faces[this_face_index][-2]))
                                        self.looked_me_size+=1
                                        self.memory_faces[this_face_index][-1]=True


                            else:
                                frame=self.draw_text(frame,[[615,50]]," NO ",size=1,color=prt.color.Kirmizi,thickness=6)

                            frame=self.draw_text(frame,[[570,90]],str(self.looked_me_size),size=1,color=prt.color.Yesil,thickness=6)










                            if type(looking_me)==list:
                                text=["face_wight : "+str(face_wight),
                                      "face_height : "+str(face_height),
                                      "irises_b_width  :  "+str(irises_b_width),
                                      "l_eye_widht : "+str(l_eye_widht),
                                      "r_eye_widht  : "+str(r_eye_widht),
                                      "l_eye_height  :  "+str(l_eye_height),
                                      "r_eye_height  : "+str(r_eye_height ),
                                      "l_eye_proportion : "+str(l_eye_proportion),
                                      "r_eye_proportion  :  "+str(r_eye_proportion),
                                      "e_f_widht_proportion  :  "+str(e_f_widht_proportion),
                                      "face_proportion  :  "+str(face_proportion ),
                                      "eye_oran[0]  :  "+str(iris_oran[0]),
                                      "eye_oran[1]  :  "+str(iris_oran[1]),
                                      "left  :  "+str("loking at  me " if looking_me[0] else "Not loking at  me "),
                                      "Right :  "+str("loking at  me " if looking_me[1] else "Not loking at  me "),
                                      "iris direction [0]  :  "+str(direction[0]),
                                      "iris direction [1]  :  "+str(direction[1]),

                                      "eye_oranti_up[0]  :  "+str(iris_oran_up[0]),
                                      "eye_oranti_up[1]  :  "+str(iris_oran_up[1]),
                                      "looking_me_up[0]  :  "+str("loking at  me " if looking_me_up[0] else "  Not loking me "),
                                      "looking_me_up[1]  :  "+str("loking at  me " if looking_me_up[1] else "  Not loking me "),
                                      "iris direction_up [0]  :  "+str(direction_up[0]),
                                      "iris direction_up [1]  :  "+str(direction_up[1])
                                      ]
                            else:
                                text=["face_wight : "+str(face_wight),
                                      "face_height : "+str(face_height),
                                      "irises_b_width  :  "+str(irises_b_width),
                                      "l_eye_widht : "+str(l_eye_widht),
                                      "r_eye_widht  : "+str(r_eye_widht),
                                      "l_eye_height  :  "+str(l_eye_height),
                                      "r_eye_height  : "+str(r_eye_height ),
                                      "l_eye_proportion : "+str(l_eye_proportion),
                                      "r_eye_proportion  :  "+str(r_eye_proportion),
                                      "e_f_widht_proportion  :  "+str(e_f_widht_proportion),
                                      "face_proportion  :  "+str(face_proportion ),
                                      "eye_width  :  "+str(iris_oran),
                                      "iris direction :  "+str(direction),
                                      "left eye  :  "+str("loking at  me " if looking_me else "Not loking at  me "),

                                      "eye_oranti_up[0]  :  "+str(iris_oran_up[0]),
                                      "eye_oranti_up[1]  :  "+str(iris_oran_up[1]),
                                      "iris direction_up [0]  :  "+str(direction_up[0]),
                                      "iris direction_up [1]  :  "+str(direction_up[1]),
                                      "looking_me_up[0]  :  "+str("loking at  me " if looking_me_up[0] else "  Not loking me "),
                                      "looking_me_up[1]  :  "+str("loking at  me " if looking_me_up[1] else "  Not loking me "),
                                      ]


                            for s,i in enumerate(text):
                                frame=self.draw_text(frame,[[prt._right_menu[0],prt._right_menu[1]+(20*s)]],i,size=1)



                        else:
                            #print("göz kapalı")
                            frame=self.draw_text(frame,[[20,50]],"GOZ KAPALI",size=2)


                #print(" tamm liste : " , self.memory_faces)
                #print(" memory liste : " , memory_saved)
                for i in self.memory_faces:
                    if i[0] in memory_saved:
                        #print("burda")
                        pass
                    else:
                        self.memory_faces.remove(i)

                #print(" temizlenen  liste : " , len(self.memory_faces))
                ##############################   measure fps and print to main image
                new_frame_time = time.time() ##################### elapsed time

                frame=self.FPS(new_frame_time,frame)     #####################  fps dectance

                #cv2.imshow("hand_dedector_2",frame)
                cv2.imshow("hand_dedector_1",frame)############# main image print

                if cv2.waitKey(1) & 0xFF == ord('q'): ### if print  "q" button
                    self.cam.release() ################## turn of wepcam
                    cv2.destroyAllWindows()


    def control_eye(self,look_list):

        if type(look_list)==list:
            well=True
            for i in look_list:
                if i:
                    pass
                else:
                    return False
            return well
        else:
            return look_list


    def FPS(self,time,img):
        #################################### fps
        self.fps = 1/(time-self.prev_frame_time)
        self.prev_frame_time=time
        cv2.putText(img, "FPS : "+str(int(self.fps)), (1100,30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100, 255, 0),1)
        return img
if __name__=="__main__" :
    video=frame()
    video.video_capture()
    cv2.destroyAllWindows()
