# coding-utf-8
# /home/lx/.conda/envs/pytorch_lx/bin/python3.6
# AUTHOR:lx
# IDE : PyCharm
# DATE: 2022/12/5 15:35
import os
import PyQt5
import cv2
import numpy as np
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from color import temp



def colorize(ir_image_path):
    pass


def sr(ir_image_path):
    pass


class GUI:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('图像增强')
        self.window.setGeometry(100, 100, 1300, 600)
        self.ir_image_path = ''

        # add a label to show origin image
        self.label_ir_image = QLabel(self.window)
        self.set_image_label(self.label_ir_image, 110, 100, 320, 256)

        # add a label to show ir image
        self.label_sr_image = QLabel(self.window)
        self.set_image_label(self.label_sr_image, 510, 100, 320, 256)

        # add a label to show result image
        self.label_color_image = QLabel(self.window)
        self.set_image_label(self.label_color_image, 910, 100, 320, 256)

        # create a button about 可见光
        self.button_sr = QPushButton('选择待增强图像', self.window)
        self.set_button(self.button_sr, '选择待增强图像', 200, 400, 150, 30)
        self.button_sr.clicked.connect(
            lambda: self.show_img(
                QFileDialog.getOpenFileName(self.window, '选择待增强图像', './', 'Image Files(*.jpg *.png)')[0],
                self.label_ir_image, self.label_ir_image))

        # add a button to choose origin image
        self.button_choose_origin = QPushButton('超分', self.window)
        self.set_button(self.button_choose_origin, '超分', 600, 400, 150, 30)
        self.button_choose_origin.clicked.connect(
            lambda: self.show_result(self.label_sr_image, 1))

        # add a button to choose origin image
        self.button_fuse = QPushButton('着色', self.window)
        self.set_button(self.button_fuse, '着色', 1000, 400, 150, 30)
        self.button_fuse.clicked.connect(lambda: self.show_result(self.label_color_image, 0))

        # add a label
        self.label_origin = QLabel(self.window)
        self.set_text_label(self.label_origin, '可见光图像', 200, 0, 150, 100)

        # add a label
        self.label_ir = QLabel(self.window)
        self.set_text_label(self.label_ir, '红外图像', 600, 0, 150, 100)

        # add a label
        self.label_result = QLabel(self.window)
        self.set_text_label(self.label_result, '融合图像', 1000, 0, 150, 100)

        # show the window
        self.window.show()
        # start the Qt application
        self.app.exec_()

    def show_img(self, img_path, label, size=(320, 256)):
        img = QPixmap(img_path)
        img = img.scaled(size[0], size[1])
        label.setPixmap(img)
        self.ir_image_path = img_path

    def show_result(self, label, flag):
        if flag == 0:
            colorize(self.ir_image_path)
        else:
            sr(self.ir_image_path)
        img = QPixmap('result.jpg')
        img = img.scaled(320, 256)
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
    GUI()
    # 删除临时的‘result.png’文件
    os.remove('result.png')
