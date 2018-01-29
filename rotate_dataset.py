# -*-coding:utf-8-*-
from __future__ import print_function
import json
import os
from xml.dom.minidom import Document
from math import atan2, sqrt, cos, sin, pi
import cv2

def get_shapes_labels(json_file, label_list_check):
    with open(json_file) as f:
        fdict = json.load(f)
    shapes = []
    labels = []
    for item in fdict['shapes']:
        if item['label'] in label_list_check:
            shapes.append(item['points'])
            labels.append(item['label'])
        else:
            print('label error: {}'.format(item['label']))
    return shapes, labels


def get_bbox(points):
    xlist = []
    ylist = []
    for point in points:
        xlist.append(int(point[0]))
        ylist.append(int(point[1]))
    xlist.sort()
    ylist.sort()
    xmin = xlist[0]
    xmax = xlist[-1]
    ymin = ylist[0]
    ymax = ylist[-1]
    return xmin, ymin, xmax, ymax


def get_bboxs(shapes):
    bboxs = []
    for shape in shapes:
        bboxs.append(get_bbox(shape))
    return bboxs


def add_element(doc, root, name, content):
    element = doc.createElement(name)
    element_text = doc.createTextNode(str(content))
    element.appendChild(element_text)
    root.appendChild(element)


def get_xml(image_path, image_size, labels, bboxs):
    image_path_split = image_path.split('/')
    image_name = image_path_split[-1]
    image_folder = image_path_split[-2]
    xml_path = image_path[:-4] + '.xml'

    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    add_element(doc, annotation, 'folder', image_folder)
    add_element(doc, annotation, 'filename', image_name)
    add_element(doc, annotation, 'path', image_path)

    source = doc.createElement('source')
    annotation.appendChild(source)
    add_element(doc, source, 'database', 'Unknown')

    size = doc.createElement('size')
    annotation.appendChild(size)
    add_element(doc, size, 'width', image_size[0])
    add_element(doc, size, 'height', image_size[1])
    add_element(doc, size, 'depth', 3)

    add_element(doc, annotation, 'segmented', 0)

    for label, bbox in zip(labels, bboxs):
        object = doc.createElement('object')
        annotation.appendChild(object)
        add_element(doc, object, 'name', label)
        add_element(doc, object, 'pose', 'Unspecified')
        add_element(doc, object, 'truncated', 0)
        add_element(doc, object, 'difficult', 0)

        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        add_element(doc, bndbox, 'xmin', bbox[0])
        add_element(doc, bndbox, 'ymin', bbox[1])
        add_element(doc, bndbox, 'xmax', bbox[2])
        add_element(doc, bndbox, 'ymax', bbox[3])

    with open(xml_path, 'w') as f:
        doc.writexml(f, addindent='    ', newl='\n')


def rotate_shapes(shapes, angle, center):
    shapes_rot = []
    for shape in shapes:
        shape_rot = []
        for point in shape:
            vector = [point[0] - center[0], point[1] - center[1]]
            direct = atan2(vector[1], vector[0])
            direct_rot = direct - angle
            length = sqrt(vector[0]**2 + vector[1]**2)
            point_rot = [center[0] + length * cos(direct_rot), center[1] + length * sin(direct_rot)]
            shape_rot.append(point_rot)
        shapes_rot.append(shape_rot)
    return shapes_rot


def rotate_image(in_path, out_path, angle):
    img = cv2.imread(in_path)
    rows, cols, channel = img.shape

    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(out_path,dst)


def main(angle_du):
    # angle_du = 75.0
    angle = angle_du / 180.0 * pi
    json_dict = '/home/zj/database_temp/fisheye2_data_set/train/annotations_labelme'
    image_dict = '/home/zj/database_temp/fisheye2_data_set/train/images'
    image_rot_dict = '/home/zj/database_temp/fisheye2_data_set/train/images' + str(int(angle_du))
    if not os.path.exists(image_rot_dict):
        os.mkdir(image_rot_dict)
    image_size = [960, 960]
    label_list_check = ['ir', 'ob']

    for root, dirs, files in os.walk(json_dict):
        for json_name in files:
            print('convert {}'.format(json_name))
            json_path = os.path.join(json_dict, json_name)
            image_path = os.path.join(image_dict, json_name[:-5] + '.jpg')
            image_rot_path = os.path.join(image_rot_dict, json_name[:-5] + str(int(angle_du)) + '.jpg')
            rotate_image(image_path, image_rot_path, angle_du)
            shapes, labels = get_shapes_labels(json_path, label_list_check)
            shapes_rot = rotate_shapes(shapes, angle, [(image_size[0] - 1) / 2.0, (image_size[1] - 1) / 2.0])
            bboxs_rot = get_bboxs(shapes_rot)
            get_xml(image_rot_path, image_size, labels, bboxs_rot)


if __name__ == '__main__':
    main(15.0)
    main(30.0)
    main(45.0)
    main(60.0)
    main(75.0)
