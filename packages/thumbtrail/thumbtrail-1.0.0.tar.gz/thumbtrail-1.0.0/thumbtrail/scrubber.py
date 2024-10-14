
# MIT License
#
# Copyright (c) 2024 Sariya Ansari
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Scrubber Module

This module provides the `Scrubber` class to manage the generation of video thumbnails
and WebVTT files. It supports decryption of encrypted video streams (AES and HLS)
before generating the thumbnails.

Author: [Your Name]
"""

import cv2
import os
from datetime import timedelta
from PIL import Image
from thumbtrail.aesmanager import AESManager
from thumbtrail.hlsmanager import HLSManager


class Scrubber:
    """
    Scrubber handles the generation of video thumbnails and WebVTT files.
    It supports both encrypted and clear video streams.
    """
    def __init__(self, video_path, output_path=None, decryption_method=None, key_file=None, iv_file=None):
        """
        Initialize Scrubber with optional decryption.

        Args:
            **video_path** (str): Path to the encrypted or clear video file.
            **output_path** (str, optional): Directory where output files (thumbnails and WebVTT) will be saved. Defaults to current working directory.
            **decryption_method** (str, optional): Specify the decryption method ('AES', 'HLS', or None). Defaults to None.
            **key_file** (str, optional): Path to the file containing the decryption key (for AES or HLS). Defaults to None.
            **iv_file** (str, optional): Path to the file containing the IV (only for AES decryption). Defaults to None.
        """
        self.video_path = video_path
        self.decryption_method = decryption_method
        self.key_file = key_file
        self.iv_file = iv_file
        self.output_path = output_path if output_path else os.getcwd()

        # Ensure the output directory exists
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def _format_time(self, seconds):
        """
        Helper function to format time in WebVTT format (HH:MM:SS.mmm).

        Args:
            **seconds** (int): Time in seconds.

        Returns:
            str: Time formatted in WebVTT format.
        """
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((td.total_seconds() - total_seconds) * 1000)
        return f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'

    def _read_key(self, key_file):
        """
        Helper function to read the decryption key from a file.

        Args:
            **key_file** (str): Path to the key file.

        Returns:
            bytes: The key read from the file.
        """
        with open(key_file, 'rb') as f:
            return f.read()

    def _decrypt_video_if_needed(self):
        """
        Decrypt the video if necessary, using AESManager or HLSManager.

        Returns:
            str: Path to the decrypted video file.
        """
        if not self.decryption_method:
            print("The video stream is clear. No decryption needed.")
            return self.video_path

        print(f"Decrypting video: {self.video_path} using {self.decryption_method}...")

        base_name, extension = os.path.splitext(os.path.basename(self.video_path))
        decrypted_file_name = f"{base_name}_decrypted{extension}"
        decrypted_video_path = os.path.join(self.output_path, decrypted_file_name)

        if self.decryption_method == "AES":
            aes_key = self._read_key(self.key_file)
            aes_iv = self._read_key(self.iv_file)
            aes_manager = AESManager(aes_key, aes_iv)
            aes_manager.decrypt_video(self.video_path, decrypted_video_path)

        elif self.decryption_method == "HLS":
            hls_manager = HLSManager()
            hls_manager.decrypt_hls(self.video_path, decrypted_video_path, self._read_key(self.key_file))

        return decrypted_video_path

    def _merge_thumbnails(self, thumbnail_list, thumbnail_size, output_image_path):
        """
        Helper function to merge thumbnails into a single image.

        Args:
            **thumbnail_list** (list): List of thumbnail image arrays.
            **thumbnail_size** (tuple): Size of each thumbnail.
            **output_image_path** (str): Path to save the merged image.

        Returns:
            list: Coordinates of each thumbnail in the merged image.
        """
        columns = 5
        rows = (len(thumbnail_list) + columns - 1) // columns
        merged_image = Image.new("RGB", (columns * thumbnail_size[0], rows * thumbnail_size[1]))

        coordinates = []
        for i, thumbnail_array in enumerate(thumbnail_list):
            thumbnail_rgb = cv2.cvtColor(thumbnail_array, cv2.COLOR_BGR2RGB)
            thumbnail = Image.fromarray(thumbnail_rgb)
            row = i // columns
            col = i % columns
            merged_image.paste(thumbnail, (col * thumbnail_size[0], row * thumbnail_size[1]))
            coordinates.append((col * thumbnail_size[0], row * thumbnail_size[1]))

        merged_image.save(output_image_path)
        return coordinates

    def generate_thumbnails_and_webvtt(self, interval=5, thumbnail_size=(160, 90),
                                       image_format="jpg", should_merge_thumbnails=False,
                                       use_absolute_paths=False, thumbnail_url=None):
        """
        Generate thumbnails and WebVTT for a video.

        Args:
            **interval** (int, optional): Time interval between thumbnails (in seconds). Defaults to 5.
            **thumbnail_size** (tuple, optional): Size of each thumbnail. Defaults to (160, 90).
            **image_format** (str, optional): Format for thumbnail images. Defaults to "jpg".
            **should_merge_thumbnails** (bool, optional): Whether to merge all thumbnails into one image. Defaults to False.
            **use_absolute_paths** (bool, optional): Whether to use absolute paths in WebVTT. Defaults to False.
            **thumbnail_url** (str, optional): URL prefix for thumbnails in WebVTT. Defaults to None.
        """
        decrypted_video_path = self._decrypt_video_if_needed()

        vtt_file_path = os.path.join(self.output_path, f"{os.path.splitext(os.path.basename(decrypted_video_path))[0]}.vtt")
        thumbnail_list = []

        video = cv2.VideoCapture(decrypted_video_path)

        if not video.isOpened():
            print(f"Error: Unable to open video file: {decrypted_video_path}")
            return

        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps

        with open(vtt_file_path, "w") as vtt_file:
            vtt_file.write("WEBVTT\n\n")

            for sec in range(0, int(duration), interval):
                frame_number = int(fps * sec)
                video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                success, frame = video.read()

                if not success:
                    print(f"Warning: Could not read frame at {sec} seconds")
                    continue

                thumbnail = cv2.resize(frame, thumbnail_size)

                if should_merge_thumbnails:
                    thumbnail_list.append(thumbnail)
                else:
                    thumbnail_filename = f"thumbnail_{sec}.{image_format}"
                    thumbnail_filepath = os.path.join(self.output_path, thumbnail_filename)
                    cv2.imwrite(thumbnail_filepath, thumbnail)
                    thumbnail_list.append(thumbnail_filepath)

                    if thumbnail_url:
                        if not thumbnail_url.endswith('/'):
                            thumbnail_url += '/'
                        thumbnail_path_in_vtt = f"{thumbnail_url}{thumbnail_filename}"
                    else:
                        thumbnail_path_in_vtt = os.path.abspath(thumbnail_filepath) if use_absolute_paths else os.path.basename(thumbnail_filepath)

                    start_time = self._format_time(sec)
                    end_time = self._format_time(sec + interval)
                    vtt_file.write(f"{start_time} --> {end_time}\n")
                    vtt_file.write(f"{thumbnail_path_in_vtt}\n\n")

            if should_merge_thumbnails:
                merged_image_path = os.path.join(self.output_path, f"merged_thumbnails.{image_format}")
                coordinates = self._merge_thumbnails(thumbnail_list, thumbnail_size, merged_image_path)
                merged_image_path_in_vtt = os.path.abspath(merged_image_path) if use_absolute_paths else os.path.basename(merged_image_path)

                for i, sec in enumerate(range(0, int(duration), interval)):
                    start_time = self._format_time(sec)
                    end_time = self._format_time(sec + interval)
                    x, y = coordinates[i]
                    vtt_file.write(f"{start_time} --> {end_time}\n")
                    vtt_file.write(f"{merged_image_path_in_vtt}#xywh={x},{y},{thumbnail_size[0]},{thumbnail_size[1]}\n\n")

        video.release()
        print(f"Thumbnails and WebVTT file generated in {self.output_path}")

        if self.decryption_method:
            print(f"Deleting decrypted video: {decrypted_video_path}")
            os.remove(decrypted_video_path)
