import sys
import threading
import platform
import time

import pkg_resources as pkg

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QWindow
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QApplication, QDesktopWidget, QStyle, QLabel

import msg_box
import gb
from gb import YOLOGGER, thread_runner
from info import APP_NAME, APP_VERSION
from settings_dialog import SettingsDialog
from widget_camera import WidgetCamera
from widget_info import WidgetInfo
from widget_config import WidgetConfig
from jetson_stuff import JetsonGPIO

class MainWindow(QMainWindow):
    config_error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        py_min = '3.8.0'
        py_current = platform.python_version()
        py_current, py_min =(pkg.parse_version(x) for x in(py_current, py_min))
        if py_current < py_min:
            msg = msg_box.MsgWarning()
            msg.setText(f'Python Version({py_current}) is not supported. Please use at least ({py_min})!')
            msg.exec_()
            sys.exit()

        self.setWindowTitle(f'{APP_NAME} {APP_VERSION}')
        self.setWindowIcon(QIcon('img/yologo.png'))

        gb.init_logger()
        gb.clean_log()
        gb.init_config()

        self.led_state = False

        self.camera = WidgetCamera()        #Initialize Camera
        self.info = WidgetInfo()            # Information Panel
        self.config = WidgetConfig()        # YOLO Configuration
        self.settings = SettingsDialog()    
        self.status_icon = QLabel()
        self.status_text = QLabel()
        self.btn_camera = QPushButton('Start/Stop Camera')
        self.btn_capture = QPushButton('Capture Image')
        self.btn_lighting = QPushButton()

        self.config_error.connect(self.slot_msg_dialog)

         # Model Thread Load
        self.load_model_thread = threading.Thread(target=self.load_yolo)
        self.load_model_thread.start()

        self.config.btn_settings.clicked.connect(self.settings.exec)
        self.settings.accepted.connect(self.reload)

        self.update_status('Loading Model....', False)
        hbox = QHBoxLayout()
        hbox.addWidget(self.status_icon)
        hbox.addWidget(self.status_text)

        self.btn_camera.setEnabled(False)
        self.btn_camera.clicked.connect(self.open_close_camera)
        self.btn_camera.setFixedHeight(60)

        self.btn_capture.setEnabled(False)
        self.btn_capture.setFixedHeight(60)
        self.btn_capture.clicked.connect(self.camera.image_capture)

        self.btn_lighting.setFixedHeight(30)
        self.btn_lighting.clicked.connect(self.lighting)

        vbox1 = QVBoxLayout()
        vbox1.setContentsMargins(0,0,0,0)
        vbox1.addWidget(self.info)
        vbox1.addWidget(self.config)
        vbox1.addStretch()
        vbox1.addLayout(hbox)
        vbox1.addWidget(self.btn_lighting)
        vbox1.addWidget(self.btn_capture)
        vbox1.addWidget(self.btn_camera)

        right_widget = QWidget()
        right_widget.setMaximumWidth(400)
        right_widget.setLayout(vbox1)

        hbox = QHBoxLayout()
        hbox.addWidget(self.camera, 3)
        hbox.addWidget(right_widget, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        self.central_widget = QWidget()
        self.central_widget.setLayout(vbox)
        self.setCentralWidget(self.central_widget)

        # ------ Dynamic Screen Resizing ------ #
        screen = QDesktopWidget().screenGeometry(self)
        available = QDesktopWidget().availableGeometry(self)
        title_height = self.style().pixelMetric(QStyle.PM_TitleBarHeight)
        if screen.width() < 1280 or screen.height() < 768:
            self.setWindowState(QWindow.showMaximized)                              # Set Maximized Window for small resolution
            self.setFixedSize(available.width(), available.height()-title_height)   # Set maximum Window size according to screen
        else:
            self.setMinimumSize(QSize(1100, 700))       # Minimum Width and Height
        self.show()

    def open_close_camera(self):
        if self.camera.cap.isOpened():
            self.camera.close_camera()
            self.camera.stop_video_recorder()
            self.btn_capture.setEnabled(False)
        else:
            ret = self.camera.open_camera(
                use_camera = self.config.check_camera.isChecked(),
                video = self.config.line_video.text()
            )
            if ret:
                fps = 0 if self.config.check_camera.isChecked() else 30
                self.camera.show_camera(fps = fps)
                if self.config.check_record.isChecked():
                    self.camera.run_video_recorder()
                if self.load_model_thread.is_alive():
                    self.load_model_thread.join()
                self.camera.start_detect()
                self.update_info()
                self.btn_capture.setEnabled(True)
    
    def load_yolo(self):
        # --- Reload YOLO Model --- #
        YOLOGGER.info(f'Model {self.settings.line_weights.text()} is loaded')
        #---- Object Detection ----#
        check, msg = self.camera.yolo.set_config(
            weights=self.settings.line_weights.text(),
            device=self.settings.line_device.text(),
            img_size=int(self.settings.combo_size.currentText()),
            conf=round(self.settings.spin_conf.value(), 1),
            iou=round(self.settings.spin_iou.value(), 1),
            max_det=int(self.settings.spin_max_det.value()),
            agnostic=self.settings.check_agnostic.isChecked(),
            augment=self.settings.check_augment.isChecked(),
            half=self.settings.check_half.isChecked(),
            dnn=self.settings.check_dnn.isChecked()
        )
        # Enable button and camera if model successfully loaded
        if check:
            if not self.camera.yolo.load_model():
                return False
            self.update_status('Model Loaded', True)
            self.btn_camera.setEnabled(True)
            YOLOGGER.info('Model loaded Successfully')
        # Disable Button and Camera if model failed or wrong configuration
        else:
            YOLOGGER.warning('Incorrect configuration, model loading cancelled')
            self.update_status('Model loading failed', False)
            self.btn_camera.setEnabled(False)
            self.camera.stop_detect()
            self.config_error.emit(msg)
            return False
        return True
    
    def reload(self):
        self.update_status('Reloading model...', False)
        self.load_model_thread = threading.Thread(target=self.load_yolo)
        self.load_model_thread.start()

    def slot_msg_dialog(self, text):
        msg = msg_box.MsgWarning()
        msg.setText(text)
        msg.exec()
    
    def lighting(self):
        if self.state is False:
            self.state = True
            self.JetsonGPIO.on_off()
        if self.state is True:
            self.state = False
            self.JetsonGPIO.on_off()

    def update_status(self, text, ok=False):
        size = 15
        min_width = f'min-width: {size}px;'         # Minimum Width
        min_height = f'min-height: {size}px;'       # Minimum Height
        max_width = f'max-width: {size}px;'         # Maximum Width
        max_height = f'max-height: {size}px;'       # maximum Height
        # Set border shape and size
        border_radius = f'border-radius: {size/2}px;'   # Border is rounded
        border = 'border:1px solid black;'               # Black 1px thick border
        # Set background color
        background = "background-color:"
        if ok:
            background += "rgb(0,255,0)"
        else:
            background += "rgb(255,0,0)"
        style = min_width + min_height + max_width + max_height + border_radius + border + background
        self.status_icon.setStyleSheet(str(style))
        self.status_text.setText(text)

    @thread_runner
    def update_info(self):
        YOLOGGER.info('Start update and print fps')
        while self.camera.detecting:
            self.info.update_fps(self.camera.fps)
            time.sleep(0.2)
        self.info.update_fps(self.camera.fps)
        YOLOGGER.info('Stop update and print fps')

    def resizeEvent(self, event):
        self.update()

    def closeEvent(self, event):
        if self.camera.cap.isOpened():
            self.camera.close_camera()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
