#converting the xml format to yolo format

import os
import xml.etree.ElementTree as ET

def convert_to_yolo(xml_folder, output_folder, classes):
    # Get a list of XML file paths
    xml_paths = [os.path.join(xml_folder, file) for file in os.listdir(xml_folder) if file.lower().endswith('.xml')]

    # Iterate through each XML file
    for xml_path in xml_paths:
        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Get image width and height
        width = float(root.find(".//size/width").text)
        height = float(root.find(".//size/height").text)

        # Create a YOLO format string
        yolo_format = ""

        # Iterate through each object in the XML
        for obj in root.findall(".//object"):
            name = obj.find("name").text
            class_id = classes.index(name)
            xmin = float(obj.find(".//bndbox/xmin").text)
            ymin = float(obj.find(".//bndbox/ymin").text)
            xmax = float(obj.find(".//bndbox/xmax").text)
            ymax = float(obj.find(".//bndbox/ymax").text)

            # Convert coordinates to YOLO format (normalized)
            x_center = (xmin + xmax) / (2 * width)
            y_center = (ymin + ymax) / (2 * height)
            box_width = (xmax - xmin) / width
            box_height = (ymax - ymin) / height

            # Add to YOLO format string
            yolo_format += f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n"

        # Write YOLO format to a new file
        output_path = os.path.join(output_folder, os.path.splitext(os.path.basename(xml_path))[0] + ".txt")
        with open(output_path, "w") as output_file:
            output_file.write(yolo_format)

# Example usage
xml_folder = "F:/Raghav/traffic_sign_detection/dataset/labels"
output_folder = "F:/Raghav/traffic_sign_detection/annotations"
classes = ["traffic_sign"]  # Replace with your class names

convert_to_yolo(xml_folder, output_folder, classes)