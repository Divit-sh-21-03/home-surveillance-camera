
## Features

- **Real-Time Weapon Detection**  
  - Detects weapons like guns and knives using a YOLOv8 model.  
  - Draws bounding boxes around detected objects with confidence scores.  
  - Sends an email alert with an image of the detected threat.  

- **Tamper Detection**  
  - Uses an IR sensor to detect if someone is tampering with or destroying the setup.  
  - Sends an immediate email alert in case of tampering.  

- **Flexible Camera Integration**  
  - Supports IP cameras for video streaming.  
  - Adjustable resolution settings for better performance and FPS optimization.  

- **Email Notifications**  
  - Sends real-time email alerts with images of detected threats.  
  - Configurable with Gmail or other email services using app passwords.  

---

## Components  

### Hardware  
- Raspberry Pi 5  
- an old phone (or any device that can be used as ip cam)
- cam module for Rasberry Pi (if you are using 2nd setup)
- IR Sensor   

### Software  
- YOLOv8 trained weapon detection model  
- OpenCV 
- Python 
- SMTP

---

# Object Detection on Edge Devices using YOLO Models

In this project, I aimed to achieve maximum FPS while running object detection models on Raspberry Pi (RPI). Although these models run seamlessly on computers/laptops, running them on edge devices requires some optimization.  

I have uploaded the **YOLOv8 (NCNN)** and **YOLOv5 (ONNX)** versions, which can be easily executed using Python scripts.  

---

##  Folder Contents

### 1. YOLOv5
- **best.onnx**: Custom YOLOv5 model in ONNX framework (optimized for edge devices).  
- **bestdivit.pt**: Custom YOLOv5 model in PyTorch framework (not recommended for edge devices; suitable for devices with better hardware).  
- **onnx.py**: Python script to run the ONNX version of the model.  
- **with_gmail.py**: Modified `onnx.py` with email alert functionality (reduces FPS slightly).  
- **final.py**: ONNX script with email alerts and IR sensor integration.  
  - FPS comparison: `onnx.py > with_gmail.py > final.py`

### 2. YOLOv8
- **best(8).pt**: Custom YOLOv8 model in PyTorch framework.  
- **model.ncnn.bin** and **model.ncnn(1).param**: Custom YOLOv8 model in NCNN framework.  
- **yolov8_final.py**: Python script to run the NCNN version of the model.

---

##  Implementation Details

### Failed Attempts
1. YOLOv8 (PyTorch): Adjusted resolution to achieve 2-3 FPS, but accuracy was poor.  
2. YOLOv8 (NCNN): Integrated NCNN and optimized resolution for higher FPS, but accuracy remained subpar.  
3. Pretrained Custom Models: Tested several GitHub models for detection. While accurate, FPS was very low (0.5-1 FPS, trained on YOLOv8).  

### Successful Attempts
1. **YOLOv5**: Trained a custom model and converted it from PyTorch to ONNX (success).  
2. **YOLOv8**: Trained a custom model and converted it from PyTorch to NCNN (via ONNX) (success).  

---

##  Key Observations
- For **normal object detection** without identification, FPS improves significantly (10-15 FPS).  
- The **current setup cost (~₹7-8k)** using a Raspberry Pi 4B is high compared to commercial AI cameras (~₹2-3k). However, this setup provides extensive customization options:  
  - Integration of two cameras to capture tampering attempts.  
  - Integrating IR sensors for detection if someone is tampering the setup.  

### Cost-Effective Alternative:
If you wish to reduce the hardware cost to **₹1-2k**, you can use an ESP32-CAM and deploy the YOLO model on a server.  

---

##  Advantages
- Full customization for specific use cases.  
- Ability to integrate additional functionalities (e.g., tamper-proofing, face recognition).  
- Greater flexibility in hardware and software configurations compared to commercial solutions.
 
---

## Screenshots of email notification 
![Screenshot_2025-01-14-10-22-21-91_e307a3f9df9f380ebaf106e1dc980bb6](https://github.com/user-attachments/assets/22a2ea14-39c5-4dc8-ad5d-a27415b8cf74)
![Screenshot_2025-01-14-10-22-37-56_e307a3f9df9f380ebaf106e1dc980bb6](https://github.com/user-attachments/assets/27fce27a-a10f-428d-9d8a-601e8672f5dd)


   
