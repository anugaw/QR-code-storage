import shutil
import cv2
import os
import re
from tqdm import tqdm


def images_to_video(input_folder, output_file, fps, frame_size, frame_interval):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]

    # Custom sorting based on the numeric part of the filename using regular expressions
    images.sort(key=lambda x: int(re.search(r'\d+', x).group() if re.search(r'\d+', x) else 0))

    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*"mp4v"), fps, frame_size)

    for img_name in tqdm(images, desc="Creating Video"):
        img_path = os.path.join(input_folder, img_name)
        frame = cv2.imread(img_path)
        frame = cv2.resize(frame, frame_size)

        for _ in range(frame_interval):
            video.write(frame)

    cv2.destroyAllWindows()
    video.release()

def init(input):
    input_folder = input
    output_file = "output_video.mp4"
    fps = 25
    frame_size = (640, 480)
    frame_interval = 5

    images_to_video(input_folder, output_file, fps, frame_size, frame_interval)
    print("Video created successfully.")

    shutil.rmtree(input_folder)
    