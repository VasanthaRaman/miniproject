import tensorflow as tf
from tensorflow.python.platform import gfile

f=gfile.FastGFile("./model/tf_model.pb",'rb')
graph_def=tf.GraphDef()
graph_def.ParseFromString(f.read())
f.close()

sess.graph.as_default()
tf.import_graph_def(graph_def)