import cv2
import os


def run(video_path, out_folder_path, label, frame_interval):
    img_count = 1
    my_video = cv2.VideoCapture(video_path)

    if not my_video.isOpened():
        print('video open error')
        return
    else:
        cv2.namedWindow("img")
        while True:
            success, src = my_video.read()
            if not success:
                break
            cv2.imshow('img', src)

            stop = False
            while (not stop):
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
    video_path = '/home/zj/database/zmart_data/video/fisheye.avi'
    out_folder_path = '/home/zj/my_workspace/test/image_out'
    label = 'fisheye'
    frame_interval = 10

    run(video_path, out_folder_path, label, frame_interval)
