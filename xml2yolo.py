from xml.dom import minidom
import os
import glob

lut = {}
lut["without_mask"] = 0
lut["with_mask"] = 1
lut["mask_weared_incorrect"] = 2

def convert_coordinates(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_xml2yolo(lut):
    xml_files = glob.glob("E:/mask detection/annotations/*.xml")

    for xml_file in xml_files:
        xmldoc = minidom.parse(xml_file)
        txt_file = os.path.splitext(xml_file)[0] + '.txt'

        with open(txt_file, "w") as f:
            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                classid = (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    label_str = "-1"
                    print("Warning: Label '%s' not in look-up table" % classid)

                xmin = int(((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data)
                ymin = int(((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data)
                xmax = int(((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data)
                ymax = int(((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data)
                b = (xmin, xmax, ymin, ymax)
                bb = convert_coordinates((width, height), b)

                f.write(label_str + " " + " ".join([str(a) for a in bb]) + '\n')

        print("Converted %s to %s" % (xml_file, txt_file))

def main():
    convert_xml2yolo(lut)

if __name__ == '__main__':
    main()
