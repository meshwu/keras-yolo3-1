import xml.etree.ElementTree as ET
import glob

classes = ["forward", "backward"]

def convert_annotation(in_file_path, list_file):
    in_file = open(in_file_path)
    tree=ET.parse(in_file)
    root = tree.getroot()

    fname = root.find('filename').text
    list_file.write('dataset/images/'+fname)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), 
            int(float(xmlbox.find('ymin').text)), 
            int(float(xmlbox.find('xmax').text)), 
            int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
    list_file.write('\n')

with open('train.txt', 'w') as list_file:
    for in_file_path in glob.glob('dataset/anns/*.xml'):
        convert_annotation(in_file_path, list_file)

