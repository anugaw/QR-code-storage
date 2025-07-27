import cv2
from os import mkdir
from os.path import join, isdir
from tqdm import tqdm
from qr_to_file import init

class VideoToImagesConverter:
    def img_from_video(self, video_name, save_dir, frame_interval, frame_size):
        cap = cv2.VideoCapture(video_name)
        if not isdir(save_dir):
            mkdir(save_dir)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if frame_count == 0:
            exit("Video file not found")

        output_index = 0  # Counter for output image filenames
        for i in tqdm(range(0, frame_count, frame_interval), desc="Extracting"):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, img = cap.read()
            if ret:
                img = cv2.resize(img, frame_size)
                cv2.imwrite(join(save_dir, 'image%d.png' % output_index), img)
                output_index += 1
        cap.release()


def videostart(name):
    video_name = name
    save_dir = "extracted_images"
    frame_size = (640, 480)
    frame_interval = 5

    # Create an instance of the class and run the conversion
    converter = VideoToImagesConverter()
    converter.img_from_video(video_name, save_dir, frame_interval, frame_size)
    init()

