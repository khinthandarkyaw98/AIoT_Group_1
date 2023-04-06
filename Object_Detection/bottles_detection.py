# -*- coding: utf-8 -*-
"""bottles_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wZ_dKPqKXUCNT_bdk5GjUZ8t4IjWFjmB

# Configuring cuDNN on Colab for YOLOv4
"""

# CUDA: Let's check that Nvidia CUDA drivers are already pre-installed and which version is it.
!/usr/local/cuda/bin/nvcc --version
# We need to install the correct cuDNN according to this output

#take a look at the kind of GPU we have
!nvidia-smi

# This cell ensures you have the correct architecture for your respective GPU
# If you command is not found, look through these GPUs, find the respective
# GPU and add them to the archTypes dictionary

# Tesla V100
# ARCH= -gencode arch=compute_70,code=[sm_70,compute_70]

# Tesla K80 
# ARCH= -gencode arch=compute_37,code=sm_37

# GeForce RTX 2080 Ti, RTX 2080, RTX 2070, Quadro RTX 8000, Quadro RTX 6000, Quadro RTX 5000, Tesla T4, XNOR Tensor Cores
# ARCH= -gencode arch=compute_75,code=[sm_75,compute_75]

# Jetson XAVIER
# ARCH= -gencode arch=compute_72,code=[sm_72,compute_72]

# GTX 1080, GTX 1070, GTX 1060, GTX 1050, GTX 1030, Titan Xp, Tesla P40, Tesla P4
# ARCH= -gencode arch=compute_61,code=sm_61

# GP100/Tesla P100 - DGX-1
# ARCH= -gencode arch=compute_60,code=sm_60

# For Jetson TX1, Tegra X1, DRIVE CX, DRIVE PX - uncomment:
# ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]

# For Jetson Tx2 or Drive-PX2 uncomment:
# ARCH= -gencode arch=compute_62,code=[sm_62,compute_62]
import os
os.environ['GPU_TYPE'] = str(os.popen('nvidia-smi --query-gpu=name --format=csv,noheader').read())

def getGPUArch(argument):
  try:
    argument = argument.strip()
    # All Colab GPUs
    archTypes = {
        "Tesla V100-SXM2-16GB": "-gencode arch=compute_70,code=[sm_70,compute_70]",
        "Tesla K80": "-gencode arch=compute_37,code=sm_37",
        "Tesla T4": "-gencode arch=compute_75,code=[sm_75,compute_75]",
        "Tesla P40": "-gencode arch=compute_61,code=sm_61",
        "Tesla P4": "-gencode arch=compute_61,code=sm_61",
        "Tesla P100-PCIE-16GB": "-gencode arch=compute_60,code=sm_60"

      }
    return archTypes[argument]
  except KeyError:
    return "GPU must be added to GPU Commands"
os.environ['ARCH_VALUE'] = getGPUArch(os.environ['GPU_TYPE'])

print("GPU Type: " + os.environ['GPU_TYPE'])
print("ARCH Value: " + os.environ['ARCH_VALUE'])

"""# Installing Darknet for YOLOv4 on Colab



"""

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/
# %rm -rf darknet

#we clone the fork of darknet maintained by roboflow
#small changes have been made to configure darknet for training
!git clone https://github.com/AlexeyAB/darknet

# Commented out IPython magic to ensure Python compatibility.
#install environment from the Makefile
# %cd /content/darknet/
# compute_37, sm_37 for Tesla K80
# compute_75, sm_75 for Tesla T4
# !sed -i 's/ARCH= -gencode arch=compute_60,code=sm_60/ARCH= -gencode arch=compute_75,code=sm_75/g' Makefile

#install environment from the Makefile
#note if you are on Colab Pro this works on a P100 GPU
#if you are on Colab free, you may need to change the Makefile for the K80 GPU
#this goes for any GPU, you need to change the Makefile to inform darknet which GPU you are running on.
!sed -i 's/OPENCV=0/OPENCV=1/g' Makefile
!sed -i 's/GPU=0/GPU=1/g' Makefile
!sed -i 's/CUDNN=0/CUDNN=1/g' Makefile
!sed -i "s/ARCH= -gencode arch=compute_60,code=sm_60/ARCH= ${ARCH_VALUE}/g" Makefile
!make

# Commented out IPython magic to ensure Python compatibility.
#download the newly released yolov4-tiny weights
# %cd /content/darknet
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29

"""# Set up Custom Dataset for YOLOv4

We'll use Roboflow to convert our dataset from any format to the YOLO Darknet format. 

1. To do so, create a free [Roboflow account](https://app.roboflow.ai).
2. Upload your images and their annotations (in any format: VOC XML, COCO JSON, TensorFlow CSV, etc).
3. Apply preprocessing and augmentation steps you may like. We recommend at least `auto-orient` and a `resize` to 416x416. Generate your dataset.
4. Export your dataset in the **YOLO Darknet format**.
5. Copy your download link, and paste it below.

See our [blog post](https://blog.roboflow.ai/training-yolov4-on-a-custom-dataset/) for greater detail.

In this example, I used the open source [BCCD Dataset](https://public.roboflow.ai/object-detection/bccd). (You can `fork` it to your Roboflow account to follow along.)
"""



