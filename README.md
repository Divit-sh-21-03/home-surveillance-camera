# Home Security System with Weapon Detection

This project showcases a robust home security system leveraging a Raspberry Pi 5 for real-time weapon detection, tamper detection, and an integrated alert system. It's designed for efficiency on edge devices, with a focus on optimizing object detection models for low-power hardware.

## Features

- **Real-Time Weapon Detection**
  - Identifies weapons like guns and knives using a YOLOv8 model.
  - Displays bounding boxes around detected objects with confidence scores.
  - Dispatches email alerts with an image of the detected threat.

- **Tamper Detection**
  - Utilizes an IR sensor to detect unauthorized interaction with the system setup.
  - Triggers an immediate email alert if tampering is detected.

- **Flexible Camera Integration**
  - Supports IP cameras for live video streaming.
  - Offers adjustable resolution settings to optimize performance and frame rate.

- **Email Notifications**
  - Delivers real-time email alerts, including images of detected threats.
  - Configurable with Gmail or other email services using app passwords for secure integration.

- **Custom Uninterruptible Power Supply (UPS)**
  - Provides continuous power to the Raspberry Pi 5, ensuring uninterrupted operation during power fluctuations or outages.
  - Seamlessly switches between a main power source and a power bank (as a backup battery) when the primary power is unavailable.
  - Incorporates components to facilitate a smooth transition, helping prevent system reboots or interruptions.

---

## Components

### Hardware
- Raspberry Pi 5
- An old smartphone (or any device configurable as an IP camera)
- Camera module for Raspberry Pi (for an alternative setup)
- IR Sensor
- **Custom UPS Components (for the power backup system):**
  - Main Power Source
  - ADC 
  - Power Bank or battery
  - 5V Relay Module (Single Pole Double Throw - SPDT)
  - Schottky diodes for low voltage drop
  - Capacitors (for power smoothing)
  - Transistor and Resistor 

### Software
- YOLOv8 trained weapon detection model
- OpenCV
- Python
- SMTP (for email functionality)

---

# Object Detection on Edge Devices using YOLO Models

This project focused on achieving maximum frames per second (FPS) for object detection models deployed on Raspberry Pi (RPI). While these models perform seamlessly on computers and laptops, running them on edge devices necessitates significant optimization.

The repository includes optimized **YOLOv8 (NCNN)** and **YOLOv5 (ONNX)** versions, designed for efficient execution with Python scripts on the Raspberry Pi.

---

## Folder Contents

### 1. YOLOv5
- **best.onnx**: Custom YOLOv5 model in ONNX framework (optimized for edge devices).
- **bestdivit.pt**: Custom YOLOv5 model in PyTorch framework (recommended for devices with robust hardware; not ideal for edge devices).
- **onnx.py**: Python script for running the ONNX version of the model.
- **with_gmail.py**: A modified `onnx.py` incorporating email alert functionality (this may slightly reduce FPS).
- **final.py**: The ONNX script integrating both email alerts and IR sensor capabilities.
  - *FPS comparison: `onnx.py` > `with_gmail.py` > `final.py`*

### 2. YOLOv8
- **best(8).pt**: Custom YOLOv8 model in PyTorch framework.
- **model.ncnn.bin** and **model.ncnn(1).param**: Custom YOLOv8 model in NCNN framework.
- **yolov8_final.py**: Python script for running the NCNN version of the model.

---

## Implementation Details

### Approaches Explored
1. **YOLOv8 (PyTorch):** Resolution adjustments were explored, yielding 2-3 FPS; however, accuracy was not satisfactory.
2. **YOLOv8 (NCNN):** NCNN integration and resolution optimization improved FPS, though accuracy remained a challenge.
3. **Pretrained Custom Models:** Several GitHub models were evaluated for detection. While accurate, the FPS remained very low (0.5-1 FPS, trained on YOLOv8).

### Achieved Optimizations
1. **YOLOv5:** A custom model was trained and successfully converted from PyTorch to ONNX.
2. **YOLOv8:** A custom model was trained and successfully converted from PyTorch to NCNN (via ONNX).

---

## Key Observations
- For **general object detection** without specific identification requirements, FPS significantly improves (10-15 FPS).
- The **current system cost (~₹7-8k INR)**, utilizing a Raspberry Pi 4B, is higher compared to readily available commercial AI cameras (~₹2-3k INR). However, this custom setup offers extensive customization capabilities:
  - Integration of multiple cameras for comprehensive surveillance, including tamper attempt capture.
  - Inclusion of IR sensors for detecting physical interference with the setup.

### Cost-Effective Alternative:
For projects aiming to reduce hardware costs to **₹1-2k INR**, an ESP32-CAM coupled with server-side YOLO model deployment presents a viable solution.

---

## Advantages
- Full customization to meet specific application needs.
- Capability to incorporate additional functionalities, such as tamper-proofing and facial recognition.
- Enhanced flexibility in hardware and software configurations compared to off-the-shelf commercial solutions.

---

## Screenshots of Email Notification

![Screenshot_2025-01-14-10-22-21-91_e307a3f9df9f380ebaf106e1dc980bb6](https://github.com/user-attachments/assets/22a2ea14-39c5-4dc8-ad5d-a27415b8cf74)  


---

## Contributing

Contributions are welcome. Fork the repository, create a feature branch, include testbench evidence, and (where applicable) updated implementation screenshots, then submit a pull request.

---

## License

Apache License 2.0 — reuse is allowed with proper attribution. Do not remove or alter the author's name in any derivative works. See the `LICENSE` file in this repository for full details.

---

## Author

Divit Sharma — B.Tech (2nd Year)  
GitHub: [https://github.com/Divit-sh-21-03](https://github.com/Divit-sh-21-03)  
Email: divits@iitbhilai.ac.in
