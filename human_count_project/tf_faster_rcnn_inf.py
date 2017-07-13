import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import traceback
import time

sys.path.append("/data/project/models/object_detection")
sys.path.append("/data/project/models")
from utils import label_map_util
from utils import visualization_utils as vis_util



def load_model_and_label_map(PATH_TO_CKPT, PATH_TO_LABELS, NUM_CLASSES):

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    detection_graph.as_default()
    sess = tf.Session(graph=detection_graph)
    #print "category_index",category_index

    return detection_graph, category_index ,sess

def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def detect(sess, detection_graph, category_index, TEST_IMAGE_PATHS):


    for image_path in TEST_IMAGE_PATHS:
        t1 = time.time()

        image = Image.open(image_path)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image_np = load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        scores = detection_graph.get_tensor_by_name('detection_scores:0')
        classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        # Actual detection.
        (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)

        Image.fromarray(image_np).save(image_path.replace('.jpg', '.rs.jpg'))
        # plt.figure(figsize=IMAGE_SIZE)
        # plt.imshow(image_np)
        # print boxes, classes, scores
        # print "shape", image_np.shape
        print "One pic time:", time.time() - t1

        return boxes, classes, scores, image_np.shape


if __name__ == '__main__':
    try:
        PATH_TO_CKPT = "/data/model_zoo/faster_rcnn_resnet101_coco_11_06_2017" + '/frozen_inference_graph.pb'
        # PATH_TO_CKPT = "/data/model_zoo/faster_rcnn_inception_resnet_v2_atrous_coco_11_06_2017" + '/frozen_inference_graph.pb'
        PATH_TO_LABELS = os.path.join('/data/model_zoo', 'mscoco_label_map.pbtxt')
        NUM_CLASSES = 90

        detection_graph, category_index, sess = load_model_and_label_map(PATH_TO_CKPT, PATH_TO_LABELS, NUM_CLASSES)
        print "model and label map loaded."

        TEST_IMAGE_PATHS = ["examples/B1001.src.jpg", "examples/original.src.jpg",
                            "examples/192.168.100.240_09_20161223171423352.mp40037.src.jpg"]
        detect(sess, detection_graph, category_index, TEST_IMAGE_PATHS)
    except:
        traceback.print_exc()

    #IMAGE_SIZE = (12, 8)