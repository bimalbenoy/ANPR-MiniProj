import os
import logging

logging.basicConfig(level=logging.INFO)

def compare_license_plates(file_path):
    license_plates = []

    if not os.path.exists(file_path):
        logging.error(f"❌ File not found: {file_path}")
        return []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    if parts:
                        license_plates.append(parts[0])
        logging.info(f"✅ Successfully parsed {len(license_plates)} license plates.")
        return license_plates
    except Exception as e:
        logging.exception(f"⚠️ An unexpected error occurred while reading {file_path}: {e}")
        return []
