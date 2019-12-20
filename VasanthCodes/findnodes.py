import tensorflow as tf
sess = tf.Session()
graph = tf.get_default_graph()
with graph.as_default():
    with sess.as_default():
#        #restoring the model
        saver = tf.train.import_meta_graph(r"C:\Users\Internship005\output_inference_graph_v1.pb\model.ckpt.meta")
        saver.restore(sess,tf.train.latest_checkpoint(r'C:\Users\Internship005\output_inference_graph_v1.pb\./'))

#import tensorflow as tf
#gf = tf.GraphDef()
#gf.ParseFromString(open(r"C:\Users\Internship005\output_inference_graph_v1.pb\frozen_inference_graph.pb",'rb').read()) 
#[n.name + '=>' +  n.op for n in gf.node if n.op in ( 'Softmax','Placeholder')]

 #initializing all variables
        sess.run(tf.global_variables_initializer())
       
        #using the model for prediction
        x_tensor = graph.get_tensor_by_name("inputTensor:0")
        #keep_prob is not always necessary it depends on your model
        keep_prob = graph.get_tensor_by_name("dropout_keep_prob:0")
        op_to_restore = graph.get_tensor_by_name("output/softmax:0")
        feed_dict={x_tensor: x_test,  keep_prob: 1.0}
        
        opt = []
        
        opt = sess.run(op_to_restore ,feed_dict)
        
        y_test = np.asarray(y_test)# converting list to numpy array
        labels=np.argmax(y_test, 1)
        predictions=np.argmax(opt,1)
        count =  np.sum(labels == predictions)
        print("Number of correct prediction %d out of %d"%(count,len(predictions)))
        print("Accuracy is {:.3f}". format(float(count)/len(predictions)))
