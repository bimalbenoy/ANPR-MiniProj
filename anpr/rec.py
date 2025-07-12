import os
import cv2
import pandas as pd
import logging
import torch
from ultralytics import YOLO
from paddleocr import PaddleOCR
from datetime import datetime

# 🛑 Trust override: Allow full PyTorch unpickling
torch_load = torch.load
def unsafe_load(*args, **kwargs):
    kwargs['weights_only'] = False
    return torch_load(*args, **kwargs)
torch.load = unsafe_load

# Headless OpenCV
os.environ["QT_QPA_PLATFORM"] = "offscreen"

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class PlateRecognition:
    def __init__(self, model_path="models/best.pt"):
        # Load YOLOv8 model
        self.model = YOLO(model_path)

        # Initialize PaddleOCR
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang="en",
            det_model_dir="./models/en_PP-OCRv3_det_infer",
            rec_model_dir="./models/en_PP-OCRv3_rec_infer",
            cls_model_dir="./models/ch_ppocr_mobile_v2.0_cls_infer",
        )

    def correct_text(self, text):
        if len(text) < 6:
            return text
        corrected_text = list(text)
        for i in range(2):
            if corrected_text[i] == '0':
                corrected_text[i] = 'O'
        for i in range(2, 4):
            if corrected_text[i] == 'O':
                corrected_text[i] = '0'
        for i in range(4, len(corrected_text)):
            if corrected_text[i] == 'O':
                corrected_text[i] = '0'
        return ''.join(corrected_text)

    def recognize_text(self, crop):
        if crop is None or crop.size == 0:
            logging.warning("⚠️ Empty crop, skipping OCR.")
            return ""
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        result = self.ocr.ocr(gray, cls=True)
        detected_text = "".join([line[1][0] for line in result[0]]).strip() if result and result[0] else ""
        detected_text = detected_text.replace("IND", "").replace(" ", "").replace(".", "").upper()
        words = detected_text.split()
        detected_text = " ".join(sorted(set(words), key=words.index))
        detected_text = "".join(char for char in detected_text if char.isalnum())
        if "KL" in detected_text:
            detected_text = detected_text[detected_text.index("KL"):]
        detected_text = self.correct_text(detected_text)
        if not detected_text:
            logging.warning("❌ No text detected by OCR.")
        return detected_text

    def process_frame(self, frame):
        if frame is None:
            logging.error("❌ Error: Invalid frame received.")
            return []
        results = self.model.predict(frame, conf=0.5)
        boxes = results[0].boxes.data if results and hasattr(results[0].boxes, "data") else None
        if boxes is None or boxes.numel() == 0:
            logging.warning("⚠️ No license plate detected.")
            return []
        detected_data = []
        for box in boxes:
            x1, y1, x2, y2, _, _ = map(int, box.tolist()[:6])
            crop = frame[y1:y2, x1:x2]
            text = self.recognize_text(crop)
            if text:
                detected_data.append((text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return detected_data

    def process_input_file(self, input_file):
        is_image = input_file.lower().endswith((".jpg", ".jpeg", ".png"))
        if is_image:
            frame = cv2.imread(input_file)
            if frame is None:
                logging.error("❌ Error: Unable to read the image file.")
                return []
            detected_data = self.process_frame(frame)
            cv2.imshow("Detected Image", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return detected_data
        else:
            cap = cv2.VideoCapture(input_file)
            if not cap.isOpened():
                logging.error("❌ Error: Unable to open video file.")
                return []
            detected_plates = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                detected_plates.extend(self.process_frame(frame))
                cv2.imshow("Video Detection", frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            return detected_plates

    def save_results(self, detected_plates, output_file="anpr/car_plate_data.txt"):
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        if detected_plates:
            with open(output_file, "a") as file:
                if os.stat(output_file).st_size == 0:
                    file.write("NumberPlate\tDate\tTime\n")
                for plate, timestamp in detected_plates:
                    file.write(f"{plate}\t{timestamp}\n")
            logging.info(f"✅ Results saved to {output_file}")


if __name__ == "__main__":
    input_file = "car_video1.mp4"
    plate_recognition = PlateRecognition()
    detected_plates = plate_recognition.process_input_file(input_file)
    plate_recognition.save_results(detected_plates)
    logging.info("🎉 License Plate Detection Complete.")
