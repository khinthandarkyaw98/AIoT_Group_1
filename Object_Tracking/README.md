# Bottles and Cans tracking
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zmeSTP3J5zu2d5fHgsQC06DyYEYJFXq1?usp=sharing)

Bottles and cans tracking implemented with YOLOv4-tiny, DeepSort, and Tensorflow. YOLOv4-tiny is the smaller version for YOLOv4, which is suitable for 
small computation device such as raspberry pi 4 and Jetson Nano for detecting image in real-time video. Object detection detect object in one frame at a time, 
same object in diffrent frame will count as new object for YOLOv4-tiny object detector. To solve this the Deepsort algorithm is used to tracking object which connect object in diffrent frames together.

# How to Run this code

## Install the Dependencies

### Conda

```bash
# Tensorflow CPU
conda env create -f conda-cpu.yml
conda activate yolov4-cpu

# Tensorflow GPU
conda env create -f conda-gpu.yml
conda activate yolov4-gpu
```
### Pip

(TensorFlow 2 packages require a pip version >19.0.)
```bash
# TensorFlow CPU
pip install -r requirements.txt

# TensorFlow GPU
pip install -r requirements-gpu.txt
```
## Convert the Darknet model into Tensorflow model

The pre-trained model is import in the data folder use the copy the code below to convert the model into tensorflow model 
```
# save yolov4-tiny model
python save_model.py --weights ./data/yolov4-tiny.weights --output ./checkpoints/yolov4-tiny-416 --model yolov4 --tiny

```
## Run Object Tracking
```
# Run Object tracking
python object_tracker.py --weights ./checkpoints/yolov4-tiny-416 --model yolov4 --video ./data/video/test.mp4 --output ./outputs/tiny.avi --tiny

```
# Result

The below video is the result of object tracking

![Result](https://github.com/khinthandarkyaw98/AIoT_Group_1/blob/main/Object_Tracking/outputs/bottles_cans_tracking.gif)
