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
from fusion import TEST


def fusion_(vis, ir):
    affine = np.array([[1.1541, 0.0179, -1.5489e-05],
                       [0.0300, 1.3006, 1.4895e-04],
                       [-69.2963, -68.5971, 1.0000]])
    affine = affine.T
    vis = cv2.warpPerspective(vis, affine, (vis.shape[1], vis.shape[0]))
    return vis



def fuse_img(img1_path, img2_path):
    # 读取中文路径下的图片
    img1 = cv2.imdecode(np.fromfile(img1_path, dtype=np.uint8), -1)
    img2 = cv2.imdecode(np.fromfile(img2_path, dtype=np.uint8), -1)

    img1 = fusion_(img1, img2)

    # 转换为灰度图
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) / 255
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) / 255
    # 若大小不一致，将图片缩放到一致
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # 图像融合
    img_fuse = TEST.inference(img1, img2) * 255
    # 返回融合后的图片
    return img_fuse


class FuseGUI:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('图像融合')
        self.window.setGeometry(100, 100, 1300, 600)
        self.rgb_image_path = ''
        self.ir_image_path = ''

        # add a label to show origin image
        self.label_sr_image = QLabel(self.window)
        self.set_image_label(self.label_sr_image, 110, 100, 320, 256)

        # add a label to show ir image
        self.label_ir_image = QLabel(self.window)
        self.set_image_label(self.label_ir_image, 510, 100, 320, 256)

        # add a label to show result image
        self.label_result_image = QLabel(self.window)
        self.set_image_label(self.label_result_image, 910, 100, 320, 256)

        # create a button about 可见光
        self.button_sr = QPushButton('选择可见光图像', self.window)
        self.set_button(self.button_sr, '选择可见光图像', 200, 400, 150, 30)
        self.button_sr.clicked.connect(
            lambda: self.show_img(
                QFileDialog.getOpenFileName(self.window, '选择可见光图像', './', 'Image Files(*.jpg *.png)')[0],
                                  self.label_sr_image, self.label_ir_image))

        # add a button to choose origin image
        self.button_choose_origin = QPushButton('选择红外图像', self.window)
        self.set_button(self.button_choose_origin, '选择红外图像', 600, 400, 150, 30)
        # self.button_choose_origin.clicked.connect(
        #     lambda: self.show_img(
        #         QFileDialog.getOpenFileName(self.window, '选择红外图像', './', 'Image Files(*.jpg *.png)')[0],
        #                           self.label_ir_image, 1))

        # add a button to choose origin image
        self.button_fuse = QPushButton('融合', self.window)
        self.set_button(self.button_fuse, '融合', 1000, 400, 150, 30)
        self.button_fuse.clicked.connect(lambda: self.show_result(self.label_result_image))

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

    def show_img(self, img_path, label1, label2,  size=(320, 256)):
        img = QPixmap(img_path)
        # 将path中的rgb换成ir
        ir_img_path = img_path.replace('rgb', 'ir')
        ir_img = QPixmap(ir_img_path)
        img = img.scaled(size[0], size[1])
        ir_img = ir_img.scaled(size[0], size[1])
        label1.setPixmap(img)
        label2.setPixmap(ir_img)
        self.rgb_image_path = img_path
        self.ir_image_path = ir_img_path

    def show_result(self, label):
        fuse = fuse_img(self.rgb_image_path, self.ir_image_path)
        cv2.imwrite('result.png', fuse)
        img = QPixmap('result.png')
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
    FuseGUI()
    # 删除临时的‘result.png’文件
    os.remove('result.png')



