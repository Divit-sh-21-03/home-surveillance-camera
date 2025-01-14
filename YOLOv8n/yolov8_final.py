import cv2
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ultralytics import YOLO

# Email sending function
def send_email(subject, body, recipient_email, attachment_path):
    sender_email = "your_email@gmail.com"  # Your Gmail address
    password = "your_app_password"  # Gmail App Password

    try:
        # Create a MIME object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email  # Ensure this is a string, not a tuple
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


# Function to detect objects from IP camera stream
def detect_objects_from_ip_camera(ip_camera_url):
    # Load YOLO model
    yolo_model = YOLO('./runs/detect/Normal_Compressed/weights/best.pt')

    # Open video stream
    cap = cv2.VideoCapture(ip_camera_url)
    if not cap.isOpened():
        print("Error: Unable to access IP camera.")
        return

    # Set resolution for FPS optimization
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height

    while True:
        start_time = time.time()  # Start time for FPS calculation

        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Run YOLO model on the frame
        results = yolo_model(frame)

        # Iterate over detection results
        for result in results:
            classes = result.names
            cls = result.boxes.cls
            conf = result.boxes.conf
            detections = result.boxes.xyxy

            # Loop through detected objects
            for pos, detection in enumerate(detections):
                if conf[pos] >= 0.5:  # Confidence threshold
                    xmin, ymin, xmax, ymax = detection
                    label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}"
                    color = (0, int(cls[pos] * 20), 255)  # Color based on class
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                    cv2.putText(frame, label, (int(xmin), int(ymin) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

                    # Check if knife or gun is detected
                    if classes[int(cls[pos])] in ["knife", "gun"]:  # Adjust based on your model’s class names
                        send_email(
                            subject="Weapon Detected",
                            body=f"Warning: {classes[int(cls[pos])]} detected with confidence {conf[pos]:.2f}."
                        )

        # Calculate FPS
        end_time = time.time()
        fps = 1 / (end_time - start_time)

        # Display FPS on the frame
        text = f"FPS: {fps:.1f}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Show the frame
        cv2.imshow("IP Camera Stream", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Replace with your IP camera URL
ip_camera_url = "http://10.50.55.193:8080/video"
detect_objects_from_ip_camera(ip_camera_url)
