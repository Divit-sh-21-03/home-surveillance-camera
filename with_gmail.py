import cv2
import numpy as np
import onnxruntime as ort
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from paramiko import SSHClient
from paramiko.client import AutoAddPolicy

# Load ONNX model
onnx_model_path = "path-to/best.onnx"
session = ort.InferenceSession(onnx_model_path)

# Define input and output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Open video stream
ip_camera_url = "http://your_ip/video"
cap = cv2.VideoCapture(ip_camera_url)

# Define email sending function using Gmail SMTP with App Password
def send_email(subject, body, recipient_email):
    sender_email = "your_email@gmail.com"  # Replace with your Gmail address
    sender_password = "your_app_password"  # Replace with your Gmail App Password (NOT your Gmail password)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # TLS port for Gmail SMTP

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection using TLS
        server.login(sender_email, sender_password)  # Log in using App Password
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()  # Close the server connection
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Define weapon class IDs (Assuming class ID 0 corresponds to weapons)
weapon_class_ids = [0]  # Modify based on your model's output for weapons

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
    preds = preds[0]  # Remove batch dimension

    # Apply Non-Maximum Suppression
    detections = non_max_suppression(preds)

    # Check if weapon is detected and send an email
    for (x1, y1, x2, y2, conf, cls) in detections:
        if cls in weapon_class_ids:  # Check if the detected class is a weapon
            subject = "Weapon Detected!"
            body = f"A weapon was detected at position ({x1}, {y1}) to ({x2}, {y2}) with confidence {conf:.2f}."
            recipient_email = "recipient@example.com"  # Replace with recipient's email
            send_email(subject, body, recipient_email)

        # Draw detections
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
