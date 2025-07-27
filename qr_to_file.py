import shutil
import cv2
from pyzbar.pyzbar import decode
import os
import base64
import numpy as np
from tqdm import tqdm


def decode_and_combine(qr_code_folder, num_images):
    qr_file_path = os.path.join(qr_code_folder, 'image0.png')

    # Check if the file exists
    if not os.path.isfile(qr_file_path):
        print(f"Error: File not found - {qr_file_path}")
        return None

    img = cv2.imread(qr_file_path, cv2.IMREAD_GRAYSCALE)
    decoded_objects = decode(img)

    if not decoded_objects:
        print("Error: QR code decoding failed.")
        return None

    decoded_data = decoded_objects[0].data.decode('utf-8')
    file_type = decoded_data

    decoded_data = ""

    for i in tqdm(range(1, num_images), desc="Decoding QR codes"):
        qr_code_path = os.path.join(qr_code_folder, f'image{i}.png')

        if not os.path.isfile(qr_code_path):
            print(f"Error: File not found - {qr_code_path}")
            return None

        img = cv2.imread(qr_code_path, cv2.IMREAD_GRAYSCALE)

        decoded_objects = decode(img)

        if not decoded_objects:
            print(f"Error: QR code decoding failed for {qr_code_path}.")
            return None

        decoded_data += decoded_objects[0].data.decode('utf-8')

    binary_data = base64.b64decode(decoded_data)
    binary_array = np.frombuffer(binary_data, dtype=np.uint8)
    combined_image = cv2.imdecode(binary_array, cv2.IMREAD_UNCHANGED)

    if combined_image is not None:
        output_file_path = f'combined_output.{file_type}'
        cv2.imwrite(output_file_path, combined_image)
        return output_file_path
    else:
        print("Error: Combined image is empty.")
        return None


def count_png_images(folder_path):
    # Get all files in the folder
    all_files = os.listdir(folder_path)

    # Filter out only PNG files
    png_files = [file for file in all_files if file.lower().endswith('.png')]

    # Return the count of PNG files
    return len(png_files)

def init():
    qr_code_folder = 'extracted_images'
    num_images = (count_png_images(qr_code_folder))
    output_file_path = decode_and_combine(qr_code_folder, num_images)

    if output_file_path:
        print(f"Combined image saved to: {output_file_path}")
    else:
        print("Failed to save the combined image.")

    shutil.rmtree(qr_code_folder)