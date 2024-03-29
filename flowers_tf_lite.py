#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#Original code can be found at
#https://colab.research.google.com/github/tensorflow/examples/blob/master/community/en/flowers_tf_lite.ipynb#scrollTo=aCLb_yV5JfF3

import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt

IMAGE_SIZE = 224
BATCH_SIZE = 64

def download_flower_dataset():
    _URL = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
    zip_file = tf.keras.utils.get_file(origin=_URL,
                                        fname="flower_photos.tgz",
                                        extract=True)
    return os.path.join(os.path.dirname(zip_file), 'flower_photos')


def create_image_batch_generator(base_dir):
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2)

    train_generator = datagen.flow_from_directory(
        base_dir,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        subset='training')

    val_generator = datagen.flow_from_directory(
        base_dir,
        target_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
        subset='validation')
    
    return train_generator, val_generator

 
def save_labels(train_generator):
    for image_batch, label_batch in train_generator:
        break

    print(image_batch.shape, label_batch.shape)
    print (train_generator.class_indices)

    labels = '\n'.join(sorted(train_generator.class_indices.keys()))

    with open('labels.txt', 'w') as f:
        f.write(labels)


def download_mobilenet_v2_model():
    # Create the base model from the pre-trained model MobileNet V2
    IMG_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                include_top=False,
                                                weights='imagenet')

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.Conv2D(32, 3, activation='relu'),
        tf.keras.layers.Dropout(0.2), 
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(5, activation='softmax')
    ])

    # Let's take a look to see how many layers are in the base model
    print("Number of layers in the base model: ", len(base_model.layers))

    return base_model, model

def run_transfer_learning(base_model, model, train_generator, val_generator):
    base_model.trainable = False
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                loss='categorical_crossentropy',
                metrics=['accuracy'])

    model.summary()
    print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

    epochs = 10
    history = model.fit(train_generator,
                        epochs=epochs,
                        validation_data=val_generator)
    return history

def run_fine_tuning(base_model, model, train_generator, val_generator):
    base_model.trainable = True
    # Fine tune from this layer onwards
    fine_tune_at = 100

    # Freeze all the layers before the `fine_tune_at` layer
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable =  False

    model.compile(loss='categorical_crossentropy',
                optimizer = tf.keras.optimizers.Adam(1e-5),
                metrics=['accuracy'])
    model.summary()

    print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

    history = model.fit(train_generator,
                            epochs=5,
                            validation_data=val_generator)
    return history

def save_model_as_tflite(model):
    saved_model_dir = 'fine_tuning'

    tf.saved_model.save(model, saved_model_dir)
    converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    tflite_model = converter.convert()

    with open('model.tflite', 'wb') as f:
        f.write(tflite_model)

def plot_figure(history, fig_name):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']

    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Training Accuracy')
    plt.plot(val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.ylabel('Accuracy')
    plt.ylim([min(plt.ylim()),1])
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Training Loss')
    plt.plot(val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.ylabel('Cross Entropy')
    plt.ylim([0,1.0])
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.show()
    plt.savefig(fig_name)
    
if __name__ == '__main__':
    print(tf.__version__)
    base_dir = download_flower_dataset()
    train_generator, val_generator = create_image_batch_generator(base_dir)
    save_labels(train_generator)

    base_model, model = download_mobilenet_v2_model() #download without top layer and add top layer 

    history = run_transfer_learning(base_model, model, train_generator, val_generator)
    plot_figure(history, 'transfer_learning.png')

    history_fine = run_fine_tuning(base_model, model, train_generator, val_generator)
    save_model_as_tflite(model)
    plot_figure(history_fine, 'fine_tuning.png')

