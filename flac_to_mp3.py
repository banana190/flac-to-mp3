import os
import concurrent.futures
import ffmpeg
import shutil
from functools import partial

def convert_flac_to_mp3(input_folder, output_folder, bitrate="320k", num_threads=4):
    os.makedirs(output_folder, exist_ok=True)

    def convert_file(flac_path, search_string, replacement, bitrate):
        mp3_filename = os.path.splitext(os.path.basename(flac_path))[0] + ".mp3"
        output_root = os.path.dirname(flac_path)
        output_root = output_root.replace(search_string, replacement)
        os.makedirs(output_root, exist_ok=True)
        mp3_path = os.path.join(output_root, mp3_filename)
        if not os.path.exists(mp3_path):
            flac_audio = ffmpeg.input(flac_path)
            ffmpeg.output(flac_audio, mp3_path, acodec='libmp3lame', ab=bitrate).run()
            print(f"Converted: {flac_path} -> {mp3_path}")
        else:
            print(f"Skipped: {flac_path} (MP3 already exists)")

    flac_files = []
    folder_images = []

    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".flac"):
                flac_files.append(os.path.join(root, filename))
            elif filename.endswith((".png", ".jpg")):
                folder_images.append(os.path.join(root, filename))

    input_folder_parts = input_folder.split(os.path.sep)
    output_folder_parts = output_folder.split(os.path.sep)
    search_string = input_folder_parts[1]
    replacement = output_folder_parts[1]

    for image in folder_images:
        output_image_path = os.path.dirname(image)
        output_image_path = output_image_path.replace(search_string, replacement)
        os.makedirs(output_image_path, exist_ok=True)
        shutil.copy(image, output_image_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        convert_file_with_args = partial(
            convert_file,
            search_string=search_string,
            replacement=replacement,
            bitrate=bitrate
        )
        executor.map(convert_file_with_args, flac_files)

if __name__ == "__main__":
    input_folder = r".\Music0"
    output_folder = r".\Music"
    convert_flac_to_mp3(input_folder, output_folder, bitrate="320k", num_threads=8)
