import cv2
import numpy as np
import onnxruntime as ort
import time

# Load ONNX model
onnx_model_path = "give the path here"
session = ort.InferenceSession(onnx_model_path)

# Define input and output names
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Open video stream
ip_camera_url = "http://your-ip/video"
cap = cv2.VideoCapture(ip_camera_url)

def preprocess_frame(frame):
    """Preprocess the frame for ONNX model input."""
    img = cv2.resize(frame, (640, 640))
    img = img.transpose(2, 0, 1)  # Convert to CHW format
    img = img[np.newaxis, :, :, :] / 255.0  # Add batch dimension and normalize
    return img.astype(np.float32)

def non_max_suppression(predictions, iou_threshold=0.4):
    """Apply Non-Maximum Suppression to remove overlapping boxes."""
    boxes = []
    confidences = []
    class_ids = []

    for pred in predictions:
        x1, y1, x2, y2, conf, class_conf, class_id = pred
        if conf > 0.2:  # Filter by confidence threshold
            boxes.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])  # Convert to [x, y, w, h]
            confidences.append(float(conf))
            class_ids.append(int(class_id))

    # Apply OpenCV's NMS function
    if len(boxes) > 0:
        indices = cv2.dnn.NMSBoxes(
            boxes, confidences, score_threshold=0.2, nms_threshold=iou_threshold
        )

        filtered_boxes = []
        if len(indices) > 0:
            for i in indices.flatten():  # Ensure indices is properly iterated
                filtered_boxes.append((*boxes[i], confidences[i], class_ids[i]))
        return filtered_boxes
    else:
        return []  

# FPS calculation
prev_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to connect to ip camera.")
        break

    # Preprocess frame
    img = preprocess_frame(frame)

    # Run inference
    preds = session.run([output_name], {input_name: img})[0]
    preds = preds[0]  # Remove batch dimension if present

    # Apply Non-Maximum Suppression
    detections = non_max_suppression(preds)

    # Draw detections
    for (x, y, w, h, conf, cls) in detections:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = f"Class: {cls}, Conf: {conf:.2f}"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

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
