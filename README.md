
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
I know that implementing this approach just to detect hostile intruders is way too costly. The hardware setup would cost somewhere around 7-8k (if Raspberry Pi 4B is used), whereas in the commercial market, basic AI cameras are available for 2-3k.  
But the advantage we have here is that we can customize the setup the way we want. For instance, I integrated two different cameras so that if someone tries to tamper with the setup, their face can still be captured. Similarly, we can also deploy face recognition so that if we are not at home and an unknown person decides to pay a visit, we are alerted. The code and implementation of this face recognition will also be posted in the repo at a later point in time after optimizing it for better FPS.  

However, if you want to reduce the hardware setup cost to just 1-2k, you can implement this project using an ESP32-CAM and deploy your YOLO model on a server. For that, you will need to know the basics of:  
- HTTP Protocols  
- Model Deployment on Servers  
- YOLO (You Only Look Once) Object Detection  



   
