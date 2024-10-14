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
HLSManager Module

This module provides the `HLSManager` class to manage the conversion of video to
HLS streams, encryption of HLS streams, and decryption of encrypted HLS streams.

Author: [Your Name]
"""

import os
import subprocess
from Crypto.Random import get_random_bytes


class HLSManager:
    """
    HLSManager handles the conversion, encryption, and decryption of HLS streams.
    """
    def __init__(self):
        pass

    def generate_key(self):
        """
        Generate AES key for HLS encryption.

        Returns:
            bytes: The generated AES key.
        """
        self.key = get_random_bytes(16)
        return self.key

    def convert_to_hls(self, input_file, output_dir, key_info_file=None):
        """
        Convert a video to HLS, with optional encryption.

        Args:
            **input_file** (str): Path to the input video file.
            **output_dir** (str): Directory where the output HLS files will be saved.
            **key_info_file** (str, optional): Path to the key info file for encryption. Defaults to None.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_m3u8 = os.path.join(output_dir, 'output.m3u8').replace("\\", "/")
        ffmpeg_cmd = ['ffmpeg', '-i', input_file, '-hls_playlist_type', 'vod', '-hls_time', '10', output_m3u8]

        if key_info_file:
            key_info_file = key_info_file.replace("\\", "/")
            ffmpeg_cmd.insert(3, '-hls_key_info_file')
            ffmpeg_cmd.insert(4, key_info_file)

        print(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Video converted to HLS and saved to {output_m3u8}")

    def encrypt_hls(self, playlist_file, key_file, iv_hex, key_info_file, output_dir):
        """
        Encrypt an existing HLS stream using FFmpeg.

        Args:
            **playlist_file** (str): Path to the HLS playlist file.
            **key_file** (str): Path to the AES key file.
            **iv_hex** (str): Initialization vector (IV) for encryption.
            **key_info_file** (str): Path to the key info file.
            **output_dir** (str): Directory where the encrypted HLS files will be saved.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_playlist = os.path.join(output_dir, 'output_encrypted.m3u8').replace("\\", "/")
        playlist_file = os.path.abspath(playlist_file).replace("\\", "/")
        key_info_file = key_info_file.replace("\\", "/")

        ffmpeg_cmd = [
            'ffmpeg', '-i', playlist_file,
            '-hls_key_info_file', key_info_file,
            '-hls_playlist_type', 'vod',
            '-hls_time', '10',
            output_playlist
        ]

        print(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")
        try:
            subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Encrypted HLS stream saved to {output_playlist}")
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg failed with error: {e.stderr.decode('utf-8')}")

    def create_key_info_file(self, key_file, iv_hex, key_info_file):
        """
        Create key_info file for HLS encryption.

        Args:
            **key_file** (str): Path to the AES key file.
            **iv_hex** (str): Initialization vector (IV) in hexadecimal format.
            **key_info_file** (str): Path to the key info file to be created.
        """
        absolute_key_path = os.path.abspath(key_file).replace("\\", "/")
        with open(key_info_file, 'w') as f:
            f.write(f"{absolute_key_path}\n")
            f.write(f"{absolute_key_path}\n")
            f.write(f"{iv_hex}\n")
        print(f"key_info generated and saved to {key_info_file}")

    def decrypt_hls(self, input_playlist, output_file, decryption_key_hex, iv_hex=None):
        """
        Decrypt an AES-encrypted HLS playlist.

        Args:
            **input_playlist** (str): Path to the encrypted HLS playlist.
            **output_file** (str): Path to save the decrypted video.
            **decryption_key_hex** (str): Hex-encoded decryption key.
            **iv_hex** (str, optional): Initialization vector (IV) for decryption. Defaults to None.
        """
        if isinstance(decryption_key_hex, bytes):
            decryption_key_hex = decryption_key_hex.hex()

        ffmpeg_cmd = [
            'ffmpeg', '-allowed_extensions', 'ALL',
            '-i', input_playlist,
            '-c', 'copy',
            '-decryption_key', decryption_key_hex
        ]
        if iv_hex:
            ffmpeg_cmd += ['-iv', iv_hex]

        ffmpeg_cmd.append(output_file)
        print(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")

        try:
            result = subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"HLS video decrypted and saved to {output_file}")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode('utf-8') if e.stderr else 'Unknown error'
            print(f"FFmpeg failed with error: {error_message}")
