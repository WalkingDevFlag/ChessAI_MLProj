import tensorflow as tf

'''
1. Contains the definition of a neural network model for the AlphaZero chess algorithm.

2. Defines a residual block layer and the main AlphaZeroChessModel model.

3. Implements the model's architecture, including convolutional layers, residual blocks, and output layers.

4. Provides methods for model training and prediction
'''
    
class ResidualBlock(tf.keras.layers.Layer):
    def __init__(self, filters, kernel_size):
        super(ResidualBlock, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(filters, kernel_size, padding='same', activation='relu')
        self.conv2 = tf.keras.layers.Conv2D(filters, kernel_size, padding='same', activation='linear')

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        return tf.keras.layers.add([inputs, x])

class AlphaZeroChessModel(tf.keras.Model):
    def __init__(self):
        super(AlphaZeroChessModel, self).__init__()
        # Define input layer separately
        self.input_layer = tf.keras.layers.InputLayer(input_shape=(8, 8, 17))

        # Convolutional layers
        self.conv1 = tf.keras.layers.Conv2D(256, 3, padding='same', activation='relu')
        self.res_blocks = [ResidualBlock(256, 3) for _ in range(19)]
        self.policy_conv = tf.keras.layers.Conv2D(2, 1, padding='same', activation='relu')
        self.policy_flatten = tf.keras.layers.Flatten()
        self.policy_output = tf.keras.layers.Dense(4096, activation='softmax')

        self.value_conv = tf.keras.layers.Conv2D(1, 1, padding='same', activation='relu')
        self.value_flatten = tf.keras.layers.Flatten()
        self.value_dense1 = tf.keras.layers.Dense(256, activation='relu')
        self.value_output = tf.keras.layers.Dense(1, activation='tanh')

    def call(self, inputs):
        x = self.input_layer(inputs)  # Pass input through input layer
        x = self.conv1(x)
        for block in self.res_blocks:
            x = block(x)
        policy = self.policy_output(self.policy_flatten(self.policy_conv(x)))
        value = self.value_output(self.value_dense1(self.value_flatten(self.value_conv(x))))
        return policy, value
    
    def forward(self, x):
        x_input = tf.identity(x)
        x = self.conv1(x)
        for block in self.res_blocks:
            x = block(x)
        x = self.policy_output(self.policy_flatten(self.policy_conv(x)))
        x_input = self.value_output(self.value_dense1(self.value_flatten(self.value_conv(x_input))))
        x = x + x_input
        return tf.keras.activations.relu(x)
    
    def train_step(self, data):
        inputs, targets = data
        with tf.GradientTape() as tape:
            policy, value = self(inputs, training=True)
            policy_loss = tf.keras.losses.CategoricalCrossentropy()(targets['policy'], policy)
            value_loss = tf.keras.losses.MeanSquaredError()(targets['value'], value)
            total_loss = policy_loss + value_loss
        gradients = tape.gradient(total_loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))
        return {'total_loss': total_loss, 'policy_loss': policy_loss, 'value_loss': value_loss}

    def train(self, states, policies, values, batch_size=32, epochs=1):
        dataset = tf.data.Dataset.from_tensor_slices((states, {'policy': policies, 'value': values}))
        dataset = dataset.shuffle(buffer_size=10000).batch(batch_size)
        self.compile(optimizer=tf.keras.optimizers.Adam())
        self.fit(dataset, epochs=epochs)
