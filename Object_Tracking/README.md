# Bottles and Cans tracking
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1wZ_dKPqKXUCNT_bdk5GjUZ8t4IjWFjmB?usp=sharing)

<p> The implementation of bottle and can tracking utilizes a sophisticated integration of YOLOv4-tiny, DeepSort, and Tensorflow frameworks. YOLOv4-tiny, a scaled-down variant of YOLOv4, is specifically designed for devices with limited computational capacity, such as the Raspberry Pi 4 and Jetson Nano, enabling real-time object detection within video streams. YOLOv4-tiny's object detection mechanism operates on a frame-by-frame basis, wherein the same object appearing in different frames is treated as separate entities. To address this limitation, the DeepSort algorithm is employed, effectively linking objects across multiple frames to facilitate continuous tracking. This approach demonstrates the potential for developing efficient object detection and tracking systems, particularly for applications with constrained computational resources. </p>

# DeepSort Algorithm



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

When ever the bottles or cans pass the green box the system will start counting them. The system will record the ID of each object so that it wont duplicate the object.
