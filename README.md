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
- an old phone (you can also use CAM module for seamless integration)
- IR Sensor   

### Software  
- YOLOv8 trained weapon detection model  
- OpenCV 
- Python 
- SMTP 


   
