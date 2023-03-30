import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import sys, os,cv2



#############################################################   these class code blocks is  the menu of the dowland tab
class DOWLAND (QWidget):
    def __init__(self):
        super().__init__()
        # self.setting3_value=23
        self.fixed=12     ############################ this code sets arrays of objects left justified and this is the length of the strings
        self.fixed_v=" "     ######################### this code shows what type to set the length of the texts
        self.setAutoFillBackground(True)            ## GUI bacground say fill or not fill
        self.setBackgroundRole(QPalette.Button)     ## sets the  GUI bacground color
        self.setting()


    ########################################################################  these code blocks are the setting of QCheckbox or QRadioButton objects
    def Checkboxx(self,checbox,name="",ceched=False,tristate=False):
        # QCheckBox nesnesini oluşturun ve metni ayarlayın
        checbox.setText(name)
        # Seçme butonunun seçili olup olmadığını ayarlayın
        checbox.setChecked(ceched)
        return checbox

    ####################################################################### these code blocks are the setting of the QCombobox objects
    def Comboboxx(self,items=[],size=(100,30),edit=False):
        combo = QComboBox()
        combo.addItems(items)
        # Seçme butonunun düzenlenebilir olup olmadığını ayarlayın
        combo.setEditable(edit)
        combo.setFixedWidth(size[0])
        combo.setFixedHeight(size[1])
        return  combo

    ######################################################################### these code blocks is the main menu of checkboxx and QRadioButton
    def chackboxs(self):
        self.frame=self.Checkboxx(QRadioButton(),"orginal",True)
        self.mask=self.Checkboxx(QRadioButton(),"black mask",False)
        self.green=self.Checkboxx(QRadioButton(),"white mask",False)
        self.revers_mask=self.Checkboxx(QRadioButton(),"frame",False)
        self.array_gif=self.Comboboxx(["numpy","gif"])

        checck = QHBoxLayout()
        checck.addWidget(self.frame)
        checck.addWidget(self.mask)
        checck.addWidget(self.green)
        checck.addWidget(self.revers_mask)
        checck.addWidget(self.array_gif)
        for i in range(5):
            checck.addStretch()


        return checck

   ###########################################   edits menu of localetion
    def Düzen(self,Qwidget,args):
        src = QHBoxLayout()
        src.addWidget(args[0])
        src.addWidget(Qwidget)
        for i in args[1:]:
            src.addWidget(i)
        for i in range(2):
            src.addStretch()


        return src

    ######################################  saves gif's np.arrays  , as .npy file
    def gif_to_npy(self,src,arrays):

        np.save(src,arrays)

    ############################################################################  finds new file names for saved files
    def file_name(self,default_name="new_gift_",tip="npy",url="duzenli_gifler"):
        liste=[]

        src=url.split("file:///")[-1]
        src=src.split("\\"+default_name)[0]

        for i in os.listdir(src):

            if i.endswith(f".{tip}"):
                liste.append(i)
        ek=1



        while 1:
            if default_name+str(ek)+f".{tip}" not in  liste:
                break
            ek+=1
        return src+"\\"+default_name+str(ek)+f".{tip}"



    ############################################################### these code blocks are main menu of dowland tab
    def setting(self):
        ###############################################  button saves your wants file
        self.download = QPushButton(self)
        self.download.setText("Dowloand")
        self.download.setFont(QFont("Ariel", 10))
        ######################################################### button finds your want localition
        self.local = QPushButton(self)
        self.local.setText("▼")
        self.local.setFont(QFont("Ariel",15))
        self.local.setFixedWidth(30)
        self.local.setFixedHeight(30)
        ######################################################### local address shows you
        self.src = QLineEdit(self)
        self.src.setText(self.file_name(url=os.getcwd()+r"\duzenli_gifler"))
        self.src.setFont(QFont("Ariel", 8))



        self.div = QVBoxLayout()
        self.div.setSpacing(5)



        l = QHBoxLayout()
        l.addWidget(QLabel("<h1><i> GİF DOWLOAND </i></h1>"))
        self.div.addLayout(l)
        self.div.addStretch()

        setting=QVBoxLayout()


        setting.addLayout(self.chackboxs())
        setting.addStretch()
        setting.addStretch()


        self.div.addLayout(setting)
        self.div.addLayout(self.Düzen(self.src,[QLabel("SRC : ".ljust(self.fixed)),self.local]))
        self.div.addStretch()
        self.div.addStretch()
        self.div.addStretch()

        button1 = QHBoxLayout()
        button1.addStretch()
        button1.addWidget(self.download)
        for i in range(5):
            button1.addStretch()


        #############################################  this code if will  local button is press, binds chancle_src
        self.local.clicked.connect(self.chancle_src)

        self.div.addLayout(button1)

        self.setLayout(self.div)

    ##################################################### this code blocks shows you want address prints to the  GUI
    def chancle_src(self):
        try:
            src=QFileDialog.getExistingDirectoryUrl()
            konum=self.file_name(url=src.url())
            self.src.setText(konum)
        except:
            pass



    def gif_to_mp4(self,src,frams,speed):
        # Kaydedilecek video özellikleri
        width = frams[0].shape[1]
        height = frams[0].shape[0]
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(src, codec, speed, (width, height))
        for i in frams:
            out.write(i)




