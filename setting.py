import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import sys, os,cv2
############################################################### these codes  ,right a menu of main menu , And this menu change the setting of images
class Right_menu(QWidget):
    def __init__(self):
        super().__init__()
        ##self.setting3_value=23
        self.fixed=12 ############################ this code sets object sitrings to justify left and this  sets lengs of setrings
        self.fixed_v=" " ######################### this code shows which type to set the length of the texts
        self.setAutoFillBackground(True)        ## GUI bacground say fill or not fill
        self.setBackgroundRole(QPalette.Button) ## sets the  GUI bacground color
        self.div=QVBoxLayout()                  ## it is the main menu of the setting menu
        self.setting()                          ## call  the main menu


        ######################################################################### these are  all function of the objects like QSlider,QSpinBox
    def QObje(self,obje,min,max,step,size=(100,10),value=0,togather=None):
        # Kaydırma tuşunun hareket edeceği minimum ve maksimum değerlerini ayarlayın
        o=obje
        o.setMinimum(min)
        o.setMaximum(max)
        # Kaydırma tuşunun ne kadar adımda hareket edeceğini ayarlayın
        o.setSingleStep(step)
        o.setFixedWidth(size[0])
        o.setFixedHeight(size[1])
        o.setValue(value)
        return o
    ######################################################################### these are  all function of the objects like QCheckBox,QRadioButton
    def Checkboxx(self,checbox,name="",ceched=False,tristate=False):
        # QCheckBox nesnesini oluşturun ve metni ayarlayın
        checbox.setText(name)
        # Seçme butonunun seçili olup olmadığını ayarlayın
        checbox.setChecked(ceched)
        return checbox

    ######################################################################### these codes are  all function of the QComboBox
    def Comboboxx(self,items=[],size=(100,30),edit=False):
        combo = QComboBox()
        combo.addItems(items)
        # Seçme butonunun düzenlenebilir olup olmadığını ayarlayın
        combo.setEditable(edit)
        combo.setFixedWidth(size[0])
        combo.setFixedHeight(size[1])
        return  combo
    ###################################################################### this code upload gif names to QcomboBoxs
    def gif_upload(self,src):
        liste=[]
        for i in os.listdir(src):
            if i.endswith(".gif") or i.endswith(".jpg") or i.endswith(".png"):
                liste.append(i)

        return liste

    ##################################################################### these codes make QSlider and QSpinBox , And append to menu ,next return this object
    def hsv_hue(self):
        ###############################################  # hsv hue (renk aralığı) min ##### this make the min  huve value of hsv
        self.MIN_h =  self.QObje(QSlider(Qt.Horizontal),0,180,1,(200,20))
        self.MIN_hv =  self.QObje(QSpinBox(),0,180,1,(50,20))
        self.MIN_hv.valueChanged.connect(self.MIN_h.setValue)                         ##### this the min_hv' value equalizes the value of min_h
        self.MIN_h.valueChanged.connect(self.MIN_hv.setValue)                         ##### this the min_h' value equalizes the value of min_hv
        ###############################################  # MAX hue                    ##### this make the min  huve value of hsv
        self.MAX_h =  self.QObje(QSlider(Qt.Horizontal),0,180,1,(200,20),value=180)
        self.MAX_hv =  self.QObje(QSpinBox(),0,180,1,(50,20),value=180)
        self.MAX_hv.valueChanged.connect(self.MAX_h.setValue)                         ##### this the max_hv' value equalizes the value of max_h
        self.MAX_h.valueChanged.connect(self.MAX_hv.setValue)                         ##### this the max_h' value equalizes the value of max_hv

        min_hue = QHBoxLayout()
        min_hue.addStretch()
        min_hue.addWidget(QLabel("Min H:".ljust(self.fixed,self.fixed_v)))
        min_hue.addStretch()
        min_hue.addWidget(self.MIN_h)
        min_hue.addStretch()
        min_hue.addWidget(self.MIN_hv)
        min_hue.addStretch()

        max_hue = QHBoxLayout()
        max_hue.addStretch()
        max_hue.addWidget(QLabel("Max H :".ljust(self.fixed,self.fixed_v)))
        max_hue.addStretch()
        max_hue.addWidget(self.MAX_h)
        max_hue.addStretch()
        max_hue.addWidget(self.MAX_hv)
        max_hue.addStretch()

        return min_hue,max_hue

    ##################################################################################  these codes sets value of  hsv staturation
    def hsv_saturation(self):
        ###############################################  # MIN saturation (doygunluk) ### this code sets min value of saturation
        self.MIN_s=  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20),value=80)
        self.MIN_sv =  self.QObje(QSpinBox(),0,255,1,(50,20),value=80)
        self.MIN_sv.valueChanged.connect(self.MIN_s.setValue)                       ##### this  MIN_sv' value equalizes the value of MIN_s
        self.MIN_s.valueChanged.connect(self.MIN_sv.setValue)                       ##### this  MIN_s' value equalizes the value of MIN_sv
        ###############################################  # MAX saturation           ##### this code sets max value of saturation
        self.MAX_s =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20),value=255)
        self.MAX_sv =  self.QObje(QSpinBox(),0,255,1,(50,20),value=255)
        self.MAX_sv.valueChanged.connect(self.MAX_s.setValue)                       ##### this  MAX_sv' value equalizes the value of MAX_s
        self.MAX_s.valueChanged.connect(self.MAX_sv.setValue)                       ##### this  MAX_s' value equalizes the value of MAX_sv

        min_saturation = QHBoxLayout()
        min_saturation.addStretch()
        min_saturation.addWidget(QLabel("Min S :".ljust(self.fixed,self.fixed_v)))
        min_saturation.addStretch()
        min_saturation.addWidget(self.MIN_s)
        min_saturation.addStretch()
        min_saturation.addWidget(self.MIN_sv)
        min_saturation.addStretch()

        max_saturation = QHBoxLayout()
        max_saturation.addStretch()
        max_saturation.addWidget(QLabel("Max S :".ljust(self.fixed,self.fixed_v)))
        max_saturation.addStretch()
        max_saturation.addWidget(self.MAX_s)
        max_saturation.addStretch()
        max_saturation.addWidget(self.MAX_sv)
        max_saturation.addStretch()

        return min_saturation,max_saturation


    ##################################################################################  these codes sets value of  hsv value
    def hsv_value(self):
        ###############################################  # MIN value(parlaklık)  ####### sets min value of hsv value
        self.MIN_v =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20),value=80)
        self.MIN_vv =  self.QObje(QSpinBox(),0,255,1,(50,20),80)
        self.MIN_vv.valueChanged.connect(self.MIN_v.setValue)                    ####### sets min_vv' value equalizes value of min_v
        self.MIN_v.valueChanged.connect(self.MIN_vv.setValue)                    ####### sets min_vv' value equalizes value of min_v
        ###############################################  # MAX value             ####### sets min value of hsv value
        self.MAX_v =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20),value=255)
        self.MAX_vv =  self.QObje(QSpinBox(),0,255,1,(50,20),value=255)
        self.MAX_vv.valueChanged.connect(self.MAX_vv.setValue)                   ####### sets MAX_vv' value equalizes value of MAX_vv
        self.MAX_v.valueChanged.connect(self.MAX_v.setValue)                   ####### sets MAX_v' value equalizes value of MAX_v

        min_value = QHBoxLayout()
        min_value.addStretch()
        min_value.addWidget(QLabel("Min V :".ljust(self.fixed,self.fixed_v)))
        min_value.addStretch()
        min_value.addWidget(self.MIN_v)
        min_value.addStretch()
        min_value.addWidget(self.MIN_vv)
        min_value.addStretch()

        max_value = QHBoxLayout()
        max_value.addStretch()
        max_value.addWidget(QLabel("Max V :".ljust(self.fixed,self.fixed_v)))
        max_value.addStretch()
        max_value.addWidget(self.MAX_v)
        max_value.addStretch()
        max_value.addWidget(self.MAX_vv)
        max_value.addStretch()

        return min_value,max_value
    ######################################################  make menu of hsv
    def hsv_menu(self):
        min_h,max_h=self.hsv_hue()
        min_s,max_s=self.hsv_saturation()
        min_v,max_v=self.hsv_value()


        hsv = QVBoxLayout()
        hsv.addStretch()
        hsv.addLayout(min_h)
        hsv.addStretch()
        hsv.addLayout(max_h)
        hsv.addStretch()
        hsv.addStretch()
        hsv.addLayout(min_s)
        hsv.addStretch()
        hsv.addLayout(max_s)
        hsv.addStretch()
        hsv.addStretch()
        hsv.addLayout(min_v)
        hsv.addStretch()
        hsv.addLayout(max_v)
        hsv.addStretch()
        hsv.addStretch()

        return hsv


    ###########################################################   making menu of thredhold
    def thredshold_menu(self):
        ###############################################  # MIN threshold ######  sets min value of threshold
        self.MIN =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20))
        self.MIN_V =  self.QObje(QSpinBox(),0,255,1,(50,20))
        self.MIN_V.valueChanged.connect(self.MIN.setValue)
        self.MIN.valueChanged.connect(self.MIN_V.setValue)
        ###############################################  # MAX threshold  ######  sets max value of threshold
        self.MAX =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20),value=255)
        self.MAX_V =  self.QObje(QSpinBox(),0,255,1,(50,20),value=255)
        self.MAX_V.valueChanged.connect(self.MAX.setValue)
        self.MAX.valueChanged.connect(self.MAX_V.setValue)

        min_thredshold = QHBoxLayout()
        min_thredshold.addStretch()
        min_thredshold.addWidget(QLabel("Min :".ljust(self.fixed,self.fixed_v)))
        min_thredshold.addStretch()
        min_thredshold.addWidget(self.MIN)
        min_thredshold.addStretch()
        min_thredshold.addWidget(self.MIN_V)
        min_thredshold.addStretch()

        max_thredshold = QHBoxLayout()
        max_thredshold.addStretch()
        max_thredshold.addWidget(QLabel("Max :".ljust(self.fixed,self.fixed_v)))
        max_thredshold.addStretch()
        max_thredshold.addWidget(self.MAX)
        max_thredshold.addStretch()
        max_thredshold.addWidget(self.MAX_V)
        max_thredshold.addStretch()

        thredshold = QVBoxLayout()
        thredshold.addStretch()
        thredshold.addLayout(min_thredshold)
        thredshold.addStretch()
        thredshold.addLayout(max_thredshold)
        thredshold.addStretch()

        return thredshold


    ########################################################   making menu of chackboxs
    def chackboxs(self):
        ######################################################################
        self.frame=self.Checkboxx(QCheckBox(),"orginal",True)
        self.mask=self.Checkboxx(QCheckBox(),"black mask",True)
        self.green=self.Checkboxx(QCheckBox(),"white mask",True)
        self.revers_mask=self.Checkboxx(QCheckBox(),"frame",True)

        checck = QHBoxLayout()
        checck.addStretch()
        checck.addWidget(self.frame)
        checck.addStretch()
        checck.addWidget(self.mask)
        checck.addStretch()
        checck.addWidget(self.green)
        checck.addStretch()
        checck.addWidget(self.revers_mask)
        checck.addStretch()

        return checck

    #########################################################  making menu of spead control
    def spead_control(self):
        ###############################################  # GİF SPEAT
        self.SPEAD =  self.QObje(QSlider(Qt.Horizontal),1,1000,50,(200,20),value=160)
        self.SPEAD_V =  self.QObje(QSpinBox(),1,1000,50,(50,20),value=160)
        self.SPEAD_V.valueChanged.connect(self.SPEAD.setValue)
        self.SPEAD.valueChanged.connect(self.SPEAD_V.setValue)

        sped = QHBoxLayout()
        sped.addStretch()
        sped.addWidget(QLabel("Sped :".ljust(self.fixed,self.fixed_v)))
        sped.addStretch()
        sped.addWidget(self.SPEAD)
        sped.addStretch()
        sped.addWidget(self.SPEAD_V)
        sped.addStretch()

        return sped
    ############################################# sets size of an image
    def size_control(self):
        ###############################################  # GİF SPEAT
        self.fram_size =  self.QObje(QSlider(Qt.Horizontal),1,12,1,(200,20),value=3)
        self.fram_size_v =  self.QObje(QSpinBox(),1,12,1,(50,20),value=3)
        self.fram_size_v.valueChanged.connect(self.fram_size.setValue)
        self.fram_size.valueChanged.connect(self.fram_size_v.setValue)

        size = QHBoxLayout()
        size.addStretch()
        size.addWidget(QLabel("size :".ljust(self.fixed,self.fixed_v)))
        size.addStretch()
        size.addWidget(self.fram_size)
        size.addStretch()
        size.addWidget(self.fram_size_v)
        size.addStretch()

        return size

    #################################################    main menu of right menu
    def setting(self):
        ###############################################  button plays  gif
        self.start = QPushButton(self)
        self.start.setText("start")
        self.start.setFont(QFont("Ariel", 10))

        ###############################################  button stops gif
        self.stop_gif = QPushButton(self)
        self.stop_gif.setText("stop")
        self.stop_gif.setFont(QFont("Ariel", 10))


        ###############################################   specify the hsv or the thresold
        self.hsv_or_threshold=self.Comboboxx(["threshold","hsv"])

        ###############################################  uploads gif names to the ComboBox
        self.gifs=self.Comboboxx(self.gif_upload(src="img_and_gift"),size=(220,30))





        self.main_div() ###################################################### calls the main menu

        ############################################## edits  the menu
        self.div.setSpacing(20)
        self.div.setContentsMargins(20, 20, 20, 20)
        self.div.setSizeConstraint(50)


        ################################ clicking th button , controls the  value of hsv
        self.hsv_or_threshold.currentIndexChanged.connect(self.hsv_control)
        self.hsv_control()


        self.setLayout(self.div)


    ########################################################## controls value of hsv
    def hsv_control(self):
        hsv=[self.MIN_h,self.MIN_hv,self.MAX_h,self.MAX_hv,
             self.MIN_s,self.MIN_sv,self.MAX_s,self.MAX_sv,
             self.MIN_v,self.MIN_vv,self.MAX_v,self.MAX_vv]

        thredhold=[self.MIN,self.MIN_V,self.MAX,self.MAX_V]

        ################################################# if the hsv is true , thredhol's setting will not be true,hsv'setting will be true
        if self.hsv_or_threshold.currentText()=="hsv":
            for i in thredhold:
                i.setEnabled(False)
            for i in hsv:
                i.setEnabled(True)

        else:
            for i in thredhold:
                i.setEnabled(True)
            for i in hsv:
                i.setEnabled(False)



    #############################  these codes  are  main menu codes
    def main_div(self):

        self.div = QVBoxLayout()
        l = QHBoxLayout()
        l.addWidget(QLabel("<h1><i> SETTİNG LAYER </i></h1>"))
        l.addStretch()
        self.div.addLayout(l)
        self.div.addStretch()

        setting=QVBoxLayout()

        up_setting = QHBoxLayout()
        up_setting.addWidget(self.hsv_or_threshold)
        up_setting.addStretch()
        up_setting.addWidget(self.gifs)
        up_setting.addStretch()
        setting.addLayout(up_setting)
        setting.addStretch()
        setting.addStretch()




        setting.addLayout(self.chackboxs())
        setting.addStretch()
        setting.addStretch()


        setting.addLayout(self.thredshold_menu())
        setting.addStretch()
        setting.addStretch()

        setting.addLayout(self.hsv_menu())
        setting.addStretch()
        setting.addStretch()



        self.div.addLayout(setting)

        self.div.addStretch()
        self.div.addLayout(self.size_control())
        self.div.addStretch()
        self.div.addStretch()
        self.div.addLayout(self.spead_control())
        self.div.addStretch()

        self.div.addStretch()

        button1 = QHBoxLayout()
        button1.addStretch()
        button1.addWidget(self.start)
        button1.addStretch()
        button1.addWidget(self.stop_gif)
        button1.addStretch()
        self.div.addLayout(button1)


