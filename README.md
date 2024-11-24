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
Ensure the following dependencies are installed:  
- **Hardware**:  
  - 2D LiDAR sensor  
  - Camera module compatible with `libcamera`  
  - Servo motors (optional, for LiDAR adjustment)  
- **Software**:  
  - Python (>=3.6)  

## Running the Code  

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/your-repo-name/Edge-Based-Fusion-of-LiDAR-and-Camera-Data.git  
   cd Edge-Based-Fusion-of-LiDAR-and-Camera-Data  
   ./main2.sh
