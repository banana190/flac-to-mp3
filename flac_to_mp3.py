import os
import concurrent.futures
import ffmpeg


def convert_flac_to_mp3(input_folder, output_folder, bitrate="128k", num_threads=8):
    os.makedirs(output_folder, exist_ok=True)

    def convert_file(flac_path):
        mp3_filename = os.path.splitext(os.path.basename(flac_path))[0] + ".mp3"
        output_root = os.path.dirname(flac_path)
        search_string = "Music0"
        replacement = "Music"
        output_root = output_root.replace(search_string, replacement)
        os.makedirs(output_root, exist_ok=True)
        mp3_path = os.path.join(output_root, mp3_filename)

        flac_audio = ffmpeg.input(flac_path)
        ffmpeg.output(flac_audio, mp3_path, acodec='libmp3lame', ab="320k").run()

    flac_files = []
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".flac"):
                flac_files.append(os.path.join(root, filename))

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(convert_file, flac_files)


if __name__ == "__main__":
    input_folder = r".\your_input_file_here"  # 替换为包含FLAC文件的文件夹路径
    output_folder = r".\your_output_file_here"  # 替换为保存MP3文件的文件夹路径
    convert_flac_to_mp3(input_folder, output_folder, num_threads=8)