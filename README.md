# Edge-Based Fusion of LiDAR and Camera Data for Real-Time Colored 3D Point Cloud Generation

This repository contains the code and documentation for the paper:  
**"Edge-Based Fusion of LiDAR and Camera Data for Real-Time Colored 3D Point Cloud Generation"**  

## Abstract  
This project demonstrates the feasibility of generating detailed colored 3D point clouds on edge computing platforms. By integrating a 2D LiDAR sensor, a camera module, and a single-board computer, this solution processes spatial and RGB data in real time.  

Key challenges addressed include:  
- Optimizing algorithms for edge devices.  
- Accurate data fusion through calibration.  
- Managing real-time data processing with constrained resources.  

The methodology achieves precise synchronization between spatial and color data. Experimental results show effective 3D reconstruction without reliance on traditional desktop infrastructure, advancing edge computing's capabilities in 3D modeling and mapping.  

## Features  
- **Real-Time 3D Point Cloud Generation**: Combines LiDAR data and images for colored 3D point clouds.  
- **Edge Device Optimization**: Designed to work efficiently on single-board computers.  
- **Simplified Workflow**: All processing is consolidated in a single pipeline for ease of use.  

## Prerequisites  
- **Hardware**:  
  - 2D LiDAR sensor (recommend Slamtec RPLIDAR A1)
  - Camera module compatible with `libcamera` (recommend rev 1.3 camera module)
  - Servo motors (for LiDAR adjustment, recommend Mg996r)
  - Accelerometer (recommend ADXL345)
  - Single Board Computer (recommend Raspberry Pi 4)
- **Software**:  
  - Python (>=3.6)
  - Pi OS (recommend)

## Prototype Assembly Instructions
The STL files for the prototype can be found in the prototype folder of this repository. Simply download the files and use a 3D printer for printing.
The material used for printing is PLA 1.75mm filament, with a layer height of 0.2mm for optimal results.
There is also a video of the mounting process. Feel free to download, if necessary.

<img src="https://raw.githubusercontent.com/edulazzari/Edge-Based-Fusion-of-LiDAR-and-Camera-Data-for-Real-Time-Colored-3D-Point-Cloud-Generation/main/Prototype/prototipo_final.png" alt="Protótipo final" width="500"/>

## Code Tutorial
    libcamera-jpeg -o testando.jpg --shutter 20000
This command uses the libcamera tool to capture a JPEG image from a camera module. Here's what each part of the command does:
- libcamera-jpeg: This is the command-line tool used to capture JPEG images with the libcamera library.
- -o testando.jpg: This option specifies the output file where the captured image will be saved.
- --shutter 20000: This option controls the shutter speed of the camera. The value 20000 refers to the exposure time in microseconds (µs). So, in this case, the camera's shutter is open for 20 milliseconds (20000 µs). A longer shutter speed allows more light to reach the camera sensor, which can be useful in low-light environments but might also cause motion blur if the camera or subject moves. Adapt it according to the ambient light.

## Running the Code  

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/your-repo-name/Edge-Based-Fusion-of-LiDAR-and-Camera-Data.git  
   cd Edge-Based-Fusion-of-LiDAR-and-Camera-Data  
   ./main2.sh



