import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PyQt5 import QtWidgets as widgets
from matplotlib import pyplot as plt
Ui_MainWindow = __import__("interface").Ui_MainWindow

model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

content_folder = './content'
content_image_name = 'ben_meditation.jpg'
style_folder = './styles'
style_image_name = 'waves.jpg'

def load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img

try:
  content_image = load_image(content_folder + '/' + content_image_name)
except:
  print("There was a problem with the content image file you selected. Please choose a BMP, GIF, JPEG, or PNG image file and try again.")
try:
  style_image = load_image(style_folder + '/' + style_image_name)
except:
  print("There was a problem with the style image file you selected. Please choose a BMP, GIF, JPEG, or PNG image file and try again.")

content_image.shape

plt.imshow(np.squeeze(content_image))
plt.show()
plt.imshow(np.squeeze(style_image))
plt.show()

stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]
plt.imshow(np.squeeze(stylized_image))
plt.show()

try:
    saved = cv2.imwrite('/content/gdrive/MyDrive/style_transfer/ben_styled_waves.jpg', cv2.cvtColor(np.squeeze(stylized_image)*255, cv2.COLOR_BGR2RGB))
except:
    saved = False
if saved:
    print("File saved")
else:
    print("Something went wrong. Please check the folder and file name then try again.")

if __name__ == "__main__":
    import sys
    app = widgets.QApplication(sys.argv)
    MainWindow = widgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())