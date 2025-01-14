import cv2
import numpy as np
import onnxruntime as ort
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO
import threading
import os
from email.mime.base import MIMEBase
from email import encoders


# Load ONNX model
onnx_model_path = "path"
session = ort.InferenceSession(onnx_model_path)

# Define input and output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Open video stream
ip_camera_url = "http://your-ip/video" #Enter your ip address here
cap = cv2.VideoCapture(ip_camera_url)

# Email function (similar to previous version)
def send_email(subject, body, recipient_email, attachment_path):
    sender_email = "your_email@gmail.com"  # Your Gmail address
    password = "your_API_password"  # Gmail API Password not app password(technically it is known as app password only but don't confuse it with your gmail password)

    try:
        # Create a MIME object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email  
        msg['Subject'] = subject

        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))

        # Attach the image if provided
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                image = MIMEBase('application', 'octet-stream')
                image.set_payload(attachment.read())
            encoders.encode_base64(image)
            image.add_header(
                'Content-Disposition',
                f'attachment; filename={attachment_path.split("/")[-1]}',
            )
            msg.attach(image)

        # Establish connection with Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# IR sensor pins setup
IR_SENSOR_PIN_1 = 17  # GPIO Pin for IR Sensor 1
IR_SENSOR_PIN_2 = 27  # GPIO Pin for IR Sensor 2

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR_PIN_1, GPIO.IN)
GPIO.setup(IR_SENSOR_PIN_2, GPIO.IN)

# Flag to track if sensor is triggered
photo_taken = False
photo_file_path = ""

def sensor_monitoring():
    """Monitor the IR sensors in a separate thread."""
    global photo_taken, photo_file_path

    while True:
        # Check if any IR sensor is triggered
        if GPIO.input(IR_SENSOR_PIN_1) == GPIO.HIGH or GPIO.input(IR_SENSOR_PIN_2) == GPIO.HIGH:
            if not photo_taken:  # Prevent taking multiple photos in quick succession
                print("Sensor triggered! Taking photo...")
                # Capture the current frame
                ret, frame = cap.read()
                if ret:
                    # Save the frame as an image
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    photo_file_path = f"/home/divit/photos/photo_{timestamp}.jpg"
                    cv2.imwrite(photo_file_path, frame)
                    photo_taken = True  # Set flag so photo isn't taken multiple times
                    # Send the photo via email
                    send_email("IR Sensor Triggered", "An object was detected by the IR sensor.", "recipient@example.com", photo_file_path)

        time.sleep(0.1)  # Small delay to avoid high CPU usage in sensor monitoring thread

def preprocess_frame(frame):
    """Preprocess the frame for ONNX model input."""
    img = cv2.resize(frame, (640, 640))  # Resize to model's expected size
    img = img[..., ::-1]  # Convert BGR to RGB
    img = img.transpose(2, 0, 1)  # Convert to CHW format
    img = img[np.newaxis, :, :, :] / 255.0  # Normalize to [0, 1]
    return img.astype(np.float32)

def scale_boxes(box, original_shape):
    """Scale bounding boxes back to the original image dimensions."""
    original_h, original_w = original_shape
    scale_x = original_w / 640
    scale_y = original_h / 640
    x1, y1, x2, y2 = box[:4]
    return [
        int(x1 * scale_x),
        int(y1 * scale_y),
        int(x2 * scale_x),
        int(y2 * scale_y),
    ]

def non_max_suppression(predictions, iou_threshold=0.4):
    """Apply Non-Maximum Suppression to remove overlapping boxes."""
    boxes = []
    confidences = []
    class_ids = []

    for pred in predictions:
        x1, y1, x2, y2, conf, class_conf, class_id = pred
        if conf > 0.2:  # Confidence threshold
            boxes.append([x1, y1, x2, y2])
            confidences.append(float(conf))
            class_ids.append(int(class_id))

    # Apply OpenCV's NMS function
    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, score_threshold=0.2, nms_threshold=iou_threshold
    )

    filtered_boxes = []
    if len(indices) > 0:
        for i in indices.flatten():
            scaled_box = scale_boxes(boxes[i], (original_h, original_w))
            filtered_boxes.append((*scaled_box, confidences[i], class_ids[i]))
    return filtered_boxes

# FPS calculation
prev_time = time.time()

# Start the IR sensor monitoring in a separate thread
sensor_thread = threading.Thread(target=sensor_monitoring)
sensor_thread.daemon = True  # Ensure it exits when the main program exits
sensor_thread.start()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from camera.")
        break

    original_h, original_w, _ = frame.shape  # Original frame dimensions

    # Preprocess frame
    img = preprocess_frame(frame)

    # Run inference
    preds = session.run([output_name], {input_name: img})[0]
    preds = preds[0]  

   
    detections = non_max_suppression(preds)

    # Draw detections
    for (x1, y1, x2, y2, conf, cls) in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"Class: {cls}, Conf: {conf:.2f}"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Calculate and display FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Show the frame
    cv2.imshow("ONNX Inference", frame)

    # Quit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
