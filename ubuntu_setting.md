## Nvidia Driver

```sh
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update
sudo ubuntu-drivers autoinstall
sudo reboot
```

- Check the nvidia driver version

```sh
# NVIDIA-SMI 440.59       Driver Version: 440.59       CUDA Version: 10.2
nvidia-smi
```

## CUDA

- Download the CUDA toolkit in this [link](https://developer.nvidia.com/cuda-toolkit-archive)

- This is the CUDA v10.2 for ubuntu 18.04

```sh
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
sudo mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1804-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-10-2-local-10.2.89-440.33.01/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda
```

- Edit the `~/.bashrc`

```sh
vi ~/.bashrc
```

- Add the following to the end of file

```sh
export PATH=/usr/local/cuda-10.2/bin:${PATH}
export LD_LIBRARY_PATH=/usr/local/cuda-10.2/lib64:${LD_LIBRARY_PATH}
```

- Restart the `~/.bashrc`

```sh
source ~/.bashrc
```

- Check the CUDA version

```sh
nvcc -V
```

## cuDNN

- Download cuDNN in tihs [link](https://developer.nvidia.com/rdp/cudnn-download#a-collapse765-102)

```sh
# cuDNN v7.6.5 for CUDA 10.2
sudo dpkg -i libcudnn7_7.6.5.32-1+cuda10.2_amd64.deb
```

- Verifying the cuDNN

```sh
cp -r /usr/src/cudnn_samples_v8/ $HOME
cd $HOME/cudnn_samples_v8/mnistCUDNN
make clean && make

# Test passed!
./mnistCUDNN
```

## OpenCV

- Download source codes

```sh
wget -O opencv-3.4.0.zip https://github.com/opencv/opencv/archive/3.4.0.zip
wget -O opencv_contrib-3.4.0.zip https://github.com/opencv/opencv_contrib/archive/3.4.0.zip

unzip opencv-3.4.0.zip
unzip opencv_contrib-3.4.0.zip

mkdir build && cd build
```

- Build the source codes

```sh
# cmake
cmake \
-D CMAKE_BUILD_TYPE=Release \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D BUILD_WITH_DEBUG_INFO=OFF \
-D BUILD_EXAMPLES=ON \
-D BUILD_opencv_python2=OFF \
-D BUILD_opencv_python3=ON \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib-3.4.0/modules \
-D WITH_TBB=ON \
-D WITH_V4L=ON \
../opencv-3.4.0/ 2>&1 | tee cmake_messages.txt

# check the number of CPU cores
nproc

make -j{NUM_CPU}
sudo make install
sudo ldconfig
```

- Check the pkg

```sh
# 3.4.0
pkg-config --modversion opencv
```

- Download the `opencv-python`

```sh
pip install opencv-python
```

## RealSense SDK

- [Reference link](https://www.intel.com/content/dam/support/us/en/documents/emerging-technologies/intel-realsense-technology/Intel-RealSense-SDK2-Github-Guide.pdf)

- Add Intel repositories and register the server's public key

```sh
echo 'deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo   xenialmain' | sudo tee /etc/apt/sources.list.d/realsense-public.list
sudo apt-key adv --keyserver keys.gnupg.net --recv-key 6F3EFCDE
```

- In order to run demos install

```sh
sudo apt update
sudo apt-get install librealsense2-dkms
sudo apt-get install librealsense2-utils
```

- Additional packages for developers

```sh
sudo apt-get install librealsense2-dev
sudo apt-get install librealsense2-dbg
```

- Requirement packages

```sh
sudo apt update && sudo apt upgrade && sudo apt dist-upgrade

sudo apt install git cmake3 libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
```

- Download source codes

```sh
git clone git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense && mkdir build && cd build
```

- Build the librealsense SDK

```sh
cmake ../ -DBUILD_EXAMPLES=true -DBUILD_WITH_CUDA=true -DBUILD_PYTHON_BINDINGS=bool:true
make -j{NUM_CPU}
sudo make install

echo "export PYTHONPATH=$PYTHONPATH:/usr/local/lib" >> ~/.bashrc

# copy udev rules so that camera can be from user space
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && udevadm trigger

./scripts/patch-realsense-ubuntu-lts.sh
```

## PyTorch

```sh
pip install torch torchvision
```

## xRDP

### Install

```sh
sudo apt install xrdp
```

### Change port

```sh
sudo vi /etc/xrdp/xrdp.ini
```

- default port: 3389

### Color Profile

```sh
# sudo vi /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes
```

### Service Start

```sh
service xrdp start
service xrdp restart
```
