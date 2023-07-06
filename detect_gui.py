# coding-utf-8
# /home/lx/.conda/envs/pytorch_lx/bin/python3.6
# AUTHOR:lx
# IDE : PyCharm
# DATE: 2022/12/5 19:53
import os
import PyQt5
import cv2
import sys
import numpy as np
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from yolov5 import detect

def detect_(img_path):
    # 将img_path中的/替换为\\
    img_path = img_path.replace('/', '\\')
    results = detect.my_run(img_path)
    return results


label_img_size = (640, 512)


class FuseGUI:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('目标检测')
        self.window.setGeometry(0, 0, 1700, 1000)
        self.ir_image_path = ''

        # add a label to show origin image
        self.label_sr_image = QLabel(self.window)
        self.set_image_label(self.label_sr_image, 110, 100, label_img_size[0], label_img_size[1])

        # add a label to show result image
        self.label_result_image = QLabel(self.window)
        self.set_image_label(self.label_result_image, 910, 100, label_img_size[0], label_img_size[1])

        # create a button about 可见光
        self.button_sr = QPushButton('选择待检测图像', self.window)
        self.set_button(self.button_sr, '选择待检测图像', 300, 700, 150, 30)
        self.button_sr.clicked.connect(
            lambda: self.show_img(
                QFileDialog.getOpenFileName(self.window, '选择待检测图像', './', 'Image Files(*.jpg *.png)')[0],
                self.label_sr_image))


        # add a button to choose origin image
        self.button_fuse = QPushButton('检测', self.window)
        self.set_button(self.button_fuse, '检测', 1200, 700, 150, 30)
        self.button_fuse.clicked.connect(lambda: self.show_result(self.label_result_image))

        # add a label
        self.label_origin = QLabel(self.window)
        self.set_text_label(self.label_origin, '待检测图像', 300, 0, 150, 100)

        # add a label
        self.label_result = QLabel(self.window)
        self.set_text_label(self.label_result, '检测结果', 1200, 0, 150, 100)

        # show the window
        self.window.show()
        # start the Qt application
        self.app.exec_()

    def show_img(self, img_path, label, size=label_img_size):
        img = QPixmap(img_path)
        img = img.scaled(size[0], size[1])
        label.setPixmap(img)
        self.ir_image_path = img_path

    def show_result(self, label):
        result = detect_(self.ir_image_path)
        cv2.imwrite('result.png', result)
        img = QPixmap('result.png')
        img = img.scaled(label_img_size[0], label_img_size[1])
        label.setPixmap(img)

    @staticmethod
    def set_button(button, text, x, y, w, h):
        button.setText(text)
        button.move(x, y)
        button.resize(w, h)

    @staticmethod
    def set_text_label(label, text, x, y, w, h):
        label.setText(text)
        label.move(x, y)
        label.resize(w, h)
        label.setFont(PyQt5.QtGui.QFont("Roman times", 20, PyQt5.QtGui.QFont.Bold))
        label.setStyleSheet("color:rgb(0,0,0)")

    @staticmethod
    def set_image_label(label, x, y, w, h):
        label.move(x, y)
        label.resize(w, h)
        label.setStyleSheet("background-color:rgb(255,255,255)")
        label.setScaledContents(True)


if __name__ == '__main__':
    FuseGUI()
    # 删除临时的‘result.png’文件
    os.remove('result.png')
    # result = detect_('G:\\data\\8bit\\FLIR_00010.jpg')
