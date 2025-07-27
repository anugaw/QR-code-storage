import os
import qrcode
import base64
from tqdm import tqdm
from qr_to_video import init

def file_to_qr(file_path, qr_code_prefix):
    chunk_size = 500  # Set your desired chunk size

    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Encode binary data to base64
    base64_data = base64.b64encode(binary_data).decode('utf-8')

    # Ensure proper padding for base64 encoding
    padded_base64_data = base64_data + '=' * (-len(base64_data) % 4)

    # Calculate the number of chunks
    num_chunks = (len(padded_base64_data) + chunk_size - 1) // chunk_size

    # Create the output folder based on the file name
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_folder = f'{file_name}_output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create a QR code for the file type
    file_type = os.path.splitext(file_path)[1][1:]  # Extract file extension without the dot
    file_type_qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    file_type_qr.add_data(file_type)
    file_type_qr.make(fit=True)

    # Save the file type QR code with a specific filename
    file_type_qr_path = os.path.join(output_folder, f'{qr_code_prefix}_file_type.png')
    file_type_img = file_type_qr.make_image(fill_color="black", back_color="white")
    file_type_img.save(file_type_qr_path)

    for i in tqdm(range(num_chunks), desc='Creating QR codes', unit='chunk'):
        # Get a chunk of data
        start = i * chunk_size
        end = (i + 1) * chunk_size
        chunk = padded_base64_data[start:end]

        # Create a QR code for the chunk
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(chunk)
        qr.make(fit=True)

        # Save the QR code in the output folder with a unique filename
        qr_code_path = os.path.join(output_folder, f'{qr_code_prefix}_{i + 1}.png')
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_code_path)

# Replace these with your actual folder paths and desired output filename
def start(filename):
    file_path = filename
    file_name = os.path.splitext(file_path)[0]
    folder = f'{file_name}_output'
    qr_code_prefix = 'image'
    file_to_qr(file_path, qr_code_prefix)
    input_folder = folder
    init(input_folder)
