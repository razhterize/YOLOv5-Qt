# -*- coding: utf-8 -*-

"""
Author: mxy
Email: mxy493@qq.com
Date: 2021/11/5
Desc: 信息板块
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGroupBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

class WidgetInfo(QWidget):
    def __init__(self):
        super(WidgetInfo, self).__init__()

        self.img_src = 'img/bat-half.png'

        hbox = QHBoxLayout()
        self.pixmap_src = QPixmap(self.img_src)
        self.bat_label = QLabel()
        self.bat_label.setPixmap(self.pixmap_src.scaled(40, 20))

        self.label_fps = QLabel('FPS: ')
        hbox.addWidget(self.label_fps)
        hbox.addWidget(self.bat_label)
        self.bat_label.setAlignment(Qt.AlignRight)

        box = QGroupBox()
        box.setLayout(hbox)

        _vbox = QVBoxLayout()
        _vbox.setContentsMargins(0, 0, 0, 0)
        _vbox.addWidget(box)
        self.setLayout(_vbox)

    def update_fps(self, fps):
        self.label_fps.setText(f'FPS: { "" if fps <= 0 else round(fps, 1)}')
    
    def update_bat_status(self, src):
        img_src = src
        self.pixmap_src = QPixmap(img_src)
        self.bat_label.setPixmap(self.pixmap_src.scaled(40, 20))

 


    
