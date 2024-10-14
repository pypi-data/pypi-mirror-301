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
CryptoManager Module

This module provides the `CryptoManager` class to unify AES and HLS encryption and decryption operations.
It acts as a high-level manager for the underlying `AESManager` and `HLSManager` classes.

Author: [Your Name]
"""

import os
from thumbtrail.aesmanager import AESManager
from thumbtrail.hlsmanager import HLSManager
from Crypto.Random import get_random_bytes


class CryptoManager:
    """
    CryptoManager unifies encryption and decryption for AES and HLS streams.
    It acts as a high-level controller for handling video security.
    """
    def __init__(self):
        self.aes_manager = AESManager()
        self.hls_manager = HLSManager()

    def generate_aes_key_iv(self):
        """
        Generate AES key and IV, and initialize AESManager with the key and IV.
        """
        aes_manager = AESManager()  # AESManager generates key/IV if none are provided
        self.aes_key, self.aes_iv = aes_manager.generate_key_iv()
        self.aes_manager = aes_manager  # Store AESManager instance for future operations
        print(f"AES key: {self.aes_key.hex()}\nIV: {self.aes_iv.hex()}")

    def save_aes_key_iv(self, key_file, iv_file):
        """
        Save AES key and IV to specified files.

        Args:
            **key_file** (str): Path to save the AES key.
            **iv_file** (str): Path to save the AES IV.
        """
        if self.aes_manager:
            self.aes_manager.save_key_iv(key_file, iv_file)
        else:
            print("AESManager not initialized. Please generate or load AES key and IV.")

    def load_aes_key_iv(self, key_file, iv_file):
        """
        Load AES key and IV from specified files and initialize AESManager.

        Args:
            **key_file** (str): Path to the AES key file.
            **iv_file** (str): Path to the AES IV file.
        """
        aes_manager = AESManager()
        aes_manager.load_key_iv(key_file, iv_file)
        self.aes_manager = aes_manager

    def encrypt_video_aes(self, input_file, output_file):
        """
        AES Encrypt video using the AESManager.

        Args:
            **input_file** (str): Path to the input video file.
            **output_file** (str): Path to save the encrypted video.
        """
        if not self.aes_manager:
            raise Exception("AES Manager not initialized. Please generate or load AES key and IV.")
        self.aes_manager.encrypt_video(input_file, output_file)

    def decrypt_video_aes(self, input_file, output_file):
        """
        AES Decrypt video using the AESManager.

        Args:
            **input_file** (str): Path to the AES-encrypted video file.
            **output_file** (str): Path to save the decrypted video.
        """
        if not self.aes_manager:
            raise Exception("AES Manager not initialized. Please generate or load AES key and IV.")
        self.aes_manager.decrypt_video(input_file, output_file)

    def generate_hls_key_info(self, output_dir):
        """
        Generate HLS key info file and AES key for encryption, storing them in the specified output directory.

        Args:
            **output_dir** (str): Directory where HLS key and info file will be stored.

        Returns:
            tuple: Paths to the generated key file, key info file, and IV (hex).
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        key_file = os.path.join(output_dir, 'hls_key.key')
        key_info_file = os.path.join(output_dir, 'hls_key_info.txt')

        key = self.hls_manager.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)

        iv_hex = get_random_bytes(16).hex()
        self.hls_manager.create_key_info_file(key_file, iv_hex, key_info_file)

        print(f"HLS key_info.txt and key generated in {output_dir}")
        return key_file, key_info_file, iv_hex

    def convert_video_to_hls(self, input_file, output_dir, key_info_file=None):
        """
        Convert video to HLS with optional encryption.

        Args:
            **input_file** (str): Path to the input video file.
            **output_dir** (str): Directory where the output HLS files will be saved.
            **key_info_file** (str, optional): Path to the key info file for encryption. Defaults to None.
        """
        self.hls_manager.convert_to_hls(input_file, output_dir, key_info_file)

    def encrypt_existing_hls(self, playlist_file, output_dir):
        """
        Encrypt an existing HLS stream.

        Args:
            **playlist_file** (str): Path to the HLS playlist file.
            **output_dir** (str): Directory where the encrypted HLS files will be saved.
        """
        key_file, key_info_file, iv_hex = self.generate_hls_key_info(output_dir)
        self.hls_manager.encrypt_hls(playlist_file, key_file, iv_hex, key_info_file, output_dir)

    def decrypt_hls_video(self, input_playlist, output_file, decryption_key_hex, iv_hex=None):
        """
        Decrypt HLS video.

        Args:
            **input_playlist** (str): Path to the encrypted HLS playlist.
            **output_file** (str): Path to save the decrypted video.
            **decryption_key_hex** (str): Hex-encoded decryption key.
            **iv_hex** (str, optional): Initialization vector (IV) for decryption. Defaults to None.
        """
        self.hls_manager.decrypt_hls(input_playlist, output_file, decryption_key_hex, iv_hex)