!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="wegusV76i2HVifSlSl4r")
project = rf.workspace("deeplearning-dnmwu").project("bottle_cans_detection")
dataset = project.version(1).download("darknet")

# Commented out IPython magic to ensure Python compatibility.
#Set up training file directories for custom dataset
# %cd /content/darknet/
# %cp {dataset.location}/train/_darknet.labels data/obj.names
# %mkdir data/obj
#copy image and labels
# %cp {dataset.location}/train/*.jpg data/obj/
# %cp {dataset.location}/valid/*.jpg data/obj/

# %cp {dataset.location}/train/*.txt data/obj/
# %cp {dataset.location}/valid/*.txt data/obj/

with open('data/obj.data', 'w') as out:
  out.write('classes = 1\n')
  out.write('train = data/train.txt\n')
  out.write('valid = data/valid.txt\n')
  out.write('names = data/obj.names\n')
  out.write('backup = backup/')

#write train file (just the image list)
import os

with open('data/train.txt', 'w') as out:
  for img in [f for f in os.listdir(dataset.location + '/train') if f.endswith('jpg')]:
    out.write('data/obj/' + img + '\n')

#write the valid file (just the image list)
import os

with open('data/valid.txt', 'w') as out:
  for img in [f for f in os.listdir(dataset.location + '/valid') if f.endswith('jpg')]:
    out.write('data/obj/' + img + '\n')

"""# Write Custom Training Config for YOLOv4"""

#we build config dynamically based on number of classes
#we build iteratively from base config files. This is the same file shape as cfg/yolo-obj.cfg
def file_len(fname):
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

num_classes = file_len(dataset.location + '/train/_darknet.labels')
max_batches = num_classes*2000
steps1 = .8 * max_batches
steps2 = .9 * max_batches
steps_str = str(steps1)+','+str(steps2)
num_filters = (num_classes + 5) * 3


print("writing config for a custom YOLOv4 detector detecting number of classes: " + str(num_classes))

#Instructions from the darknet repo
#change line max_batches to (classes*2000 but not less than number of training images, and not less than 6000), f.e. max_batches=6000 if you train for 3 classes
#change line steps to 80% and 90% of max_batches, f.e. steps=4800,5400
if os.path.exists('./cfg/custom-yolov4-tiny-detector.cfg'): os.remove('./cfg/custom-yolov4-tiny-detector.cfg')


#customize iPython writefile so we can write variables
from IPython.core.magic import register_line_cell_magic

@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))

# Commented out IPython magic to ensure Python compatibility.
# %%writetemplate ./cfg/custom-yolov4-tiny-detector.cfg
# [net]
# # Testing
# #batch=1
# #subdivisions=1
# # Training
# batch=64
# subdivisions=24
# width=416
# height=416
# channels=3
# momentum=0.9
# decay=0.0005
# angle=0
# saturation = 1.5
# exposure = 1.5
# hue=.1
# 
# learning_rate=0.00261
# burn_in=1000
# max_batches = {max_batches}
# policy=steps
# steps={steps_str}
# scales=.1,.1
# 
# [convolutional]
# batch_normalize=1
# filters=32
# size=3
# stride=2
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=2
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers=-1
# groups=2
# group_id=1
# 
# [convolutional]
# batch_normalize=1
# filters=32
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=32
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -1,-2
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -6,-1
# 
# [maxpool]
# size=2
# stride=2
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers=-1
# groups=2
# group_id=1
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=64
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -1,-2
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -6,-1
# 
# [maxpool]
# size=2
# stride=2
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers=-1
# groups=2
# group_id=1
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -1,-2
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [route]
# layers = -6,-1
# 
# [maxpool]
# size=2
# stride=2
# 
# [convolutional]
# batch_normalize=1
# filters=512
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# ##################################
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# batch_normalize=1
# filters=512
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# size=1
# stride=1
# pad=1
# filters={num_filters}
# activation=linear
# 
# 
# 
# [yolo]
# mask = 3,4,5
# anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
# classes={num_classes}
# num=6
# jitter=.3
# scale_x_y = 1.05
# cls_normalizer=1.0
# iou_normalizer=0.07
# iou_loss=ciou
# ignore_thresh = .7
# truth_thresh = 1
# random=0
# nms_kind=greedynms
# beta_nms=0.6
# 
# [route]
# layers = -4
# 
# [convolutional]
# batch_normalize=1
# filters=128
# size=1
# stride=1
# pad=1
# activation=leaky
# 
# [upsample]
# stride=2
# 
# [route]
# layers = -1, 23
# 
# [convolutional]
# batch_normalize=1
# filters=256
# size=3
# stride=1
# pad=1
# activation=leaky
# 
# [convolutional]
# size=1
# stride=1
# pad=1
# filters={num_filters}
# activation=linear
# 
# [yolo]
# mask = 1,2,3
# anchors = 10,14,  23,27,  37,58,  81,82,  135,169,  344,319
# classes={num_classes}
# num=6
# jitter=.3
# scale_x_y = 1.05
# cls_normalizer=1.0
# iou_normalizer=0.07
# iou_loss=ciou
# ignore_thresh = .7
# truth_thresh = 1
# random=0
# nms_kind=greedynms
# beta_nms=0.6

