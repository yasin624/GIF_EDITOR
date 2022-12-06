import numpy as np
import sys, os,cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


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

