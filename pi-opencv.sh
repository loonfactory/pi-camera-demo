#!/bin/bash
sudo apt-get update -y
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-103 python3-pyqt5 python3-dev -y
pip install opencv-contrib-python==4.4.0.46
pip upgrade numpy
