from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
import random
import numpy as np
import sys, os,cv2
from gif_arkaplansilme import gif_background_delete as clear_gif



class Right_menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setting3_value=23
        self.setting()
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
    def Checkboxx(self,checbox,name="",ceched=False,tristate=False):
        # QCheckBox nesnesini oluşturun ve metni ayarlayın
        checbox.setText(name)
        # Seçme butonunun seçili olup olmadığını ayarlayın
        checbox.setChecked(ceched)
        return checbox

    def Comboboxx(self,items=[],size=(100,30),edit=False):
        combo = QComboBox()
        combo.addItems(items)
        # Seçme butonunun düzenlenebilir olup olmadığını ayarlayın
        combo.setEditable(edit)
        combo.setFixedWidth(size[0])
        combo.setFixedHeight(size[1])
        return  combo
    def gif_upload(self,src):
        liste=[]
        for i in os.listdir(src):
            if i.endswith(".gif"):
                liste.append(i)

        return liste
    def setting(self):
        ###############################################   the button dowloand files
        self.start = QPushButton(self)
        self.start.setText("start")
        self.start.setFont(QFont("Ariel", 10))

        ###############################################  the button for world control
        self.stop_gif = QPushButton(self)
        self.stop_gif.setText("stop")
        self.stop_gif.setFont(QFont("Ariel", 10))
        ###############################################  # MIN threshold
        self.MIN =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20))
        self.MIN_V =  self.QObje(QSpinBox(),0,255,1,(50,20))
        self.MIN_V.valueChanged.connect(self.MIN.setValue)
        self.MIN.valueChanged.connect(self.MIN_V.setValue)

        ###############################################  # MAX threshold
        self.MAX =  self.QObje(QSlider(Qt.Horizontal),0,255,1,(200,20),value=255)
        self.MAX_V =  self.QObje(QSpinBox(),0,255,1,(50,20),value=255)
        self.MAX_V.valueChanged.connect(self.MAX.setValue)
        self.MAX.valueChanged.connect(self.MAX_V.setValue)
        ######################################################################
        self.frame=self.Checkboxx(QCheckBox(),"orginal",True)
        self.mask=self.Checkboxx(QCheckBox(),"black mask",True)
        self.green=self.Checkboxx(QCheckBox(),"white mask",True)
        self.revers_mask=self.Checkboxx(QCheckBox(),"frame",True)
        ###############################################  # GİF SPEAT
        self.SPEAD =  self.QObje(QSlider(Qt.Horizontal),1,1000,50,(200,20),value=255)
        self.SPEAD_V =  self.QObje(QSpinBox(),1,1000,50,(50,20),value=255)
        self.SPEAD_V.valueChanged.connect(self.SPEAD.setValue)
        self.SPEAD.valueChanged.connect(self.SPEAD_V.setValue)



        ###############################################   arrangement
        self.hsv_or_threshold=self.Comboboxx(["threshold","hsv"])
        self.gifs=self.Comboboxx(self.gif_upload(src="img_and_gift"),size=(220,30))



        v = QVBoxLayout()
        l = QHBoxLayout()
        l.addWidget(QLabel("<h1><i> SETTİNG LAYER </i></h1>"))
        l.addStretch()
        v.addLayout(l)
        v.addStretch()


        setting=QVBoxLayout()

        up_setting = QHBoxLayout()
        up_setting.addWidget(self.hsv_or_threshold)
        up_setting.addStretch()
        up_setting.addWidget(self.gifs)
        up_setting.addStretch()
        setting.addLayout(up_setting)
        setting.addStretch()
        setting.addStretch()



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
        setting.addLayout(checck)
        setting.addStretch()
        setting.addStretch()




        button3 = QHBoxLayout()
        button3.addStretch()
        button3.addWidget(QLabel("Min : "))
        button3.addStretch()
        button3.addWidget(self.MIN)
        button3.addStretch()
        button3.addWidget(self.MIN_V)
        button3.addStretch()
        setting.addLayout(button3)
        setting.addStretch()


        button3 = QHBoxLayout()
        button3.addWidget(QLabel("Max : "))
        button3.addStretch()
        button3.addWidget(self.MAX)
        button3.addStretch()
        button3.addWidget(self.MAX_V)
        button3.addStretch()
        setting.addLayout(button3)
        setting.addStretch()


        sped = QHBoxLayout()
        sped.addWidget(QLabel("Sped : "))
        sped.addStretch()
        sped.addWidget(self.SPEAD)
        sped.addStretch()
        sped.addWidget(self.SPEAD_V)
        sped.addStretch()
        setting.addLayout(sped)
        setting.addStretch()


        v.addLayout(setting)

        v.addStretch()
        v.addStretch()
        v.addStretch()
        v.addStretch()

        button1 = QHBoxLayout()
        button1.addWidget(self.start)
        button1.addStretch()
        button1.addWidget(self.stop_gif)
        button1.addStretch()
        v.addLayout(button1)

        v.addStretch()

        self.setLayout(v)



