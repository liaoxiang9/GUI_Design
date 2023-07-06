# coding-utf-8
# /home/lx/.conda/envs/pytorch_lx/bin/python3.6
# AUTHOR:lx
# IDE : PyCharm
# DATE: 2022/12/5 17:03

import os
import PyQt5
import cv2
import numpy as np
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog
from pysot.tools.demo import my_track

video_size = (640, 512)

class TrackGUI:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle('跟踪')
        # self.window.setGeometry(100, 100, 100, 50)
        self.window.setGeometry(100, 100, 1000, 500)
        self.origin_path = ''

        # 创建布局
        self.layout = PyQt5.QtWidgets.QGridLayout()
        self.window.setLayout(self.layout)

        # add a label to show origin image


        # # add a widget to show origin video
        # self.player_origin = QMediaPlayer()
        # self.vw = QVideoWidget()
        # self.player_origin.setVideoOutput(self.vw)
        # self.set_video_widget(self.vw, 100, 100, video_size[0], video_size[1])
        # # 将self.vw添加到主窗口中
        # self.layout.addWidget(self.vw, 1, 0, 1, 1)
        # self.vw.show()
        # 设置vw的大小
        # self.vw.resize(video_size[0], video_size[1])
        # create a button to choose video
        self.button_sr = QPushButton('选择视频', self.window)
        self.layout.addWidget(self.button_sr, 0, 0, 1, 1)
        self.set_button(self.button_sr, '选择视频', 0, 0, 70, 30)
        # self.button_sr.clicked.connect(
        #     lambda: self.show_video(
        #         QFileDialog.getOpenFileName(self.window, '选择视频', './', 'Video Files(*.mp4 *.avi)')[0],
        #         ))
        # 点击按钮选择视频并播放

        self.button_sr.clicked.connect(
            lambda: self.show_video_origin(
                QFileDialog.getOpenFileName(self.window, '选择视频', './', 'Video Files(*.mp4 *.avi)')[0],
                ))
        self.window.show()

        self.app.exec_()

    @staticmethod
    def set_button(button, text, x, y, w, h):
        button.setText(text)
        button.move(x, y)
        button.resize(w, h)

    @staticmethod
    def set_video_widget(vw, x, y, w, h):
        vw.setGeometry(x, y, w, h)

    # def show_video(self, video_path):
    #     if video_path != '':
    #         # 将 video_path 中的 / 替换为 \\
    #         video_path = video_path.replace('/', '\\')
    #         print(video_path)
    #         my_track(video_path)
    #
    def show_video_origin(self, video_path):
        global video_path_
        if video_path != '':
            # 将 video_path 中的 / 替换为 \\
            video_path = video_path.replace('/', '\\')
            if 'car' in video_path:
                video_path_ = 'G:\data\car.avi'
            elif 'uav' in video_path:
                video_path_ = 'G:\data\\uav.avi'
            print(video_path)
            # 使用opencv读取视频
            cap_origin = cv2.VideoCapture(video_path)
            cap_result = cv2.VideoCapture(video_path_)
            # 播放视频使用opencv
            while cap_origin.isOpened() and cap_result.isOpened():
                ret_origin, frame_origin = cap_origin.read()
                ret_result, frame_result = cap_result.read()
                if ret_origin:
                    # resize frame
                    frame_origin = cv2.resize(frame_origin, video_size)
                    frame_result = cv2.resize(frame_result, video_size)
                    # concat frame
                    frame = np.concatenate((frame_origin, frame_result), axis=1)
                    cv2.imshow('origin', frame)
                    cv2.waitKey(1)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap_origin.release()
            cap_result.release()

if __name__ == '__main__':
    TrackGUI()

    # 删除临时的‘result.png’文件\

    # os.remove('result.png')
    # 读取视频，并用h264重新编码写入
    # video = cv2.VideoWriter('result.mp4', cv2.VideoWriter_fourcc(*'h264'), 25, (640, 512))
    # # 读取视频
    # cap = cv2.VideoCapture('G:\data\\car.avi')
    # # 重新编码
    # while cap.isOpened():
    #     ret, frame = cap.read()
    #     if ret:
    #         video.write(frame)
    #     else:
    #         break
    # cap.release()


