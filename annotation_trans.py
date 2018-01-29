# -*-coding:utf-8-*-
from __future__ import print_function
import json
import os
from xml.dom.minidom import Document


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


def main():
    json_dict = '/home/zj/database_temp/fisheye2_data_set/annotations_labelme'
    image_dict = '/home/zj/database_temp/fisheye2_data_set/images'
    image_size = [960, 960]
    for root, dirs, files in os.walk(json_dict):
        for json_name in files:
            print('trans {}'.format(json_name))
            json_path = os.path.join(json_dict, json_name)
            image_path = os.path.join(image_dict, json_name[:-5] + '.jpg')
            shapes, labels = get_shapes_labels(json_path, ['ir', 'ob'])
            bboxs = get_bboxs(shapes)
            get_xml(image_path, image_size, labels, bboxs)


if __name__ == '__main__':
    main()