class Left_menu(QWidget):
    def __init__(self):
        super().__init__()

        self.etiketler()
    def boxses(self,img,text):
        boxx = QVBoxLayout()
        boxx.addWidget(text)
        boxx.addStretch()
        boxx.addWidget(img)
        return boxx
    def etiketler(self):
        ###############################################   app main icon
        self.resim1 = QLabel(self)
        self.resim1_abount=QLabel(self)
        ###############################################   app main icon
        self.resim2 = QLabel(self)
        self.resim2_abount=QLabel(self)
        ###############################################   app main icon
        self.resim3 = QLabel(self)
        self.resim3_abount=QLabel(self)
        ###############################################   app main icon
        self.resim4 = QLabel(self)
        self.resim4_abount=QLabel(self)
        ###############################################   arrangement
        v = QVBoxLayout()
        l = QHBoxLayout()
        l.addWidget(QLabel("<h1><i> IMAGES LAYER </i></h1>"))
        l.addStretch()
        v.addLayout(l)

        img_parse1 = QHBoxLayout()
        img_parse1.addStretch()
        box1=self.boxses(self.resim1,self.resim1_abount)
        img_parse1.addLayout(box1)
        img_parse1.addStretch()
        box2 = self.boxses(self.resim2,self.resim2_abount)
        img_parse1.addLayout(box2)
        img_parse1.addStretch()
        v.addLayout(img_parse1)

        v.addStretch()
        v.addStretch()

        img_parse2 = QHBoxLayout()
        img_parse2.addStretch()
        box3=self.boxses(self.resim3,self.resim3_abount)
        img_parse2.addLayout(box3)
        img_parse1.addStretch()
        box4 = self.boxses(self.resim4,self.resim4_abount)
        img_parse2.addLayout(box4)
        img_parse2.addStretch()
        v.addLayout(img_parse2)

        v.addStretch()

        self.setLayout(v)


