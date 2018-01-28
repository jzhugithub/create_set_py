#! /usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import cv2
import os


def run(video_path, out_folder_path, label, frame_interval, auto_mode):
    img_count = 1
    tmp_char = 'n'
    my_video = cv2.VideoCapture(video_path)

    if not my_video.isOpened():
        print('video open error')
        return
    else:
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        while True:
            success, src = my_video.read()
            if not success:
                break
            cv2.imshow('img', src)

            stop = False
            while (not stop):

                if auto_mode:
                    cv2.waitKey(1)

                    if tmp_char == 'n':
                        n = 's'
                        tmp_char = 's'
                    else:
                        n = 'n'
                        tmp_char = 'n'
                else:
                    n = chr(cv2.waitKey(0))

                if n == 'n' or n == 'N':
                    for i in range(0, int(frame_interval)):
                        if not my_video.read()[0]:
                            break
                    stop = True
                elif n == 's' or n == 'S':
                    cv2.imwrite(os.path.join(out_folder_path, label + str(img_count) + '.jpg'), src)
                    print(label + str(img_count) + '.jpg')
                    img_count += 1
                elif (n >= 'a' and n <= 'z') or (n >= 'A' and n <= 'Z'):
                    stop = True
                    return


if __name__ == '__main__':
    print('n: next frame')
    print('s: select this frame')
    print('other letter: exit')

    video_path = '/home/zj/database/fisheye_data/video/out_fisheye01194.avi'
    out_folder_path = '/home/zj/my_workspace/create_set_py/image_select'
    label = 'out_fisheye01194_'
    frame_interval = 3

    run(video_path, out_folder_path, label, frame_interval, True)
