import tensorflow as tf


class FuncApprox(object):
    def __init__(self):
        pass

    def train(self, _batch):
        pass

    def eval(self, _input):
        pass

    def save(self):
        pass


class MLP(FuncApprox):
    def __init__(self, sess, name, structure):
        FuncApprox.__init__(self)
        self.t = 0
        self.name = name
        self._sess = sess
        self.weights = {}
        with tf.variable_scope(name):
            self.setup(structure)

    def layer(self, input, kernel_shape, bias_shape):
        """
        Full-connected layer, might use tf.contrib.layers.fully_connected in the future
        :param input: input of layer
        :param kernel_shape: neural units shape
        :param bias_shape: bias shape
        :return: output tensor
        """
        weight = tf.get_variable("weight", kernel_shape, initializer=tf.random_normal_initializer())
        bias = tf.get_variable("bias", bias_shape, initializer=tf.constant_initializer(0.0))
        self.weights[weight.name.replace(self.name, "")] = weight
        self.weights[bias.name.replace(self.name, "")] = bias
        return tf.nn.relu(tf.add(tf.matmul(input, weight), bias))

    def setup(self, structure):
        learning_rate = 0.001

        n_input = structure[0]
        n_output = structure[-1]
        self.x = tf.placeholder(tf.float32, [None, n_input])
        self.y = tf.placeholder(tf.float32, [None, n_output])

        layers = [self.x]

        for i in range(len(structure) - 1):
            with tf.variable_scope('layer_%d' % i):
                layers.append(self.layer(layers[-1], [structure[i], structure[i + 1]], [structure[i + 1]]))

        self.pred = layers[-1]

        self.loss = tf.nn.l2_loss(self.pred - self.y)
        self.optimizer = tf.train.AdamOptimizer(learning_rate).minimize(self.loss)

    def train(self, _batch):
        batch_x, batch_y = _batch
        # Run optimization op (backprop) and cost op (to get loss value)
        _, c = self._sess.run([self.optimizer, self.loss], feed_dict={self.x: batch_x, self.y: batch_y})
        self.t += 1

    def eval(self, _input):
        return self.pred.eval({self.x: _input}, session=self._sess)

    def copy_to(self, network):
        copy_ops = []

        for name in self.weights.keys():
            copy_op = network.weights[name].assign(self.weights[name])
            copy_ops.append(copy_op)

        self.copy_op = tf.group(*copy_ops, name='copy_op')

    def run_copy(self):
        if self.copy_op is None:
            raise Exception("run `create_copy_op` first before copy")
        else:
            self._sess.run(self.copy_op)