# Commented out IPython magic to ensure Python compatibility.
#here is the file that was just written. 
#you may consider adjusting certain things

#like the number of subdivisions 64 runs faster but Colab GPU may not be big enough
#if Colab GPU memory is too small, you will need to adjust subdivisions to 16
# %cat cfg/custom-yolov4-tiny-detector.cfg

"""# Train Custom YOLOv4 Detector"""

!./darknet detector train data/obj.data cfg/custom-yolov4-tiny-detector.cfg yolov4-tiny.conv.29 -dont_show -map
#If you get CUDA out of memory adjust subdivisions above!
#adjust max batches down for shorter training above

# Commented out IPython magic to ensure Python compatibility.
#define utility function
def imShow(path):
  import cv2
  import matplotlib.pyplot as plt
#   %matplotlib inline

  image = cv2.imread(path)
  height, width = image.shape[:2]
  resized_image = cv2.resize(image,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

  fig = plt.gcf()
  fig.set_size_inches(18, 10)
  plt.axis("off")
  #plt.rcParams['figure.figsize'] = [10, 5]
  plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
  plt.show()

"""# Infer Custom Objects with Saved YOLOv4 Weights"""

#check if weigths have saved yet
#backup houses the last weights for our detector
#(file yolo-obj_last.weights will be saved to the build\darknet\x64\backup\ for each 100 iterations)
#(file yolo-obj_xxxx.weights will be saved to the build\darknet\x64\backup\ for each 1000 iterations)
#After training is complete - get result yolo-obj_final.weights from path build\darknet\x64\bac
!ls backup
#if it is empty you haven't trained for long enough yet, you need to train for at least 100 iterations

# Commented out IPython magic to ensure Python compatibility.
#coco.names is hardcoded somewhere in the detector
# %cp data/obj.names data/coco.names
os.getcwd()

# Commented out IPython magic to ensure Python compatibility.
# %ls

# Commented out IPython magic to ensure Python compatibility.
  #/test has images that we can test our detector on

# %cd bottle_cans_detection-1/
test_images = [f for f in os.listdir('test') if f.endswith('.jpg')]
# %cd ..
import random
#img_path = "bottle_cans_detection-1/test/" + random.choice(test_images);

img_path = "bottle_cans_detection-1/test/" +'beverage_cans-140_jpg.rf.e5c918b8b3d2b2f8908c7837ef36d278.jpg';
print(img_path)
# %ls
#test out our detector!
#!./darknet detect cfg/custom-yolov4-tiny-detector.cfg backup/custom-yolov4-tiny-detector_best.weights {img_path} -dont-show
!./darknet detect cfg/custom-yolov4-tiny-detector.cfg backup/yolov4-tiny.weights {img_path} -dont_show
imShow('/content/darknet/predictions.jpg')

"""Run detector on a webcam image"""



#run detector on images captured by webcam for your custom YOLOv4 trained model
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

def take_photo(filename='photo.jpg', quality=0.8):
  js = Javascript('''
    async function takePhoto(quality) {
      const div = document.createElement('div');
      const capture = document.createElement('button');
      capture.textContent = 'Capture';
      div.appendChild(capture);

      const video = document.createElement('video');
      video.style.display = 'block';
      const stream = await navigator.mediaDevices.getUserMedia({video: true});

      document.body.appendChild(div);
      div.appendChild(video);
      video.srcObject = stream;
      await video.play();

      // Resize the output to fit the video element.
      google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

      // Wait for Capture to be clicked.
      await new Promise((resolve) => capture.onclick = resolve);

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getVideoTracks()[0].stop();
      div.remove();
      return canvas.toDataURL('image/jpeg', quality);
    }
    ''')
  display(js)
  data = eval_js('takePhoto({})'.format(quality))
  binary = b64decode(data.split(',')[1])
  with open(filename, 'wb') as f:
    f.write(binary)
  return filename

from IPython.display import Image
try:
  filename = take_photo()
  print('Saved to {}'.format(filename))
  
  # Show the image which was just taken.
  display(Image(filename))
except Exception as err:
  # Errors will be thrown if the user does not have a webcam or if they do not
  # grant the page permission to access it.
  print(str(err))

!./darknet detect cfg/custom-yolov4-tiny-detector.cfg backup/custom-yolov4-tiny-detector_best.weights photo.jpg -dont_show
imShow('predictions.jpg')

"""Run detector on a video"""

# Commented out IPython magic to ensure Python compatibility.
# run your custom detector on a video with this command (upload a video to your google drive to test, the thresh flag sets the minimum accuracy required for object detection).This saves the output video with the detections in your output path
# %cd /content/darknet
!./darknet detector demo data/obj.data cfg/custom-yolov4-tiny-detector.cfg backup/custom-yolov4-tiny-detector_best.weights -dont_show output_Trim.mp4 -i 0 -out_filename result.avi

from google.colab import files
files.download('/content/darknet/backup/custom-yolov4-tiny-detector_best.weights')