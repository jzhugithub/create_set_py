import os
import cv2

def crop_images(dir, row_begin, row_end, col_begin, col_end, save=True, show=True, stop=False):

    cv2.namedWindow('src')
    cv2.namedWindow('dst')

    for root, dirs, files in os.walk(dir):
        for file in files:
            image_src = cv2.imread(os.path.join(root, file))
            image_dst = image_src[row_begin:row_end, col_begin:col_end, :]
            if show:
                cv2.imshow('src',image_src)
                cv2.imshow('dst',image_dst)
                if stop:
                    cv2.waitKey(0)
                else:
                    cv2.waitKey(1)
            if save:
                cv2.imwrite(os.path.join(root, file)[:-4] + '_s.jpg',image_dst)


if __name__ == '__main__':
    crop_images('image_select', 60, 1020, 420, 1380, save=False, show=True, stop=True)