class setup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gif_src=r"img_and_gift\rasengan2.gif"
        ##########################################################  table
        self.left_menu = Left_menu()
        self.right_menu = Right_menu()
        ######################################################  setup settings
        self.setWindowTitle("VİDEO DOWLAND VS: 30.3 ")
        self.setWindowIcon(QIcon("logo.ico"))
        self.setMinimumSize(1000,800)


        self.fixed_size=(300,300)
        self.start=True
        ######################################################## they parameters 'boundedTo', 'expandedTo', 'grownBy','scale', 'scaled', 'setHeight', 'setWidth', 'shrunkBy', 'transpose', 'transposed', 'width'
        self.içerik()

    def içerik(self):
        #######################################################  text menu
        menu = self.menuBar()
        self.dosya = menu.addMenu("file")
        self.konum = QAction("Dowland Local")
        self.konum2 = QAction("Dowland files")
        self.dosya.addAction(self.konum)
        self.dosya.addAction(self.konum2)

        ######################################################  table menu
        self.tablo = QTabWidget()
        self.tablo.tablo1 = QWidget()
        self.tablo.tablo2 = QWidget()
        self.tablo.tablo3 = QWidget()

        self.tablo.addTab(self.tablo.tablo1, "MENU")
        self.tablo.addTab(self.tablo.tablo2, "DOWLAND FİLES")
        self.tablo.addTab(self.tablo.tablo3, "SETİNG")

        #####################################################  satatus bar (info the bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Tüm hakları saklıdır © 2020 | yalcınyazılımcılık")

        ###################################################   full the tables
        self.tab1()
        self.setCentralWidget(self.tablo)
        ################################################################### file download location
        self.dosya.triggered.connect(self.konum_belirle)

        self.right_menu.start.clicked.connect(self.show_gif)
        self.right_menu.stop_gif.clicked.connect(self.stoped)

    def tab1(self):
        ############################################################### main_menu fulling
        parse = QHBoxLayout()
        parse.addWidget(self.left_menu)
        parse.addStretch()
        parse.addStretch()
        parse.addStretch()
        parse.addWidget(self.right_menu)
        self.tablo.tablo1.setLayout(parse)
    def dowloand(self):
        try:
            file_local = self.yol_k.link.text()
            url_local = self.main_m.url.text()
            self.main_m.url.setText("")
            self.dowland_l.send(" " if file_local == None else str(file_local),
                                " " if url_local == None else str(url_local))
        except:
            print("hata 2")

    def konum_belirle(self, dene):
        # cur_index = self.tabWidget.currentIndex() tablo indexleri
        if dene.text() == "Dowland Local":
            self.tablo.setCurrentIndex(2)
        elif dene.text() == "Dowland files":
            self.tablo.setCurrentIndex(1)


    def cv2_to_pixmap(self,img,format=QImage.Format_BGR888):

        img =  QImage(img, img.shape[1], img.shape[0], format)
        return QPixmap.fromImage(img)
    def stoped(self):
        self.start=False


    def show_gif(self):

        self.start=True
        clear=clear_gif()
        while self.start:
            gif=cv2.VideoCapture("img_and_gift/"+self.right_menu.gifs.currentText())

            while True:
                okay, orginal_frame = gif.read()

                if not okay or not self.start:
                    break

                orginal_frame=cv2.resize(orginal_frame,(300,300))

                frame,mask,green=clear.Delete(orginal_frame,hsv=False,background="white",
                                              threshold=(self.right_menu.MIN_V.value(),self.right_menu.MAX_V.value()),
                                              green_perde=False)





                if self.right_menu.frame.checkState()==2:
                    orginal_frame=self.cv2_to_pixmap(orginal_frame)
                    self.left_menu.resim1.setPixmap(orginal_frame)
                    self.left_menu.resim1_abount.setText("orginal_frame")
                else:
                    self.left_menu.resim1.clear()
                    self.left_menu.resim1_abount.clear()

                if self.right_menu.mask.checkState()==2:
                    mask=self.cv2_to_pixmap(mask,format=QImage.Format_Grayscale8)
                    self.left_menu.resim4.setPixmap(mask)
                    self.left_menu.resim4_abount.setText("black mask")
                else:
                    self.left_menu.resim4.clear()
                    self.left_menu.resim4_abount.clear()


                if self.right_menu.revers_mask.checkState()==2:
                    frame=self.cv2_to_pixmap(frame)
                    self.left_menu.resim2.setPixmap(frame)
                    self.left_menu.resim2_abount.setText("frame")
                else:
                    self.left_menu.resim2.clear()
                    self.left_menu.resim2_abount.clear()

                if self.right_menu.green.checkState()==2:
                    green=self.cv2_to_pixmap(green)
                    self.left_menu.resim3.setPixmap(green)
                    self.left_menu.resim3_abount.setText("white mask")

                else:
                    self.left_menu.resim3.clear()
                    self.left_menu.resim3_abount.clear()


                cv2.waitKey(self.right_menu.SPEAD_V.value())







app = QApplication(sys.argv)
dowland = setup()
dowland.show()
sys.exit(app.exec_())
cv2.waitKey(0)
cv2.destroyAllWindows()