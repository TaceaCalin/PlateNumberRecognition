import onnx
import warnings
from onnx_tf.backend import prepare
import tensorflow as tf
import numpy as np


class NeuralNetwork:

    def importONNXModel(self, path):
        warnings.filterwarnings('ignore')
        model = onnx.load(path)
        tf_rep = prepare(model)
        return tf_rep

    def ExportONNXToGraphAsProtobuf(self, path, tf_rep):
        tf_rep.export_graph(path)

    def ImportGraphAsProtobuf(self, path):

        onnx_pb_graph = tf.Graph()
        with onnx_pb_graph.as_default():
            onnx_pb_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path, 'rb') as fid:
                serialized_graph = fid.read()
                onnx_pb_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(onnx_pb_graph_def, name='')
        return (onnx_pb_graph, onnx_pb_graph_def)

    def ReturnPredictionNumber(self, tf_rep, img):
        prediction = tf_rep.run(img)
        number = np.argmax(prediction)
        return prediction, number
