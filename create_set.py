import cv2
import numpy as np
import os


class CreatSet(object):
    frame_interval = 1
    folder_path = ''

    org = np.array([])
    img = np.array([])
    tmp = np.array([])
    widthHeightRatio = 1.0
    orgName = ''

    pre_pt = np.zeros(2, np.int32)
    end_pt = np.zeros(2, np.int32)
    cur_pt = np.zeros(2, np.int32)

    count = 1

    def __init__(self, orgName, frame_interval, folder_path):
        self.orgName = orgName
        self.frame_interval = frame_interval
        self.folder_path = folder_path
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

    def on_mouse(self, event, x, y, flags, param):
        self.cur_pt = np.array([x, y], np.int32)
        self.tmp = np.array(self.img)
        if (event == cv2.EVENT_MOUSEMOVE and (not (flags & cv2.EVENT_FLAG_LBUTTON))):
            pass
        if event == cv2.EVENT_LBUTTONDOWN:
            self.pre_pt = np.array([x, y], np.int32)
        if (event == cv2.EVENT_MOUSEMOVE) and (flags & cv2.EVENT_FLAG_LBUTTON):
            self.end_pt[0] = self.cur_pt[0]
            self.end_pt[1] = int(self.pre_pt[1] + (self.cur_pt[0] - self.pre_pt[0]) / self.widthHeightRatio)
            cv2.rectangle(self.tmp, tuple(self.pre_pt), tuple(self.end_pt), (0, 255, 0))
        if event == cv2.EVENT_LBUTTONUP:
            cv2.rectangle(self.img, tuple(self.pre_pt), tuple(self.end_pt), (0, 255, 0))
            cv2.imwrite(os.path.join(self.folder_path, self.orgName + '0.jpg'), self.img)
            outImg = self.org[self.pre_pt[1]:self.end_pt[1], self.pre_pt[0]:self.end_pt[0], :]
            if outImg.shape[0] > 0 and outImg.shape[1] > 0:
                cv2.imwrite(os.path.join(self.folder_path, self.orgName + str(self.count) + '.jpg'), outImg)
            self.count += 1
        cv2.putText(self.tmp, '%s, %s' % (x, y), tuple(self.cur_pt), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, 30)
        cv2.imshow('img', self.tmp)

    def run(self):
        cap = cv2.VideoCapture(self.orgName + '.avi')
        if not cap.isOpened():
            print('read video error')
            return

        while (True):
            success, self.org = cap.read()
            if not success:
                break
            self.img = np.array(self.org)
            # cv2.namedWindow("img", cv2.WINDOW_NORMAL)
            cv2.namedWindow("img")
            cv2.setMouseCallback('img', self.on_mouse, 0)
            cv2.imshow('img', self.img)

            stop = False
            while (not stop):
                n = chr(cv2.waitKey(0))
                if n == 'n' or n == 'N':
                    for i in range(0, int(self.frame_interval)):
                        if not cap.read()[0]:
                            break
                    stop = True
                elif (n >= 'a' and n <= 'z') or (n >= 'A' and n <= 'Z'):
                    stop = True
                    return


if __name__ == '__main__':
    cs = CreatSet('fisheye', 10, 'images')
    cs.run()
