import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import sys, os,cv2
from gif_arkaplansilme import gif_background_delete as clear_gif
from setting import Right_menu
from gift_menu import Left_menu
from dowload import DOWLAND




class setup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gif_src=r"img_and_gift\rasengan2.gif"
        ##########################################################  table
        self.left_menu = Left_menu()
        self.right_menu = Right_menu()
        self.gif_dowload = DOWLAND()

        ######################################################  setup settings
        self.setWindowTitle("GİFT EDİT  VS: 7.12.22 ")
        self.setWindowIcon(QIcon("logo.ico"))
        self.setMinimumSize(1200,800)


        self.fixed_size=(300,300)
        self.start=True
        self.start_gif=True
        self.start_frame=False
        self.clear=clear_gif()
        ######################################################## they parameters 'boundedTo', 'expandedTo', 'grownBy','scale', 'scaled', 'setHeight', 'setWidth', 'shrunkBy', 'transpose', 'transposed', 'width'
        self.içerik()

    def içerik(self):
        #######################################################  text menu
        menu = self.menuBar()
        self.dosya = menu.addMenu("file")
        self.konum = QAction("Dowland files")
        self.dosya.addAction(self.konum)

        ######################################################  table menu
        self.tablo = QTabWidget()

        self.tablo.tablo1 = QWidget()
        self.tablo.tablo2 = QWidget()

        self.tablo.addTab(self.tablo.tablo1, "MENU")
        self.tablo.addTab(self.tablo.tablo2, "GIF DOWLAND")

        #####################################################  satatus bar (info the bar)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Tüm hakları saklıdır © 2020 | yalcınyazılımcılık")

        ###################################################   full the tables
        self.tab1()
        self.tab2()
        self.setCentralWidget(self.tablo)
        ################################################################### file download location
        self.dosya.triggered.connect(self.konum_belirle)

        self.right_menu.start.clicked.connect(self.gif_frame_control)
        self.right_menu.stop_gif.clicked.connect(self.stoped)

        self.right_menu.gifs.currentIndexChanged.connect(self.stop_gif)
        self.gif_dowload.download.clicked.connect(self.frame_or_gif_control_dowland)

    def frame_or_gif_control_dowland(self):
        tip=self.right_menu.gifs.currentText()
        if tip.endswith(".gif"):
            self.gifDowloand()
        elif tip.endswith(".jpg") or tip.endswith(".png"):
            self.frameDowload()
    def gif_frame_control(self):
        src="img_and_gift/"+self.right_menu.gifs.currentText()
        if src.endswith(".gif"):
            self.start=True
            self.start_frame=False
            self.show_gif(src)
        elif src.endswith(".jpg") or src.endswith(".png"):
            self.start=False
            self.start_frame=True
            self.show_frame(src)

    def Frame_control_of_download(self,orginal_frame,black_mask,frame,white_mask):
        if self.gif_dowload.frame.isChecked():
            return orginal_frame
        elif self.gif_dowload.mask.isChecked():
            return black_mask
        elif self.gif_dowload.green.isChecked():
            return white_mask
        elif self.gif_dowload.revers_mask.isChecked():
            return frame


    def frameDowload(self):
        orginal_frame=cv2.imread("img_and_gift/"+self.right_menu.gifs.currentText())

        frame,black_mask,white_mask=self.clearBackroung(orginal_frame)


        image=self.Frame_control_of_download(orginal_frame,black_mask,frame,white_mask)
        isim=self.gif_dowload.file_name(url=self.gif_dowload.src.text(),tip="png")
        self.gif_dowload.src.setText(isim)
        print(isim)
        cv2.imwrite(self.gif_dowload.src.text(),image)

        self.gif_dowload.src.setText(self.gif_dowload.file_name(url=self.gif_dowload.src.text(),tip="png"))

    def gifDowloand(self):

        gif_video=cv2.VideoCapture("img_and_gift/"+self.right_menu.gifs.currentText())
        gif_frams=[]
        while True:
            okay, orginal_frame = gif_video.read()
            if not okay :
                break
            frame,black_mask,white_mask=self.clearBackroung(orginal_frame)
            gif_frams.append(self.Frame_control_of_download(orginal_frame,black_mask,frame,white_mask))
            cv2.waitKey(1)
        self.gif_dowload.gif_to_npy(self.gif_dowload.src.text(),gif_frams)
        self.gif_dowload.src.setText(self.gif_dowload.file_name(url=self.gif_dowload.src.text()))

    def tab1(self):


        ############################################################### main_menu fulling
        parse = QHBoxLayout()
        parse.addWidget(self.left_menu)
        parse.addStretch()
        parse.addStretch()
        parse.addStretch()
        parse.addWidget(self.right_menu)


        self.tablo.tablo1.setLayout(parse)
    def tab2(self):


        ############################################################### main_menu fulling
        parse = QHBoxLayout()
        parse.addWidget(self.gif_dowload)

        self.tablo.tablo2.setLayout(parse)
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

        if dene.text() == "Dowland files":
            self.tablo.setCurrentIndex(1)
        self.status.showMessage("Tüm hakları saklıdır © 2020 | yalcınyazılımcılık")


    def cv2_to_pixmap(self,img,format=QImage.Format_BGR888):

        img =  QImage(img, img.shape[1], img.shape[0], format)
        return QPixmap.fromImage(img)
    def stoped(self):
        self.start=False


    def stop_gif(self):
        self.start_gif=False
        self.start=False
        self.start_frame=False
        self.gif_frame_control()

    def show_frame(self,src):
        clear=clear_gif()
        orginal_frame=cv2.imread(src)

        while self.start_frame:
            if not self.start_frame:
                break

            orginal_frame=cv2.resize(orginal_frame,(int(300*(int(self.right_menu.fram_size_v.value())/3)),
                                                        int(300*(int(self.right_menu.fram_size_v.value())/3))))
            frame,black_mask,white_mask=self.clearBackroung(orginal_frame)


            self.gif_control_and_img_update(orginal_frame,black_mask,frame,white_mask)
            cv2.waitKey(self.right_menu.SPEAD_V.value())

    def clearBackroung(self,orginal_frame):

        frame,black_mask,white_mask=self.clear.Delete(orginal_frame,
                                                 hsv= True if self.right_menu.hsv_or_threshold.currentText()=="hsv" else False,
                                                 background="white",
                                                 dusuk=np.array([self.right_menu.MIN_h.value(),self.right_menu.MIN_s.value(),self.right_menu.MIN_v.value()]),
                                                 yüksek=np.array([self.right_menu.MAX_h.value(),self.right_menu.MAX_s.value(),self.right_menu.MAX_v.value()]),
                                                 threshold=(self.right_menu.MIN_V.value(),self.right_menu.MAX_V.value()),
                                                 green_perde=False)

        return frame,black_mask,white_mask

    def gif_control_and_img_update(self,orginal_frame,black_mask,frame,white_mask):

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

    def show_gif(self,src):

        clear=clear_gif()
        while self.start:
            self.start_gif=True
            self.gif_video=cv2.VideoCapture(src)

            while self.start_gif:
                okay, orginal_frame = self.gif_video.read()
                if not okay or not self.start:
                    break



                orginal_frame=cv2.resize(orginal_frame,(int(300*(int(self.right_menu.fram_size_v.value())/3)),
                                                        int(300*(int(self.right_menu.fram_size_v.value())/3))))

                frame,black_mask,white_mask=self.clearBackroung(orginal_frame)

                self.gif_control_and_img_update(orginal_frame,black_mask, frame, white_mask)



                cv2.waitKey(self.right_menu.SPEAD_V.value())




    def closeEvent(self, event):
        exit()







app = QApplication(sys.argv)
dowland = setup()
dowland.show()
sys.exit(app.exec_())
