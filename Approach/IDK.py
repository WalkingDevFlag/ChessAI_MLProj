import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
import

# Load data from .npz files
data = np.load('C:\\Users\\Lenovo\\Desktop\\Chess AI\\all_board_states.npz')
board_states = data['data']

data = np.load('C:\\Users\\Lenovo\\Desktop\\Chess AI\\board_evaluation.npz')
board_evaluations = data['data']

data = np.load('C:\\Users\\Lenovo\\Desktop\\Chess AI\\move_rep.npz')
move_reps = data['data']

data = np.load('C:\\Users\\Lenovo\\Desktop\\Chess AI\\rep_layer.npz')
rep_layers = data['data']

# Check shapes of loaded data
print("Shapes of loaded data:")
print("Board states:", board_states.shape)
print("Board evaluations:", board_evaluations.shape)
print("Move representations:", move_reps.shape)
print("Representation layers:", rep_layers.shape)

board_states_train, board_states_val, board_evaluations_train, board_evaluations_val = train_test_split(
    board_states, board_evaluations, test_size=0.1, random_state=42)

move_reps_train, move_reps_val = train_test_split(move_reps, test_size=0.1, random_state=42)

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
        # Define your model architecture here
        self.conv1 = tf.keras.layers.Conv2D(256, 3, padding='same', activation='relu')
        self.res_blocks = [ResidualBlock(256, 3) for _ in range(19)]
        self.policy_conv = tf.keras.layers.Conv2D(2, 1, padding='same', activation='relu', data_format='channels_last')
        self.policy_output = tf.keras.layers.Conv2D(2, 1, padding='same', activation='softmax', data_format='channels_last')

        self.value_conv = tf.keras.layers.Conv2D(1, 1, padding='same', activation='relu')
        self.value_flatten = tf.keras.layers.Flatten()
        self.value_dense1 = tf.keras.layers.Dense(256, activation='relu')
        self.value_output = tf.keras.layers.Dense(1, activation='tanh')

    def call(self, inputs):
        x = self.conv1(inputs)
        for block in self.res_blocks:
            x = block(x)
        policy = self.policy_output(self.policy_conv(x))
        value = self.value_output(self.value_dense1(self.value_flatten(self.value_conv(x))))
        return policy, value

    def train_step(self, data):
        inputs, targets = data
        with tf.GradientTape() as tape:
            policy, value = self(inputs, training=True)
            # No need to reshape or one-hot encode policy targets
            policy_loss = tf.keras.losses.CategoricalCrossentropy()(tf.one_hot(tf.cast(targets['policy'], tf.uint8), depth=2), policy)
            value_loss = tf.keras.losses.MeanSquaredError()(targets['value'], value)
            total_loss = policy_loss + value_loss
        gradients = tape.gradient(total_loss, self.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.trainable_variables))
        return {'total_loss': total_loss, 'policy_loss': policy_loss, 'value_loss': value_loss}

# Instantiate model
model = AlphaZeroChessModel()

# Compile model
model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss={'policy': 'categorical_crossentropy', 'value': 'mse'})

# Check shapes of training and validation data
print("Shapes of training data:")
print("Board states train:", board_states_train.shape)
print("Board evaluations train:", board_evaluations_train.shape)
print("Move representations train:", move_reps_train.shape)

print("\nShapes of validation data:")
print("Board states val:", board_states_val.shape)
print("Board evaluations val:", board_evaluations_val.shape)
print("Move representations val:", move_reps_val.shape)


# Train model
history = model.fit(x=board_states_train, y={'policy': move_reps_train, 'value': board_evaluations_train},
                    validation_data=(board_states_val, {'policy': move_reps_val, 'value': board_evaluations_val}),
                    batch_size=32, epochs=10)

model.save('chess_model.h5')
