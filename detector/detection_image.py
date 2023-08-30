import os
from math import ceil
import cv2
import numpy as np
from numpy import ndarray


class DoorDetector:
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "yolo-door.cfg")
    WEIGHTS_FILE_PATH = os.path.join(os.path.dirname(__file__), "yolo-door.weights")
    DOOR_CLASS = 0

    def __init__(self, vid_source=0):
        video = cv2.VideoCapture(vid_source)
        is_ok, frame = video.read()
        if is_ok:
            self.image = frame

    def detect_all_doors(self):
        doors = []
        width = self.image.shape[1]
        height = self.image.shape[0]
        scale = 0.00392  # this is 1/255
        net = cv2.dnn.readNet(self.WEIGHTS_FILE_PATH, self.CONFIG_FILE_PATH)
        blob = cv2.dnn.blobFromImage(self.image, scale, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(self._get_output_layers(net))
        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # After detecting the whole image, try to crop square subimage and do further detection
        sub_image_list = self._split_image()
        for s in sub_image_list:
            sub_image = self.image[s[1]:s[1] + s[3], s[0]:s[0] + s[2]]
            blob = cv2.dnn.blobFromImage(sub_image, scale, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(self._get_output_layers(net))

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * s[2]) + s[0]
                        center_y = int(detection[1] * s[3]) + s[1]
                        w = int(detection[2] * s[2])
                        h = int(detection[3] * s[3])
                        x = center_x - w / 2
                        y = center_y - h / 2
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        for i in indices:
            box = boxes[i]
            if not class_ids[i]:
                x = box[0]
                y = box[1]
                w = box[2]
                h = box[3]
                doors.append((round(x + w / 10), round(y + h / 10), round(w - w / 20)))
                # add_red_point(self.image, (round(x + w / 10), round(y + h / 10)))
        return doors

    @staticmethod
    def _get_output_layers(net):
        layer_names = net.getLayerNames()

        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers

    def _split_image(self):
        width = self.image.shape[1]
        height = self.image.shape[0]
        result = []

        if width > height:
            n_image = ceil(width / height * 2)
            left = 0
            for i in range(n_image):
                if left + height > width:
                    left = width - height
                result.append((left, 0, height, height))
                left += int(height / 2)
        else:
            n_image = ceil(height / width * 2)
            top = 0
            for i in range(n_image):
                if top + width > height:
                    top = height - width
                result.append((0, top, width, width))
                top += int(width / 2)
        return result


def add_red_point(img, *coordinates):
    """
    for testing purpose - draw red points on the given coordinates
    """
    print(coordinates)
    # Load the image
    # img = cv2.imread(image_path)

    if img is None:
        print("Image not found or unable to load.")
        return
    for tup in coordinates:
        # Convert coordinates to integers
        x, y = map(int, tup)

        # Draw a red point at the specified coordinates
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)  # -1 fills the circle

    # Display the image with the added point
    cv2.imshow("Image with Red Point", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



