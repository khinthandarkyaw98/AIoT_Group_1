# yolov4-deepsort
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

Object tracking for bottle tracking implemented with YOLOv4-tiny, DeepSort, and Tensorflow. YOLOv4-tiny is the smaller version for YOLOv4, which is suitable for 
small computation device such as raspberry pi 4 and Jetson Nano for detecting image in real-time video. Object detection detect object in one frame at a time, 
same object in diffrent frame will count as new object for YOLOv4-tiny object detector. To solve this the Deepsort algorithm is used to tracking object which connect
object in diffrent frames together.
