import os
import logging

from django.conf import settings

from .rec import PlateRecognition

logging.basicConfig(level=logging.INFO)

def process_video_file(input_file):
    output_file = os.path.join(settings.MEDIA_ROOT, 'anpr', 'car_plate_data.txt')
    recognizer = PlateRecognition()
    result = recognizer.process_input_file(input_file)
    recognizer.save_results(result, output_file=output_file)
    logging.info("✅ Detection complete.")
