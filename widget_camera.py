# -*- coding: utf-8 -*-

"""
Author: mxy
Email: mxy493@qq.com
Date: 2020/11/3
Desc: 摄像头界面
"""
import os
from pathlib import Path
import numpy as np
import time
import pyautogui

import cv2

from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPixmap, QImage, QFont, QBrush, QPen, QStaticText
from PyQt5.QtWidgets import QWidget

import msg_box
from gb import thread_runner, YOLOGGER
from yolo import YOLO5


class WidgetCamera(QWidget):
    def __init__(self):
        super(WidgetCamera, self).__init__()

        self.yolo = YOLO5()
        current_date = time.strftime('%d-%m-%Y_%H-%M', time.localtime())
        self.path = f'output/{current_date}'

        self.sh, self.sw = self.height(), self.width()

        self.opened = False  # 摄像头已打开
        self.detecting = False  # 目标检测中
        self.record = False
        self.cap = cv2.VideoCapture()

        self.fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')  # XVID MPEG-4
        self.writer = cv2.VideoWriter()  # Record Vide, turn on camera then record

        self.pix_image = None   # QPixmap video frame
        self.image = None       # Current image
        self.scale = 1          # Scaling
        self.objects = []

        self.fps = 0            # Frame rate

    def open_camera(self, use_camera, video):
        """Turn on camera (webcam), return true if success"""
        self.x = 1
        YOLOGGER.info('Turn on Camera')
        cam = 0     # Default camera
        if not use_camera:
            cam = video  # local video
        flag = self.cap.open(cam)   # open camera
        if flag:
            self.opened = True  # 已打开
            return True
        else:
            msg = msg_box.MsgWarning()
            msg.setText('Failed to start video！\n'
                        'Make sure camera or video file correct！')
            msg.exec()
            return False

    def close_camera(self):
        YOLOGGER.info('Turn off camera')
        self.opened = False  #  Close YOLO detection then camera
        self.stop_detect()  # Stop YOLO
        time.sleep(0.1)  # Wait for last frame to be detected
        self.cap.release()
        self.x = 1
        self.reset()  # return to original state

    @thread_runner
    def show_camera(self, fps=0):
        """Pass frame information, camera is 0 while video is 30 or 60"""
        YOLOGGER.info('Display thread start')
        wait = 1 / fps if fps else 0
        while self.opened:
            self.read_image()  # read frame every 0.02 or 0.03s
            if fps:
                time.sleep(wait)  # wait for [wait] seconds before read and display frame
            self.update()
        self.update()
        YOLOGGER.info('Display thread ends')

    def read_image(self):
        ret, img = self.cap.read()
        if ret:
            # 删去最后一层
            if img.shape[2] == 4:
                img = img[:, :, :-1]
            # self.image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.image = img

    @thread_runner
    def run_video_recorder(self, fps=10):
        """Run video writer"""
        YOLOGGER.info('Video writer run')
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        # make sure output folder exist, if not create one
        if not os.path.exists('output'):
            os.mkmdir('output')
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        # wait for a screen
        t0 = time.time()
        while self.image is None:
            time.sleep(0.01)
            # avoid thread can't exist due to no screen
            if time.time() - t0 > 3:
                YOLOGGER.warning('Frame was not acquired after timeout, video recording canceled')
                break

        # If screen exist, start recording
        if self.image is not None: 
            # open video writer
            self.writer.open(
                filename=f'{self.path}/{now}_record.avi',
                fourcc=self.fourcc,
                fps=fps,
                frameSize=(self.sw, self.sh))  # save video

            wait = 1 / fps - 0.004  # wait for writer to finish
            while self.opened:
                rec_src = QPixmap(self.grab(QRect(0,0,self.sw, self.sh))).toImage()
                s = rec_src.bits().asstring(self.sw * self.sh * 4)
                arr = np.fromstring(s, dtype=np.uint8).reshape((self.sh, self.sw, 4)) 
                self.writer.write(arr)
                time.sleep(wait)
        self.record = False
        YOLOGGER.info('video recording thread ends')

    def stop_video_recorder(self):
        """停止视频录制线程"""
        if self.writer.isOpened():
            self.writer.release()

            path = os.path.abspath('output')
            msg = msg_box.MsgSuccess()
            msg.setText(f'录制的视频已保存到以下路径:\n{path}')
            msg.setInformativeText('本窗口将在5s内自动关闭!')
            QTimer().singleShot(5000, msg.accept)
            msg.exec()

    def image_capture(self):
        img_name = f"{self.path}/capture_{self.x}.png"
        img = QPixmap(self.grab(QRect(0,0, self.sw, self.sh)))
        QPixmap.save(img, img_name, "JPEG", 100)
        YOLOGGER.info("Image captured")
        self.x += 1

    @thread_runner
    def start_detect(self):
        # 初始化yolo参数
        YOLOGGER.info('目标检测线程开始')
        self.detecting = True
        while self.detecting:
            if self.image is None:
                continue
            # 检测
            t0 = time.time()
            self.objects = self.yolo.obj_detect(self.image)
            t1 = time.time()
            self.fps = 1 / (t1 - t0)
            self.update()
        self.update()
        YOLOGGER.info('目标检测线程结束')

    def stop_detect(self):
        """停止目标检测"""
        self.detecting = False

    def reset(self):
        """恢复初始状态"""
        self.opened = False  # 摄像头关闭
        self.pix_image = None  # 无QPixmap视频帧
        self.image = None  # 当前无读取到的图片
        self.scale = 1  # 比例无
        self.objects = []  # 无检测到的目标
        self.fps = 0  # 帧率无

    def resizeEvent(self, event):
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        qp.setWindow(0, 0, self.width(), self.height())  # 设置窗口
        qp.setRenderHint(QPainter.SmoothPixmapTransform)
        # Draw a framework background
        # qp.setBrush(QColor('#cecece'))  # Frame background color background color
        qp.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.width(), self.height())
        qp.drawRect(rect)

        sw, sh = self.width(), self.height()  # 图像窗口宽高
    

        if not self.opened:
            qp.drawPixmap((sw-1)/2-100, sh/2-100, 200, 200, QPixmap('img/video.svg'))

        # 画图
        if self.opened and self.image is not None:
            ih, iw, _ = self.image.shape
            self.scale = sw / iw if sw / iw < sh / ih else sh / ih  # 缩放比例
            px = round((sw - iw * self.scale) / 2)
            py = round((sh - ih * self.scale) / 2)
            qimage = QImage(self.image.data, iw, ih, 3 * iw, QImage.Format_BGR888)  # 转QImage
            qpixmap = QPixmap.fromImage(qimage.scaled(sw, sh, Qt.KeepAspectRatio))  # 转QPixmap
            pw, ph = qpixmap.width(), qpixmap.height()  # 缩放后的QPixmap大小
            qp.drawPixmap(px, py, qpixmap)

            # 画目标框
            font = QFont()
            font.setFamily('Microsoft YaHei')
            font.setPointSize(10)
            qp.setFont(font)
            brush1 = QBrush(Qt.NoBrush)  # 内部不填充
            qp.setBrush(brush1)
            pen = QPen()
            pen.setWidth(2)  # 边框宽度
            for obj in self.objects:
                rgb = [round(c) for c in obj['color']]
                pen.setColor(QColor(rgb[0], rgb[1], rgb[2]))  # 边框颜色
                qp.setPen(pen)
                # 坐标 宽高
                ox, oy = px + round(pw * obj['x']), py + round(ph * obj['y'])
                ow, oh = round(pw * obj['w']), round(ph * obj['h'])
                obj_rect = QRect(ox, oy, ow, oh)
                qp.drawRect(obj_rect)  # 画矩形框

                # 画 类别 和 置信度
                qp.drawText(ox, oy - 5, str(obj['class']) + str(round(obj['confidence'], 2)))

