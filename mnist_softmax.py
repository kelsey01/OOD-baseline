import os
import tensorflow as tf
import numpy as np
import experiments as exp
from tensorflow import keras


# Define simple model. execution starts from the bottom
def basic_mnist_model():

    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(256, activation=tf.nn.relu),

        keras.layers.BatchNormalization(),
        keras.layers.Dense(256, activation=tf.nn.relu),

        keras.layers.BatchNormalization(),
        keras.layers.Dense(256, activation=tf.nn.relu),

        keras.layers.BatchNormalization(),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    return model


# Load MNIST, FMNIST dataset
mnist = keras.datasets.mnist
(mnist_train_x, mnist_train_y), (mnist_test_x, mnist_test_y)\
    = mnist.load_data()
mnist_train_x, mnist_test_x = mnist_train_x/255., mnist_test_x/255.

fashion_mnist = keras.datasets.fashion_mnist
(fmnist_train_x, fmnist_train_y), (fmnist_test_x, fmnist_test_y)\
    = fashion_mnist.load_data()
fmnist_train_x, fmnist_test_x = fmnist_train_x/255., fmnist_test_x/255.

# Train model if no pre-trained model exists
saved_model_path = './mnist.hdf5'
if not os.path.exists(saved_model_path):

    model = basic_mnist_model()

    # TRAIN MODEL
    training_epochs = 10
    learning_rate = 0.001
    batch_size = 128

    model.compile(optimizer=keras.optimizers.Adam(lr=learning_rate),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(mnist_train_x, mnist_train_y,
              epochs=training_epochs,
              batch_size=batch_size)

    test_loss, test_acc = model.evaluate(mnist_test_x, mnist_test_y)
    print("Training done, test accuracy: {}".format(test_acc))

    # SAVE MODEL
    keras.models.save_model(model, "./mnist.hdf5")

else:
    model = keras.models.load_model(saved_model_path)

# right/wrong distinction, regard wrong examples as negative
exp.right_wrong_distinction(model, mnist_test_x, mnist_test_y)

# In-Out-of-distribution test, assumes out-of-distribution samples as negative
exp.in_out_distinction(model,
                       mnist_test_x,
                       fmnist_test_x,
                       "FashionMNIST")

exp.in_out_distinction(model,
                       mnist_test_x,
                       np.random.normal(size=(10000, 28, 28)),
                       "WhiteNoise")

exp.in_out_distinction(model,
                       mnist_test_x,
                       np.random.uniform(size=(10000, 28, 28)),
                       "UniformNoise")