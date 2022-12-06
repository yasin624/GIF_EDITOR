import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import sys, os,cv2
from gif_arkaplansilme import gif_background_delete as clear_gif
from setting import Right_menu
from gift_menu import Left_menu




class setup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gif_src=r"img_and_gift\rasengan2.gif"
        ##########################################################  table
        self.left_menu = Left_menu()
        self.right_menu = Right_menu()

        ######################################################  setup settings
        self.setWindowTitle("GİFT EDİT  VS: 7.12.22 ")
        self.setWindowIcon(QIcon("logo.ico"))
        self.setMinimumSize(1200,800)


        self.fixed_size=(300,300)
        self.start=True
        self.start_gif=True
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

        self.right_menu.gifs.currentIndexChanged.connect(self.stop_gif)




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

    def stop_gif(self):
        self.start_gif=False
    def show_gif(self):

        self.start=True
        clear=clear_gif()
        while self.start:
            self.start_gif=True
            self.gif_video=cv2.VideoCapture("img_and_gift/"+self.right_menu.gifs.currentText())

            while self.start_gif:
                okay, orginal_frame = self.gif_video.read()
                if not okay or not self.start:
                    break




                orginal_frame=cv2.resize(orginal_frame,(300,300))

                frame,black_mask,white_mask=clear.Delete(orginal_frame,
                                              hsv= True if self.right_menu.hsv_or_threshold.currentText()=="hsv" else False,
                                              background="white",
                                              dusuk=np.array([self.right_menu.MIN_h.value(),self.right_menu.MIN_s.value(),self.right_menu.MIN_v.value()]),
                                              yüksek=np.array([self.right_menu.MAX_h.value(),self.right_menu.MAX_s.value(),self.right_menu.MAX_v.value()]),
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
                    black_mask=self.cv2_to_pixmap(black_mask,format=QImage.Format_Grayscale8)
                    self.left_menu.resim4.setPixmap(black_mask)
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
                    white_mask=self.cv2_to_pixmap(white_mask)
                    self.left_menu.resim3.setPixmap(white_mask)
                    self.left_menu.resim3_abount.setText("white mask")

                else:
                    self.left_menu.resim3.clear()
                    self.left_menu.resim3_abount.clear()


                cv2.waitKey(self.right_menu.SPEAD_V.value())




    def closeEvent(self, event):
        exit()







app = QApplication(sys.argv)
dowland = setup()
dowland.show()
sys.exit(app.exec_())
